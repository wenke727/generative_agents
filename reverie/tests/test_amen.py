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

from persona.memory_structures.associative_memory import AssociativeMemory # type: ignore
from persona.prompt_template.openai_helper import initialize_openai_client # type: ignore
from persona.prompt_template.gpt_structure import get_embedding # type: ignore
from db.vector_db_manager import VectorDB, COLLECTION_NAME, EMBEDDING_DIM

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
query = "sleeping"
query = "Valentine's Day"
emb = get_embedding(query)

#%%
import pandas as pd
import numpy as np

# query = "dinner"
# emb = embeddings(input=query, model="text-embedding-ada-002")
# query_vector = emb.data[0].embedding
# query_vector = get_embedding(query)

vector_db = VectorDB(COLLECTION_NAME, EMBEDDING_DIM)
vector_db.create_collection(replace=False)
client = vector_db.client

persona_name = "Isabella Rodriguez"
df = retrieve_nodes(vector_db, emb, persona_name)
df


#%%
