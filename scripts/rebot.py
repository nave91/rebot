import re
import fileinput
from pyes import *


def call_es(error):
    error = error[:500]
    conn = ES('ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200')
    error = re.sub('[\W_]+', ' ', error)
    q = QueryStringQuery("ques.snippets:{}".format(error))
    results = conn.search(query=q)
    return results

def store_link(results):
    link = 'https://stackoverflow.com/a/' + str(results[0]['ans']['id'])
    num_results = len(results)
    line_to_write  = link + '\t' + str(num_results) + '\n'
    with open('links.txt', 'a') as f:
        f.write(line_to_write)

def read_stdin():
    for line in fileinput.input():
        results = call_es(line)
        store_link(results)

if __name__ == '__main__':
    read_stdin()

# watch -n 0.1 tail -n 20 links.txt 
