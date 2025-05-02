standard_prefix = '''You are an arithmetic assistant in reaching 24.
### Rules:
1. Use each number exactly as it appears in the input.
2. Only + - * / operators allowed.
3. Provide the final result in the format: `<equation> = 24 END` with NO explanations.
'''
cot_prefix = '''You are an arithmetic assistant. Think step-by-step to reach 24.
### Rules:
1. Use each number exactly as it appears in the input.
2. Only + - * / operators allowed.
3. Choose two remaining numbers and one operator to obtain a new number per step.
4. Provide the final result in the format: `<equation> = 24 END` with NO explanations.
5. Avoid multiple attempts.
'''

standard_five_shot = '''
### Examples:
4 4 6 8
(4 + 8) * (6 - 4) = 24

2 9 10 12
2 * 12 * (10 - 9) = 24

4 9 10 13
(13 - 9) * (10 - 4) = 24

1 4 8 8
(8 / 4 + 1) * 8 = 24

5 5 5 9
5 + 5 + 5 + 9 = 24
'''

cot_five_shot = '''
### Examples:
4 4 6 8
4 + 8 = 12 (left: 4 6 12)\n6 - 4 = 2 (left: 2 12)\n2 * 12 = 24 (left: 24)\n(6 - 4) * (4 + 8) = 24

2 9 10 12
12 * 2 = 24 (left: 9 10 24)\n10 - 9 = 1 (left: 1 24)\n24 * 1 = 24 (left: 24)\n(12 * 2) * (10 - 9) = 24

4 9 10 13
13 - 10 = 3 (left: 3 4 9)\n9 - 3 = 6 (left: 4 6)\n4 * 6 = 24 (left: 24)\n4 * (9 - (13 - 10)) = 24

1 4 8 8
8 / 4 = 2 (left: 1 2 8)\n1 + 2 = 3 (left: 3 8)\n3 * 8 = 24 (left: 24)\n(1 + 8 / 4) * 8 = 24

5 5 5 9
5 + 5 = 10 (left: 5 9 10)\n10 + 5 = 15 (left: 9 15)\n15 + 9 = 24 (left: 24)\n((5 + 5) + 5) + 9 = 24
'''

standard_five_shot = standard_prefix + standard_five_shot
cot_five_shot = cot_prefix + cot_five_shot

standard_prompt = {
    "five_shot": standard_five_shot
}
cot_prompt = {
    "five_shot": cot_five_shot
}