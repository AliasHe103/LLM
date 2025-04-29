#%% md
# # Reach24 Problem
#%%
import os

from agent import Agent

key = os.getenv("DASHSCOPE_API_KEY")
url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
name = "qwen-max"
agent = Agent(
    key,
    url,
    name
)
#%%
sr = agent.eval(
    problem_type="reach24",
    prompt_type="cot",
    shot_type="five_shot"
)

print(f"{name}, SR: {sr}")