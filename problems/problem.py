class Problem:
    def __init__(self):
        pass

    def get_prompt(self, input: str) -> list[dict[str, str]]:
        raise NotImplementedError

    def get_input(self, index: str|int) -> str:
        raise NotImplementedError

    def save_result(self, name: str, result):
        raise NotImplementedError

    def validate_answer(self, index, answer: str) -> bool:
        raise NotImplementedError

    def evaluate_result(self, name, prompt_type) -> float:
        raise NotImplementedError