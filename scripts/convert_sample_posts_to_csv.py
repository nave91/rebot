from xml.etree.cElementTree import iterparse
import json
import sys

# get an iterable and turn it into an iterator
context = iter(iterparse("../sample/stackexchange-posts-sample-big.xml", events=("start", "end")))

# get the root element
event, root = next(context)
assert event == "start"
rows = []
header = ['Id', 'PostTypeId', 'Score']
answer = 'AcceptedAnswerId'
for event, elem in context:
    row = ""
    if event == "end" and elem.tag == "row":
        d = dict(elem.items())
        for h in header:
            # item = d[h].encode('utf-8')
            # item = item.replace('(?>\P{M}\p{M}*)+','')
            # item = item.replace('\n', ' ')
            # item = item.replace('\"', ' ')
            # item = item.replace('\t', ' ')
            # item = item.replace(' +',' ')
            # row += "\""+item +"\""+", "
            row += str(d[h]) + ','
        if answer in d.keys():
            row += str(d[answer]) + ','
        else:
            row += 'NULL' + ','
        root.clear()
        rows.append(row[:-1])
header.append(answer)
print ','.join(header)
for r in rows: print r
