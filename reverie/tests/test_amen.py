#%%
import sys
sys.path.append('../backend_server')
from dotenv import load_dotenv
load_dotenv("../backend_server/.env")

import os
import glob
import json
import pandas as pd
from pathlib import Path
from loguru import logger

from persona.memory_structures.associative_memory import AssociativeMemory
from persona.prompt_template.openai_helper import initialize_openai_client

"""TODO
[ ] 实现 Milvus 建库
[ ] memory id 需要外部维护一个，或者简单一点直接 uuid4

"""

def load_memory_to_points(folder):
    folder = Path(folder) / "bootstrap_memory/associative_memory"

    # nodes
    df_nodes = pd.read_json(folder / "nodes.json").T
    text_2_embedding = json.load(open(folder / "embeddings.json"))
    embs = df_nodes.embedding_key.map(lambda x: text_2_embedding.get(x, []))

    points = [
        # {'id': int(id.split("_")[-1]), 'payload': payload, 'vector': emb}
        {'id': int(id.split("_")[-1]), 'vector': emb, **payload}
            for (id, payload), emb in
                zip(df_nodes.to_dict(orient='index').items(), embs)
    ]

    # try:
    #     from qdrant_client.http.models import PointStruct
    #     points = [PointStruct(**p) for p in points]
    # except:
    #     pass

    return points

def read_memory(folder, person):
    ass_mem_folder = folder / person / "bootstrap_memory/associative_memory"

    a_men = AssociativeMemory(str(ass_mem_folder))

    logger.debug(a_men.get_summarized_latest_events(10))
    logger.debug(f"get_str_seq_events: \n{a_men.get_str_seq_events()}")
    logger.debug(f"get_str_seq_thoughts: \n{a_men.get_str_seq_thoughts()}")
    logger.debug(f"get_str_seq_chats: \n{a_men.get_str_seq_chats()}")

    return a_men

def test_get_memory_by_spo(a_men):
    #! spo 关键字检索
    s = 'isabella rodriguez'
    s = "the Ville:Isabella Rodriguez's apartment:main room:bed"
    p = 'used'
    o = 'bed'

    a_men.retrieve_relevant_thoughts(s, p, o)
    a_men.retrieve_relevant_events(s, p, o)

    return a_men

def load_all_memory(folder):
    all_points = []
    idx = 0
    for sub_folder in glob.glob(f"{folder}/*"):
        person_name = os.path.basename(sub_folder)
        points = load_memory_to_points(sub_folder)
        for p in points:
            p['ori_id'] = p['id']
            p['owner'] = person_name
            p['id'] = idx
            idx += 1
        all_points.extend(points)

    logger.info(f"load memory points: {len(all_points)}")

    return all_points


folder = Path("../../environment/frontend_server/storage/July1_the_ville_isabella_maria_klaus-step-3-21/personas")
persona = "Isabella Rodriguez"
# a_men = read_memory(folder, persona)

all_points = load_all_memory(folder)
all_points[0].keys()
# add to schema: 'owner', vector, poignancy, 'subject', 'predicate', 'object', 'created', 'expiration',
# ['', 'node_count', 'type_count', 'type', 'depth', 'description', 'embedding_key', 'keywords', 'filling', 'ori_id', ]
all_points[0]

#%%
_, chat, embeddings = initialize_openai_client()

query = "sleeping"
query = "Valentine's Day"
emb = embeddings(input=query, model="text-embedding-ada-002")
query_vector = emb.data[0].embedding
query_vector

#%%
#! Milvus
import os
from loguru import logger
from typing import Dict, List, Optional, Union
from pymilvus import MilvusClient, DataType

COLLECTION_NAME = "memory"
EMBEDDING_DIM = 1536
MILVUS_URI = os.environ.get("MILVUS_URI", "../data/test_milvus.db")


