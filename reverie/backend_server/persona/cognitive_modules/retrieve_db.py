#%%
import sys
sys.path.append("../../")

import pandas as pd
import numpy as np
from loguru import logger
from db.vector_db_manager import VectorDB, COLLECTION_NAME, EMBEDDING_DIM
from persona.prompt_template.gpt_structure import get_embedding # type: ignore

TIME_COL = 'created'


def calculate_recency_decay(series, decay_factor=0.995):
    """
    根据 pd.Series 中的时间，找到时间最近的作为基点，计算每个时间的相对衰减情况。

    输入:
    series: pd.Series. 其中包含时间字符串，例如 "2023-02-13 17:55:10"
    decay_factor: float. 衰减因子, 默认为 0.995

    输出:
    recency_scores: pd.Series. 每个时间的相对衰减分数
    """

    # 将时间字符串转换为 datetime 格式
    time_series = pd.to_datetime(series)

    # 找到最近的时间（最大时间）
    max_time = time_series.max()

    # 计算每个时间与最近时间的差异（以小时为单位）
    time_diff_hours = (max_time - time_series).dt.total_seconds() / 3600

    # 计算衰减分数，公式： decay_factor ^ time_diff_hours
    recency_scores = decay_factor ** time_diff_hours

    return recency_scores

def normalize_series_floats(series, target_min=0, target_max=1):
    """
    This function normalizes the float values of a given pandas Series 'series' between
    a target minimum and maximum value. The normalization is done by scaling the
    values to the target range while maintaining the same relative proportions
    between the original values.

    INPUT:
      series: pandas.Series. The input Series whose float values need to be
              normalized.
      target_min: Integer or float. The minimum value to which the original
                  values should be scaled.
      target_max: Integer or float. The maximum value to which the original
                  values should be scaled.
    OUTPUT:
      normalized_series: A new pandas Series with the same index as the input but
                         with the float values normalized between target_min and
                         target_max.

    Example input:
      series = pd.Series({'a': 1.2, 'b': 3.4, 'c': 5.6, 'd': 7.8})
      target_min = -5
      target_max = 5
    """
    min_val = series.min()
    max_val = series.max()
    range_val = max_val - min_val

    if range_val == 0:
        # All values are the same, set all to the midpoint of the target range
        normalized_series = pd.Series(
            [(target_max - target_min) / 2] * len(series),
            index=series.index
        )
    else:
        # Apply normalization
        normalized_series = (series - min_val) * (target_max - target_min) / range_val + target_min

    return normalized_series

def retrieve_adapter(vector_db, owner=None, subject=None, predicate=None, object=None, op='or'):
    if owner is None and subject is None and predicate is None and object is None:
        return []

    expr_lst = []
    if subject:
        expr_lst.append(f'subject == "{subject}"')
    if predicate:
        expr_lst.append(f'predicate == "{predicate}"')
    if object:
        expr_lst.append(f'object == "{object}"')
    expr = f" {op} ".join(expr_lst)
    if owner:
        expr = f'({expr}) and owner ==  "{owner}" '

    res = vector_db.query(
        filter = expr,
        # output_fields=[TIME_COL]
    )

    res = pd.DataFrame(res).sort_values(TIME_COL, ascending=False)
    return res

def retrieve(persona_name, perceived, vector_db):
    retrieved = {}
    for event in perceived:
        df = retrieve_adapter(vector_db, persona_name, event.subject, event.predicate, event.object)
        retrieved[event.description] = {
            "curr_envent": event,
            "events": [record for _, record in df.query("type == 'event' ").iterrows()],
            "thoughts": [record for _, record in df.query("type == 'thought' ").iterrows()]
        }

    return retrieved

