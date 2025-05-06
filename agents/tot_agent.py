import itertools

import openai
from openai import OpenAI
from agents.agent import Agent
import backoff

from problems.arithmetic.reach24 import Reach24Problem
from problems.symbolic.llc import LLCProblem
from prompt.reach24 import last_step_judge_prompt, possibility_prompt, propose_prompt

MAX_STEPS = 20
N_EVALUATE_SAMPLE = 3
N_SELECT_SAMPLE = 5
class ToTAgent(Agent):
    def __init__(self, key, url, name):
        super().__init__(key, url, name)
        self.llm = OpenAI(
            api_key=key,
            base_url=url,
        )
        self.name = name
        self.history = []
        self.problem = None
        self.possibility_cache = {}

    @backoff.on_exception(backoff.expo, openai.OpenAIError, max_tries=3)
    def predict(self, messages: list):
        try:
            response = self.llm.chat.completions.create(
                model=self.name,
                messages=messages,
                temperature=0.3,
                max_tokens=1000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_problem(problem_type, prompt_type, shot_type):
        if problem_type == "reach24":
            return Reach24Problem(prompt_type, shot_type)
        elif problem_type == "llc":
            return LLCProblem(prompt_type, shot_type)
        else:
            raise ValueError("Invalid problem_type.")

    def tree_thoughts(self, messages: list, n=1) -> list:
        outputs = []
        while n > 0:
            steps = min(n, MAX_STEPS)
            n -= steps
            try:
                for step in range(steps):
                    response = self.predict(messages)
                    outputs.append(response)
            except Exception as e:
                print(f"API call failed: {e}")
                outputs.append(f"API call failed: {e}")
        return outputs

    # tot
    @staticmethod
    def get_current_numbers(state: str) -> str:
        last_line = state.strip().split('\n')[-1]
        return last_line.split('left: ')[-1].split(')')[0]

    def get_possibility_prompt(self, input: str, state: str) -> str:
        last_line = state.strip().split('\n')[-1]
        left_numbers = self.get_current_numbers(last_line)
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            return last_step_judge_prompt + f"Input: {input}\nAnswer: {ans}\nJudge:"
        return possibility_prompt + left_numbers

    # judge possibility
    @staticmethod
    def get_possibility_score(state: str, possible_paths: list) -> float:
        if len(state.strip().split('\n')) == 4 and 'answer' not in state.lower():
            return 0
        # impossible/likely/sure
        paths = [_.split('\n')[-1] for _ in possible_paths]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}
        value = sum(value * paths.count(name) for name, value in value_map.items())
        return value

    # sure/likely/impossible->value
    def get_possibility_value(self, input, state, n_evaluate_sample, cache_value=True):
        possibility_prompt = self.get_possibility_prompt(input, state)
        if cache_value and possibility_prompt in self.possibility_cache:
            return self.possibility_cache[possibility_prompt]
        messages = [
            {"role": "user", "content": possibility_prompt},
        ]
        # n judges
        possibility = self.tree_thoughts(messages, n=n_evaluate_sample)
        value = self.get_possibility_score(state, possibility)
        if cache_value:
            self.possibility_cache[possibility_prompt] = value
        return value

    def get_possibility_values(self, input, states, n_evaluate_sample, cache_value=True):
        values = []
        local_value_cache = {}
        for state in states:  # each partial output
            if state in local_value_cache:  # avoid duplicate candidates
                value = 0
            else:
                value = self.get_possibility_value(input, state, n_evaluate_sample, cache_value=cache_value)
                local_value_cache[state] = value
            values.append(value)
        return values

    # propose in reach24
    def get_propose_prompt(self, input: str, state: str) -> str:
        current_numbers = self.get_current_numbers(state if state else input)
        if current_numbers == '24':
            return 'Steps:'
        else:
            return propose_prompt + current_numbers

    # propose possible next steps
    def get_proposals(self, input: str, state: str):
        propose_prompt = self.get_propose_prompt(input, state)
        propose_messages = [
            {"role": "user", "content": propose_prompt},
        ]
        proposals = self.tree_thoughts(propose_messages, n=1)[0].split('\n')
        return [state + proposal + '\n' for proposal in proposals]

    def solve(self, id: int|str):
        if not self.problem:
            raise ValueError("Please set problem first.")
        input = self.problem.get_input(id)
        states = ['']
        thought_depth = 4
        for step in range(thought_depth):
            new_states = [self.get_proposals(input, state) for state in states]
            new_states = list(itertools.chain(*new_states))
            ids = list(range(len(new_states)))
            # get value/score
            values = self.get_possibility_values(input, new_states, N_EVALUATE_SAMPLE)
            #greedy, n_select_sample=5
            selected_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:5]
            selected_new_states = [new_states[selected_id] for selected_id in selected_ids]
            states = selected_new_states
        return states

    def eval(self, run=False, problem_type="reach24",
                 prompt_type="standard", shot_type="zero_shot"):
        print(f"[Problem: {problem_type}, Model: {self.name}, Method: {prompt_type}, Shot: {shot_type}]")
        self.problem = self.get_problem(problem_type, prompt_type, shot_type)
        # 1360->6/(1-3/4)=24
        self.solve(1360)