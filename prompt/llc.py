standard_prefix = '''You are a text processing assistant for last letter concatenation.
### Rules:
1. Concatenate the last letters in original word order.
2. Provide the final result in the format: `<concatenated_letters>` with NO explanations.
'''

cot_prefix = '''You are a text processing assistant. Think step-by-step to concatenate last letters.
### Rules:
1. Find the last letters in each intermediate step.
2. Concatenate the last letters in your answer.
3. Provide your steps, and the final result in the format: `<concatenated_letters>` with NO explanations.
'''

standard_five_shot = '''
### Examples:
Amy Brown
yn

John Fitzgerald Kennedy
ndy

Martin Luther King Jr
nrgr

Marie Curie
ee

William Shakespeare
me
'''

cot_five_shot = '''
### Examples:
Amy Brown
Amy: y (collected: y)\nBrown: n (collected: yn)\nyn

John Fitzgerald Kennedy
John: n (collected: n)\nFitzgerald: d (collected: nd)\nKennedy: y (collected: ndy)\nndy

Martin Luther King Jr
Martin: n (collected: n)\nLuther: r (collected: nr)\nKing: g (collected: nrg)\nJr: r (collected: nrgr)\nnrgr

Marie Curie
Marie: e (collected: e)\nCurie: e (collected: ee)\nee

William Shakespeare
William: m (collected: m)\nShakespeare: e (collected: me)\nme
'''

standard_five_shot = standard_prefix + standard_five_shot
cot_five_shot = cot_prefix + cot_five_shot

standard_prompt = {
    "five_shot": standard_five_shot
}

cot_prompt = {
    "five_shot": cot_five_shot
}