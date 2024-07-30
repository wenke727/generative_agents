#%%
import pandas as pd

fn = "../environment/frontend_server/storage/July1_the_ville_isabella_maria_klaus-step-3-21/personas/Isabella Rodriguez/bootstrap_memory/associative_memory/nodes.json"
df = pd.read_json(fn).T
df

# %%
