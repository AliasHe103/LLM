import json
import os

import prompt.llc as prompt

class LLCProblem:
    def __init__(self, prompt_type="standard", shot_type="five_shot", file="data/llc.json"):
        with open(file, "r") as f:
            self.data = json.load(f)
        self.size = len(self.data)
        self.prompt_type = prompt_type
        self.shot_type = shot_type
        self.result_path = None

    def get_prompt(self, input: str):
        if self.prompt_type in ["standard", "cot"] and self.shot_type in ["zero_shot", "five_shot"]:
            base_prompt = getattr(prompt, self.prompt_type + "_prompt")[self.shot_type]
            return [{"role": "system", "content": base_prompt}, {"role": "user", "content": input}]
        else:
            raise ValueError("Invalid prompt_type or shot_type.")

    def get_input(self, index: str|int) -> str:
        return self.data[str(index)]

    def save_result(self, name: str, result):
        filepath = f"{name}({self.shot_type})"
        dir_path = os.path.join("results", "llc", self.prompt_type)
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
        fullname = self.get_input(index) # Matin Luther King Jr
        partial = fullname.split(' ')
        concat = ''.join([part[-1] for part in partial])
        return concat == answer.strip()


    def evaluate_result(self, name, prompt_type="standard"):
        filepath = f"{name}({self.shot_type})"
        dir_path = os.path.join("results", "llc", prompt_type)
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
                print(f"{filepath}: {c_sr / len(result)}")
        sr /= datasize
        return sr
