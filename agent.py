from openai import OpenAI

from problems.reach24 import Reach24Problem


class Agent:
    def __init__(self, key, url, name):
        self.llm = OpenAI(
            api_key=key,
            base_url=url
        )
        self.name = name
        self.history = []
        self.problem = None

    def predict(self, messages):
        try:
            self.history += messages[-1]
            response = self.llm.chat.completions.create(
                model=self.name,
                messages=messages,
                temperature=0,
            )

            self.history.append({"role": "assistant", "content": response})
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(e)
            return None

    def eval(self, problem_type="reach24",
                 prompt_type="standard", shot_type="zero_shot"):
        if problem_type == "reach24":
            self.problem = Reach24Problem(prompt_type, shot_type)
        else:
            raise ValueError("Invalid problem_type.")

        result = {}
        for index in range(1312, 1362):
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
        sr = self.problem.evaluate_result(prompt_type)
        return sr