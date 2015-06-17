import sys
import random
import ast
import time

def get_lines(f):
    with open(f, 'r') as f:
        lines = f.readlines()
    return lines

lines = get_lines('logs.json')
while 1:
    i = random.randint(0,len(lines)-1)
    line = ast.literal_eval(lines[i])
    out = line['snippets']
    if '[ERROR]' not in out:
        time.sleep(1)
        print out[7:-8]
