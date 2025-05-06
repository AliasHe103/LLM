import itertools

import openai
from openai import OpenAI
from agent import Agent
import backoff

from prompt.reach24 import last_step_judge_prompt, input_judge_prompt, propose_prompt

MAX_STEPS = 20
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
        self.judge_cache = None

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
    def get_current_numbers(self, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        return last_line.split('left: ')[-1].split(')')[0]

    def get_judge_prompt(self, input: str, state: str) -> tuple[str, str]:
        # system, user
        last_line = state.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            return last_step_judge_prompt, f"Input: {input}\nAnswer: {ans}\nJudge:"
        return input_judge_prompt, input

    def value_outputs_unwrap(self, input: str, state: str, judge_results: list) -> float:
        if len(state.strip().split('\n')) == 4 and 'answer' not in state.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in judge_results]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value

    # sure/likely/impossible
    def get_judge_result(self, input, prompt, n_evaluate_sample, cache_value=True):
        judge_prompt, user_input = self.get_judge_prompt(input, prompt)
        if cache_value and judge_prompt in self.judge_cache:
            return self.judge_cache[judge_prompt]
        judge_messages = [
            {"role": "system", "content": judge_prompt},
            {"role": "system", "content": user_input},
        ]
        judge_ouput = self.tree_thoughts(judge_messages, n=n_evaluate_sample)
        judge_result = self.value_outputs_unwrap(input, prompt, judge_ouput)
        if cache_value:
            self.judge_cache[judge_prompt] = judge_result
        return judge_result

    def get_judge_results(self, x, ys, n_evaluate_sample, cache_value=True):
        judge_results = []
        local_value_cache = {}
        for y in ys:  # each partial output
            if y in local_value_cache:  # avoid duplicate candidates
                judge_result = 0
            else:
                judge_result = self.get_judge_result(x, y, n_evaluate_sample, cache_value=cache_value)
                local_value_cache[y] = judge_result
            judge_results.append(judge_result)
        return judge_results

    # propose in reach24
    def get_propose_prompt(self, input: str, state: str) -> str:
        current_numbers = self.get_current_numbers(state if state else input)
        if current_numbers == '24':
            return 'Steps:'
        else:
            return propose_prompt

    # propose possible next steps
    def get_proposals(self, input: str, state: str):
        propose_prompt = self.get_propose_prompt(input, state)
        propose_messages = [
            {"role": "system", "content": propose_prompt},
            {"role": "user", "content": input},
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
            # value
            judges = self.get_judge_results(input, new_states, self.problem.n_evaluate_sample)
            #greedy, n_select_sample=5
            selected_ids = sorted(ids, key=lambda x: judges[x], reverse=True)[:5]
            selected_new_states = [new_states[selected_id] for selected_id in selected_ids]
            states = selected_new_states
        return states