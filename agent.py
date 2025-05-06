from openai import OpenAI

from problems.arithmetic.reach24 import Reach24Problem
from problems.symbolic.llc import LLCProblem


class Agent:
    def __init__(self, key, url, name):
        self.llm = OpenAI(
            api_key=key,
            base_url=url,
        )
        self.name = name
        self.history = []
        self.problem = None

    def predict(self, messages: list):
        try:
            # self.history += messages[-1]
            response = self.llm.chat.completions.create(
                model=self.name,
                messages=messages,
                temperature=0.3,
                stop=["END", "\n\n"]
            )

            # self.history.append({"role": "assistant", "content": response})
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_problem(self, problem_type, prompt_type, shot_type):
        if problem_type == "reach24":
            return Reach24Problem(prompt_type, shot_type)
        elif problem_type == "llc":
            return LLCProblem(prompt_type, shot_type)
        else:
            raise ValueError("Invalid problem_type.")

    @staticmethod
    def get_task_index(self, problem_type) -> tuple[int, int]:
        """
        range(start_id, end_id)
        """
        if problem_type == "reach24":
            return 1312, 1362
        elif problem_type == "llc":
            return 1, 100
        else:
            raise ValueError("Invalid problem_type.")

    def eval(self, run=False, problem_type="reach24",
                 prompt_type="standard", shot_type="zero_shot"):
        print(f"[Problem: {problem_type}, Model: {self.name}, Method: {prompt_type}, Shot: {shot_type}]")
        self.problem = self.get_problem(problem_type, prompt_type, shot_type)
        result = {}
        try:
            if run:
                start, end = self.get_task_index(problem_type)
                for index in range(start, end):
                    print(f"Evaluating task{index}...")
                    input = self.problem.get_input(index)
                    prompt = self.problem.get_prompt(input)
                    try:
                        answer = self.predict(prompt)
                        result[index] = answer
                    except Exception as e:
                        print(e)
                        result[index] = "{}".format(e)
                        continue
                self.problem.save_result(self.name, result)
            sr = self.problem.evaluate_result(self.name, prompt_type)
            return sr
        except KeyboardInterrupt:
            print(f"Stop evaluating for an unexpected error.")
            if result:
                self.problem.save_result(self.name, result)
                raise
            return None