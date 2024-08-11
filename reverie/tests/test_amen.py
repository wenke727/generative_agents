#%%
import sys
sys.path.append('../backend_server')

import glob
import json
import pandas as pd
from pathlib import Path
from loguru import logger

from persona.memory_structures.associative_memory import AssociativeMemory

"""TODO
2. 测试 retrieve 的效果

"""

#%%
folder = Path("../../environment/frontend_server/storage/July1_the_ville_isabella_maria_klaus-step-3-21/personas")
persona = "Isabella Rodriguez"
ass_mem_folder = folder / persona / "bootstrap_memory/associative_memory"

a_men = AssociativeMemory(str(ass_mem_folder))
a_men

logger.debug(a_men.get_summarized_latest_events(10))
logger.debug(f"get_str_seq_events: \n{a_men.get_str_seq_events()}")
logger.debug(f"get_str_seq_thoughts: \n{a_men.get_str_seq_thoughts()}")
logger.debug(f"get_str_seq_chats: \n{a_men.get_str_seq_chats()}")

#%%
#! spo 关键字检索
s = 'isabella rodriguez'
s = "the Ville:Isabella Rodriguez's apartment:main room:bed"
p = 'used'
o = 'bed'

a_men.retrieve_relevant_thoughts(s, p, o)
a_men.retrieve_relevant_events(s, p, o)


#%%
# nodes
df_nodes = pd.read_json(ass_mem_folder / "nodes.json").T
df_nodes

#%%
# embeddings
embed = json.load(open(ass_mem_folder / "embeddings.json"))
df_embeddings = pd.DataFrame({"text": embed.keys(), 'embeddings': embed.values()})
df_embeddings


# %%
