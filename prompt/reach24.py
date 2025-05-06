standard_prefix = '''You are an arithmetic assistant in reaching 24.
### Rules:
1. Use each number exactly as it appears in the input.
2. Only + - * / operators allowed.
3. Provide the final result in the format: `<equation> = 24` with NO explanations.
'''

cot_prefix = '''You are an arithmetic assistant. Think step-by-step to reach 24.
### Rules:
1. Only + - * / operators allowed.
2. Choose two remaining numbers to obtain a new number in each intermediate step.
3. Provide your steps, and the final result in the format: `<equation> = 24` with NO explanations.
4. NEVER do any retries in your response.
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

#tot
possibility_prompt = '''Evaluate if given numbers can reach 24 (sure/likely/impossible)
10 14
10 + 14 = 24
sure
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossible
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
sure
4 9 11
9 + 11 + 4 = 20 + 4 = 24
sure
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
I cannot obtain 24 now, but numbers are within a reasonable range
likely
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
I cannot obtain 24 now, but numbers are within a reasonable range
likely
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 are all too big
impossible
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 are all too small
impossible
For the next input, give evaluation with NO extra explanations(just like the examples above):
'''

last_step_judge_prompt = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Given an input and an answer, give a judgement (sure/impossible) if the answer is correct, i.e. it uses each input exactly once and no other numbers, and reach 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Judge: 
sure
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Judge: 
sure
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Judge: 
sure
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) + 1 = 25
Judge: 
impossible
Input: 2 9 10 12
Answer: 2 * (12 - 10) = 24
Judge: 
impossible
Input: 4 9 10 13
Answer: (13 - 4) * (10 - 9) = 24
Judge: 
impossible
'''

# 3/4=0.75, 0.75 is allowed
propose_prompt = '''Input: 2 8 8 14
Possible next steps:
2 + 8 = 10 (left: 8 10 14)
8 / 2 = 4 (left: 4 8 14)
14 + 2 = 16 (left: 8 8 16)
2 * 8 = 16 (left: 8 14 16)
8 - 2 = 6 (left: 6 8 14)
14 - 8 = 6 (left: 2 6 8)
14 /  2 = 7 (left: 7 8 8)
14 - 2 = 12 (left: 8 8 12)
For the next input, give possible next steps with NO extra explanations(just like the example above):
'''