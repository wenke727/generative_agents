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
from db.vector_db_manager import get_qdrant_client_cfg, VectoreDB

"""TODO
[ ] 实现 Milvus 建库
[ ] memory id 需要外部维护一个，或者简单一点直接 uuid4

"""

#%%
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

def test_get_memory_by_spo():
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
        points = load_memory_to_points(folder / persona)
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
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType

COLLECTION_NAME = "memory"
EMBEDDING_DIM = 1536


client = MilvusClient("./test_milvus.db")

# schema
schema = client.create_schema(enable_dynamic_field=True)
schema.add_field(field_name='id', datatype=DataType.INT64, is_primary=True) # , auto_id=True
schema.add_field(field_name='owner', datatype=DataType.VARCHAR, max_length=100)
schema.add_field(field_name='subject', datatype=DataType.VARCHAR, max_length=100)
schema.add_field(field_name='predicate', datatype=DataType.VARCHAR, max_length=256)
schema.add_field(field_name='object', datatype=DataType.VARCHAR, max_length=256)
schema.add_field(field_name='created', datatype=DataType.VARCHAR, max_length=50)
schema.add_field(field_name='embedding_key', datatype=DataType.VARCHAR, max_length=65535)
schema.add_field(field_name='poignancy', datatype=DataType.INT64) # , is_partition_key=True
schema.add_field(field_name='vector', datatype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
formatted_json = str(schema.fields).replace('}, {', '}, \n {')
logger.debug(f"schema:\n{formatted_json}")

# index
index_params = client.prepare_index_params()
index_params.add_index(
    field_name='vector',
    metric_type='IP',
    # index_type="IVF_FLAT",
    index_name="text_emb",
    params={"nlist": 128}
)
index_params.add_index(field_name='owner', index_name='owner_index')
index_params.add_index(field_name='subject', index_name='subject_index')
index_params.add_index(field_name='object', index_name='object_index')
index_params.add_index(field_name='predicate', index_name='predicate_index')
index_params.add_index(field_name='poignancy', index_name='poignancy_index')
formatted_json = str(index_params).replace('}, {', '}, \n {')
logger.debug(f"index_params: \n{formatted_json}")

# if client.has_collection(COLLECTION_NAME):
#     client.load_collection(COLLECTION_NAME)
client.drop_collection(COLLECTION_NAME)
client.create_collection(
    collection_name=COLLECTION_NAME,
    dimension=EMBEDDING_DIM,
    schema=schema,
    index_params=index_params,
    # index_params=index_params,
)
indexs = client.list_indexes(COLLECTION_NAME)
logger.debug(f"indexs: {indexs}")
# self.client.create_index(self.collection_name, self.index_params)


#%%
# 增加数据
client.insert(COLLECTION_NAME, all_points)

# delete
# client.delete(COLLECTION_NAME, filter="")

# modified, 需要注意的是： collection 不能 auto_id, 此外更新需要提供全量数据
# client.upsert()

# 获取状态
client.get_collection_stats(COLLECTION_NAME)


#%%

# search 数据
res = client.search(
    COLLECTION_NAME,
    [query_vector],
    limit=128,
    output_fields=['subject', 'predicate', 'object', 'owner', 'created', 'embedding_key']
)

df = pd.DataFrame(res[0])
pd.concat([df[['id', 'distance']], pd.json_normalize(df.entity)], axis=1)



#%%

s = "the Ville:Isabella Rodriguez's apartment:main room:bed"
p = 'used'
o = 'scheduled'


res = client.query(
    collection_name=COLLECTION_NAME,
    filter= f'object == "{o}" '
)

pd.DataFrame()

#%%
