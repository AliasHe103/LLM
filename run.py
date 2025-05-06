#%% md
# # Reach24 Problem
#%%
import os

from agents.agent import Agent

key = os.getenv("DASHSCOPE_API_KEY")
url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
name = "deepseek-v3"
agent = Agent(
    key,
    url,
    name
)
#%%
sr = agent.eval(
    problem_type="reach24",
    prompt_type="cot",
    shot_type="five_shot",
    run=True
)

print(f"{name}, SR: {sr}")