from xml.etree.cElementTree import iterparse
import json
import sys

# get an iterable and turn it into an iterator
context = iter(iterparse("../sample/stackexchange-posts-sample-big.xml", events=("start", "end")))

# get the root element
event, root = next(context)
assert event == "start"
rows = []
header = ['Id', 'PostTypeId', 'Score', 'Body']
for event, elem in context:
    row = ""
    if event == "end" and elem.tag == "row":
        d = dict(elem.items())
        for h in header:
            row += "\""+str(d[h]).replace('(\n|\")',' ') +"\""+", "
        root.clear()
    rows.append(row)
print ','.join(header)
for r in rows: print r
