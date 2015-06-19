import sys
import random
import ast
import time
from pyes import *
import re, string
    
def get_lines(f):
    with open(f, 'r') as f:
        lines = f.readlines()
    return lines

def call_es(error):
    error = error[:10]
    conn = ES('ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200')
    print error
    error = re.sub('[\W_]+', '', error)
    q = QueryStringQuery("ques.snippets:{}".format(error))
    results = conn.search(query=q)
    if len(results) > 0:
        print type(results), len(results)
        for r in results:
            print r[0]

def call_rebot():
    time.sleep(1)
    error = out[7:-8]
    #sys.stderr.write(error)
    #print error
    print "."
    call_es(error)
    
if __name__ == '__main__':
    lines = get_lines('logs.json')
    _i =0 
    while _i<10:
        i = random.randint(0,len(lines)-1)
        line = ast.literal_eval(lines[i])
        out = line['snippets']
        if '[ERROR]' not in out:
            call_rebot()
        print _i
        _i += 1