class VectorDB:
    def __init__(self, collection_name, embedding_dim, milvus_uri=MILVUS_URI):
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self.milvus_uri = milvus_uri or os.environ.get("MILVUS_URI", "../data/test_milvus.db")
        self.client = MilvusClient(self.milvus_uri)

        self.schema = None
        self.index_params = None

    def create_schema(self):
        """Creates a schema for the collection."""
        schema = self.client.create_schema(enable_dynamic_field=True)
        schema.add_field(field_name='id', datatype=DataType.INT64, is_primary=True, auto_id=False)
        schema.add_field(field_name='owner', datatype=DataType.VARCHAR, max_length=100)
        schema.add_field(field_name='subject', datatype=DataType.VARCHAR, max_length=100)
        schema.add_field(field_name='predicate', datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name='object', datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name='created', datatype=DataType.VARCHAR, max_length=50)
        schema.add_field(field_name='embedding_key', datatype=DataType.VARCHAR, max_length=4096)
        schema.add_field(field_name='poignancy', datatype=DataType.INT64)
        schema.add_field(field_name='vector', datatype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)
        self.schema = schema

        formatted_json = str(schema.fields).replace('}, {', '}, \n {')
        logger.debug(f"schema:\n{formatted_json}")
        return schema

    def create_index_params(self):
        """Creates index parameters for the collection."""
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name='vector',
            # index_type="IVF_FLAT",
            metric_type='IP',
            index_name="text_emb",
            params={"nlist": 128}
        )
        index_params.add_index(field_name='subject', index_name='subject_index')
        index_params.add_index(field_name='predicate', index_name='predicate_index')
        index_params.add_index(field_name='object', index_name='object_index')

        self.index_params = index_params
        formatted_json = str(index_params).replace('}, {', '}, \n {')
        logger.debug(f"index_params: \n{formatted_json}")

        return index_params

    def create_collection(self, replace=False):
        """Drops and creates the collection with schema and index."""
        if self.client.has_collection(self.collection_name):
            if not replace:
                self.client.load_collection(self.collection_name)
                return
            self.client.drop_collection(self.collection_name)

        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=self.embedding_dim,
            schema=self.schema,
            index_params=self.index_params
        )
        indexes = self.client.list_indexes(self.collection_name)
        logger.debug(f"Indexes: {indexes}")

        return

    def insert(self, all_points, **kwargs):
        """Inserts data into the collection."""
        self.client.insert(self.collection_name, all_points, **kwargs)

    def delete(self, **kwargs):
        return self.client.delete(self.collection_name, **kwargs)

    def delete_by_ids(self, ids:list, **kwargs):
        return self.client.delete(self.collection_name, ids, **kwargs)

    """ search, query & get """
    def search(
        self,
        data: Union[List[list], list],
        filter: str = "",
        limit: int = 10,
        output_fields: Optional[List[str]] = None,
        search_params: Optional[dict] = None,
        timeout: Optional[float] = None,
        partition_names: Optional[List[str]] = None,
        anns_field: Optional[str] = None,
        **kwargs,
    ):
        return self.client.search(
            self.collection_name,
            data=data,
            filter=filter,
            limit=limit,
            output_fields=output_fields,
            search_params=search_params,
            timeout=timeout,
            partition_names=partition_names,
            anns_field=anns_field,
            **kwargs
        )

    def get(self, ids, output_fields=None, timeout=None, partition_names=None, **kwargs):
        """
        Grab the inserted vectors using the primary key from the Collection.
        """
        return self.client.get(
            self.collection_name,
            ids=ids,
            output_fields=output_fields,
            timeout=timeout,
            partition_names=partition_names,
            **kwargs
        )

    def query(
        self,
        filter: str = "",
        output_fields: Optional[List[str]] = None,
        timeout: Optional[float] = None,
        ids: Optional[Union[List, str, int]] = None,
        partition_names: Optional[List[str]] = None,
        **kwargs,
    ):
        return self.client.query(
            self.collection_name,
            filter=filter,
            output_fields=output_fields,
            timeout=timeout,
            ids=ids,
            partition_names=partition_names,
            **kwargs
        )

    def update(self, ids, update_params: dict, timeout=None, partition_names=None, **kwargs):
        data = self.get(ids=ids)
        for i in data:
            for key, val in update_params.items():
                i[key] = val

        return self.client.upsert(
            self.collection_name,
            data=data,
            timeout=timeout,
            partition_name=partition_names,
            **kwargs
        )

    def get_collection_stats(self):
        """Retrieves collection statistics."""
        return self.client.get_collection_stats(self.collection_name)


# if __name__ == "__main__":
vector_db = VectorDB(COLLECTION_NAME, EMBEDDING_DIM)

schema = vector_db.create_schema()
index_params = vector_db.create_index_params()

vector_db.create_collection(replace=True)
client = vector_db.client

vector_db.insert(all_points)

#%%
# 增
# vector_db.insert(COLLECTION_NAME, all_points)

# 删
# vector_db.delete(filter="")
# vector_db.delete_by_ids(ids=[1,2])

# 改
# vector_db.update([1], {'node_count': -1})

# 查
# vector_db.get(ids=[1, 2])
# vector_db.query(filter=' id in [1, 2] ')
# vector_db.searc(xxx)

# 获取状态
client.get_collection_stats(COLLECTION_NAME)


#%%

import pandas as pd
import numpy as np

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

def retrieve_nodes(
    vector_db,
    query_vector,
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
    filter_expr = f'owner == "{persona_name}"' \
                  f' and type in ["evnet", "thought"]' \
                  f' "idle" not in embedding_key'

    # Perform the vector search in the vector database
    res = vector_db.search(
        [query_vector],
        filter=filter_expr,
        limit=top_k*3,
        output_fields=output_fields
    )

    # Convert the search results into a DataFrame
    df = pd.DataFrame(res[0])
    df = pd.concat(
        [df[['id', 'distance']], pd.json_normalize(df.entity)[output_fields]],
        axis=1
    )

    # Normalize importance (poignancy), relevance (distance), and recency
    importance = normalize_series_floats(df.poignancy)
    relevance = normalize_series_floats(df.distance)
    recency = calculate_recency_decay(df.created, recency_decay)
    recency = normalize_series_floats(recency)

    # Calculate the final score based on the given weights
    df['score'] = recency * recency_weight + relevance * relevence_weight + importance * importance_weight

    # Sort the results by score and return the top-k results
    _df = df.sort_values(by='score', ascending=False).head(top_k)

    return _df

query = "dinner"
emb = embeddings(input=query, model="text-embedding-ada-002")
query_vector = emb.data[0].embedding
query_vector

persona_name = "Isabella Rodriguez"
df = retrieve_nodes(vector_db, query_vector, persona_name)
df


#%%

s = "the Ville:Isabella Rodriguez's apartment:main room:bed"
p = 'used'
o = 'scheduled'


res = client.query(
    collection_name=COLLECTION_NAME,
    filter= f'object == "{o}" '
)

pd.DataFrame()


# %%
