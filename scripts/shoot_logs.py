import sys
def get_lines(f):
    with open(f, 'r') as f:
        lines = f.readlines()
    return lines

lines = get_lines('logs.json')

print len(lines)
