import re
import fileinput
import requests
from pyes import *


# def call_es(error):
#     error = error[:500]
#     conn = ES('ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200')
#     error = re.sub('[\W_]+', ' ', error)
#     q = QueryStringQuery("ques.snippets:{}".format(error))
#     results = conn.search(query=q)
#     return results

def call_server(error):
    server = 'http://ec2-52-8-219-37.us-west-1.compute.amazonaws.com/api/v1/error'
    # server = 'http://localhost:5000/api/v1/error'
    params = {
        'error_log': error
    }
    result = {}
    r = requests.post(server, params)
    if r.status_code == 200:
        result['answer_link'] = r.json()['answer_link']
        result['num_results'] = r.json()['num_results']
    return result

def store_link(result):
    link = result['answer_link']
    num_results = result['num_results']
    line_to_write  = link + '\t' + str(num_results) + '\n'
    with open('links.txt', 'a') as f:
        f.write(line_to_write)

def read_stdin():
    for line in fileinput.input():
        result = call_server(line)
        store_link(result)

if __name__ == '__main__':
    read_stdin()

# watch -n 0.1 tail -n 20 links.txt 
