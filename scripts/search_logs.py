from pyes import *
import sys

conn = ES('ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200')
q = QueryStringQuery("snippets:INFO")
results = conn.search(query=q)

for r in results:
    sys.stderr.write('.')
    if '[INFO]' in r['snippets']:
        with open('logs.json','a') as f:
            f.write(repr(r)+'\n')
            

