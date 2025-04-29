standard_prefix = '''You are an arithmetic assistant in reaching 24.
### Rules:
1. Each number must be used exactly as many times as it appears in the input.
2. Four allowed operators: + - * /.
3. Provide the final result in the format: `<equation> = 24`.
'''
cot_prefix = '''You are an arithmetic assistant. Think step-by-step to reach 24.
### Rules:
1. Each number must be used exactly as many times as it appears in the input.
2. Four allowed operators: + - * /.
3. Choose two remaining numbers and one operator to obtain a new number per step.
4. Provide the final result in the format: `<equation> = 24`.
'''

'''
Input1: 4 4 6 8
Answer1: (4 + 8) * (6 - 4) = 24
Input2: 2 9 10 12
Answer2: 2 * 12 * (10 - 9) = 24
Input3: 4 9 10 13
Answer3: (13 - 9) * (10 - 4) = 24
Input4: 1 4 8 8
Answer4: (8 / 4 + 1) * 8 = 24
Input5: 5 5 5 9
Answer5: 5 + 5 + 5 + 9 = 24
'''
standard_five_shot = [
    # example1
    {"role": "user", "content": "4 4 6 8"},
    {"role": "assistant", "content": "(4 + 8) * (6 - 4) = 24"},
    # example2
    {"role": "user", "content": "Input: 2 9 10 12"},
    {"role": "assistant", "content": "2 * 12 * (10 - 9) = 24"},
    # example3
    {"role": "user", "content": "4 9 10 13"},
    {"role": "assistant", "content": "(13 - 9) * (10 - 4) = 24"},
    # example4
    {"role": "user", "content": "1 4 8 8"},
    {"role": "assistant", "content": "(1 + 8 / 4) * 8 = 24"},
    # example5
    {"role": "user", "content": "5 5 5 9"},
    {"role": "assistant", "content": "((5 + 5) + 5) + 9 = 24"}
]
cot_five_shot = [
    # example1
    {"role": "user", "content": "4 4 6 8"},
    {"role": "assistant", "content":
        "4 + 8 = 12 (left: 4 6 12)\n6 - 4 = 2 (left: 2 12)\n2 * 12 = 24 (left: 24)\n(6 - 4) * (4 + 8) = 24"
    },
    # example2
    {"role": "user", "content": "2 9 10 12"},
    {"role": "assistant", "content":
        "12 * 2 = 24 (left: 9 10 24)\n10 - 9 = 1 (left: 1 24)\n24 * 1 = 24 (left: 24)\n(12 * 2) * (10 - 9) = 24"
    },
    # example3
    {"role": "user", "content": "4 9 10 13"},
    {"role": "assistant", "content":
        "13 - 10 = 3 (left: 3 4 9)\n9 - 3 = 6 (left: 4 6)\n4 * 6 = 24 (left: 24)\n4 * (9 - (13 - 10)) = 24"
    },
    #example4
    {"role": "user", "content": "1 4 8 8"},
    {"role": "assistant", "content":
        "8 / 4 = 2 (left: 1 2 8)\n1 + 2 = 3 (left: 3 8)\n3 * 8 = 24 (left: 24)\n(1 + 8 / 4) * 8 = 24"
    },
    # example5
    {"role": "user", "content": "5 5 5 9"},
    {"role": "assistant", "content":
        "5 + 5 = 10 (left: 5 9 10)\n10 + 5 = 15 (left: 9 15)\n15 + 9 = 24 (left: 24)\n((5 + 5) + 5) + 9 = 24"
    }
]

standard_zero_shot = [{"role": "system", "content": standard_prefix}]
standard_five_shot = [{"role": "system", "content": standard_prefix}] + standard_five_shot
cot_zero_shot = [{"role": "system", "content": cot_prefix}]
cot_five_shot = [{"role": "system", "content": cot_prefix}] + cot_five_shot

standard_prompt = {
    "zero_shot": standard_zero_shot,
    "five_shot": standard_five_shot
}
cot_prompt = {
    "zero_shot": cot_zero_shot,
    "five_shot": cot_five_shot
}