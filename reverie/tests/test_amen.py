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
2. 测试 retrieve 的效果

"""

#%%
def load_memory_to_points(folder):
    folder = Path(folder) / "bootstrap_memory/associative_memory"

    # nodes
    df_nodes = pd.read_json(folder / "nodes.json").T
    text_2_embedding = json.load(open(folder / "embeddings.json"))
    embs = df_nodes.embedding_key.map(lambda x: text_2_embedding.get(x, []))

    points = [
        {'id': int(id.split("_")[-1]), 'payload': payload, 'vector': emb}
            for (id, payload), emb in
                zip(df_nodes.to_dict(orient='index').items(), embs)
    ]

    try:
        from qdrant_client.http.models import PointStruct
        points = [PointStruct(**p) for p in points]
    except:
        pass

    return points

def read_memory(folder, person):
    ass_mem_folder = folder / person / "bootstrap_memory/associative_memory"

    a_men = AssociativeMemory(str(ass_mem_folder))

    logger.debug(a_men.get_summarized_latest_events(10))
    logger.debug(f"get_str_seq_events: \n{a_men.get_str_seq_events()}")
    logger.debug(f"get_str_seq_thoughts: \n{a_men.get_str_seq_thoughts()}")
    logger.debug(f"get_str_seq_chats: \n{a_men.get_str_seq_chats()}")

    return a_men


folder = Path("../../environment/frontend_server/storage/July1_the_ville_isabella_maria_klaus-step-3-21/personas")
persona = "Isabella Rodriguez"
a_men = read_memory(folder, persona)

#%%
#! spo 关键字检索
s = 'isabella rodriguez'
s = "the Ville:Isabella Rodriguez's apartment:main room:bed"
p = 'used'
o = 'bed'

a_men.retrieve_relevant_thoughts(s, p, o)
a_men.retrieve_relevant_events(s, p, o)


#%%
points = load_memory_to_points(folder / persona)
#%%
points[4].payload


#%%

qdrant_client_cfg = get_qdrant_client_cfg()
collection_name = os.environ.get("ASSOCIATE_COLLECTION", "associate_memory")
embedding_dim = os.environ.get("EMBEDDING_DIM", 1536)

db_client = VectoreDB(qdrant_client_cfg, collection_name, embedding_dim)
db_client

#%%
db_client.add(points)

# %%
client, chat, embeddings = initialize_openai_client()


# %%
query = "sleeping"
emb = embeddings(input=query, model="text-embedding-ada-002")
query_vector = emb.data[0].embedding

res = db_client.search(query_vector=query_vector, limit=8)


# %%
query = "have a lunch"
emb = embeddings(input=query, model="text-embedding-ada-002")
query_vector = emb.data[0].embedding

res = db_client.search(query_vector=query_vector, limit=8)


# %%
query = "Valentine's Day"
emb = embeddings(input=query, model="text-embedding-ada-002")
query_vector = emb.data[0].embedding

res = db_client.search(query_vector=query_vector, limit=8)


# %%
pd.DataFrame([{'id': i.id, **i.payload, 'score': i.score} for i in res])[['embedding_key', 'score']]


# %%
