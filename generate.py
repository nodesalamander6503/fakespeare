import re
from collections import Counter, defaultdict
import random
import sys

numtok = int(sys.argv[1])

text = open("trainingdata.txt").read()
text = re.sub(r'[“”]', '"', text)
text = re.sub(r"[‘’]", "'", text)
text = re.sub(r'[^\x00-\x7F]', '', text)
text = [ord(i) for i in text]
m = min(text)
tokens = [chr(i) for i in range(m, max(text))]
text = [i - m for i in text]

def count_pairs(arr):
    pair_count = defaultdict(int)
    for i in range(len(arr) - 1):
        pair_count[(arr[i], arr[i + 1])] += 1
    return pair_count

def most_common_pair(pair_count):
    return max(pair_count, key=pair_count.get)

def replace(pair, replacement, arr):
    result = []
    i = 0
    while i < len(arr):
        if i < len(arr) - 1 and (arr[i], arr[i + 1]) == pair:
            result.append(replacement)
            i += 2
        else:
            result.append(arr[i])
            i += 1
    return result

for i in range(numtok - len(tokens)):
    print("> iteration 1", end = "\r", flush = True)
	pair_count = count_pairs(text)
    if not pair_count: break
    pair = most_common_pair(pair_count)
    text = replace(pair, len(tokens), text)
    tokens.append("".join([tokens[i] for i in pair]))

def generate_markov_grid(arr, numtok):
    size = numtok
    grid = [[0 for _ in range(size)] for _ in range(size)]
    
    for i in range(len(arr) - 1):
        current = arr[i]
        next_value = arr[i + 1]
        grid[current][next_value] += 1
    for i in range(size):
        d = sum(grid[i])
        if d > 0:
            for j in range(size):
                grid[i][j] /= d

    return grid

markov = generate_markov_grid(text, len(tokens))

def generate_random_index(probabilities):
    n = len(probabilities)
    return random.choices(range(n), weights=probabilities, k=1)[0]

sample = []
while len(sample) < 256:
    if len(sample) == 0:
        sample = [random.choice(text)]
        continue
    m = markov[sample[-1]]
    if sum(m) == 0:
        sample = sample[:-1]
        continue
    sample.append(generate_random_index(m))

print("".join([tokens[i] for i in sample]))

print("--- --- ---")

with open("markov.h", "w+") as file:
    file.write("unsigned int num_tokens = " + str(len(tokens)) + ";\n")
    file.write("struct markov_cell markov_table[" + str(len(tokens)) + "] = {\n");
    for i in range(len(tokens)):
        t = "".join(["\\" + oct(ord(c))[2:].zfill(3) for c in tokens[i]])
        file.write("{\"" + t + "\", (float[]) {");
        c = 0 # cumulative
        for p in markov[i]:
            file.write(str(c + p) + ",");
            c += p
        file.write("}},\n");
    file.write("};\n");


