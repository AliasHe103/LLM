import json
import os
import re
from collections import Counter

import pandas as pd

import prompt.reach24 as prompt
from problems.problem import Problem

ALLOWED_CHARS = set("0123456789+-*/()=")
EXP_PATTERN = re.compile(r'-?\d+')
REPEAT_OP = re.compile(r'[+\-*/]{2,}')

class Reach24Problem(Problem):
    def __init__(self, prompt_type="standard", shot_type="five_shot", file="data/reach24.csv"):
        super().__init__()
        self.data = list(pd.read_csv(file)['Puzzles'])
        self.size = len(self.data)
        self.prompt_type = prompt_type
        self.shot_type = shot_type
        self.result_path = None
        self.value_cache = {}

    def get_prompt(self, input: str):
        if self.prompt_type in ["standard", "cot"] and self.shot_type in ["zero_shot", "five_shot"]:
            base_prompt = getattr(prompt, self.prompt_type + "_prompt")[self.shot_type]
            return [{"role": "system", "content": base_prompt}, {"role": "user", "content": input}]
        else:
            raise ValueError("Invalid prompt_type or shot_type.")

    def get_input(self, index: str|int) -> str:
        return self.data[int(index)]

    def save_result(self, name: str, result):
        filepath = f"{name}({self.shot_type})"
        dir_path = os.path.join("results", "reach24", self.prompt_type)
        os.makedirs(dir_path, exist_ok=True)
        max_file_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith(filepath) and filename.endswith(".json"):
                try:
                    file_index = filename[len(filepath):-5]
                    current_index = int(file_index) if file_index else 1
                    max_file_index = max(max_file_index, current_index)
                except ValueError:
                    continue

        filepath = os.path.join(dir_path, f"{filepath}{max_file_index + 1}.json")
        self.result_path = filepath
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    def validate_answer(self, index, answer: str) -> bool:
        answer = ''.join(ch for ch in answer if ch in ALLOWED_CHARS)
        input_nums = list(map(int, self.get_input(index).split()))
        input_counter = Counter(input_nums)
        # repeated operator
        exp = answer.split('=')[0]
        if REPEAT_OP.search(exp):
            return False
        answer_nums = [abs(int(num)) for num in EXP_PATTERN.findall(exp)]
        answer_counter = Counter(answer_nums)
        # size, times of numbers
        if input_counter != answer_counter:
            return False
        # equal
        try:
            result = eval(exp, {'__builtins__': None}, {})
        except ZeroDivisionError:
            return False
        return abs(result - 24) < 1e-6


    def evaluate_result(self, name, prompt_type="standard"):
        filepath = f"{name}({self.shot_type})"
        dir_path = os.path.join("results", "reach24", prompt_type)
        matching_files = []
        for filename in os.listdir(dir_path):
            if filename.startswith(filepath) and filename.endswith(".json"):
                matching_files.append(os.path.join(dir_path, filename))
        if not matching_files:
            print(f"No matching files found for {filepath}*.json.")
            return 0.0
        sr = 0.0
        datasize = 0
        matching_files.sort()
        for filepath in matching_files:
            with open(filepath, "r", encoding="utf-8") as f:
                result = json.load(f)
                datasize += len(result)
                c_sr = 0.0
                for index, ans in result.items():
                    if prompt_type == "cot":
                        ans = ans.split('\n')[-1]
                    if self.validate_answer(index, ans):
                        sr += 1
                        c_sr += 1
                print(f"{filepath}: {(c_sr / len(result)):.3%}")
        sr /= datasize
        return sr