def retrieve_nodes_adapter(
    vector_db,
    query_vectors,
    persona_name,
    top_k=30,
    recency_weight=0.5,
    relevence_weight=3,
    importance_weight=2,
    recency_decay=0.995,
    output_fields=['poignancy', 'created', 'subject', 'predicate', 'object', 'embedding_key']
):
    """
    Retrieves relevant nodes based on the given query vector, persona name, and
    various weighting factors for recency, relevance, and importance.

    INPUT:
      vector_db: Vector database client object.
      query_vector: Vector used to search for relevant nodes.
      persona_name: The name of the persona to filter nodes.
      top_k: Number of top results to return. Default is 30.
      recency_weight: Weight given to the recency score. Default is 0.5.
      relevence_weight: Weight given to the relevance score. Default is 3.
      importance_weight: Weight given to the importance score. Default is 2.
      recency_decay: Decay factor for calculating recency. Default is 0.995.

    OUTPUT:
      _df: A pandas DataFrame of the top retrieved nodes, sorted by the final score.
    """

    # Construct filter expression
    filter_expr = f' owner == "{persona_name}" and type in ["event", "thought"]' #  and not embedding_key like "%idle%"
    logger.debug(filter_expr)

    # Perform the vector search in the vector database
    res_lst = vector_db.search(
        query_vectors,
        filter=filter_expr,
        limit=top_k*3,
        output_fields=output_fields
    )

    df_res = []
    for res in res_lst:
        # Convert the search results into a DataFrame
        df = pd.DataFrame(res)
        df = pd.concat(
            [df[['id', 'distance']], pd.json_normalize(df.entity)[output_fields]],
            axis=1
        )
        # FIXME 移到 filter_expr
        df = df[~df['embedding_key'].str.contains("idle", na=False)]

        # Normalize importance (poignancy), relevance (distance), and recency
        importance = df.poignancy / 10
        # importance = normalize_series_floats(df.poignancy)
        relevance = df.distance
        # relevance = normalize_series_floats(df.distance)
        recency = calculate_recency_decay(df.created, recency_decay)
        recency = normalize_series_floats(recency)

        # Calculate the final score based on the given weights
        df['score'] = recency * recency_weight + relevance * relevence_weight + importance * importance_weight

        # Sort the results by score and return the top-k results
        _df = df.sort_values(by='score', ascending=False).head(top_k)
        df_res.append(_df)

    return df_res

def new_retrieve(persona_name, focal_points, vector_db, n_count=30):
    retrieved = {}
    embs = [get_embedding(pt) for pt in focal_points]
    res = retrieve_nodes_adapter(vector_db, embs, persona_name, top_k=n_count)
    for text, ans in zip(focal_points, res):
        retrieved[text] = [i for _, i in ans.iterrows()]

    return retrieved


#%%
if __name__ == "__main__":
    vector_db = VectorDB(COLLECTION_NAME, EMBEDDING_DIM, "../../../data/test_milvus.db")
    vector_db.create_collection(replace=False)

    # vector_db.get(ids=[1])

    #%%
    persona_name = "Isabella Rodriguez"

    """ 1. check `retrieve_adapter` """
    s = "the Ville:Isabella Rodriguez's apartment:main room:bed"
    p = 'used'
    o = 'scheduled'

    df = retrieve_adapter(vector_db, persona_name, s, p, o)
    retrieved = {
        "events": [record for _, record in df.query("type == 'event' ").iterrows()],
        "thoughts": [record for _, record in df.query("type == 'thought' ").iterrows()]
    }
    perceived = [retrieved["events"][0]]
    perceived

    """ 1.1 check `retrieve` """
    retrieved = retrieve(persona_name, perceived, vector_db)
    retrieved.keys()

    """ 1.2 结果校核 """
    key = list(retrieved.keys())[0]
    retrieved[key]['curr_envent']
    pd.DataFrame(retrieved[key]['events'])
    pd.DataFrame(retrieved[key]['thoughts'])


    # %%

    """ 2.1 emb 检索 """
    query_vector = get_embedding("Valentine's Day")
    res = retrieve_nodes_adapter(vector_db, [query_vector, np.array(query_vector)*0.8], persona_name)
    res[0]
    res[1]

    """ 2.2 new_retrieve 测试"""
    focal_points = ["Valentine's Day", "sleeping"]
    retrieved = new_retrieve(persona_name, focal_points, vector_db, n_count=8)
    retrieved.keys()

    pd.DataFrame(retrieved[focal_points[0]])
    pd.DataFrame(retrieved[focal_points[1]])
