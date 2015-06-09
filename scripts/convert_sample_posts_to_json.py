from xml.etree.cElementTree import iterparse
import json

# get an iterable and turn it into an iterator
context = iter(iterparse("../sample/stackexchange-posts-sample-big.xml", events=("start", "end")))

# get the root element
event, root = next(context)
assert event == "start"

out = '{ '

for event, elem in context:
    if event == "end" and elem.tag == "row":
        d = dict(elem.items())
        out += d['Id'] + ': ' + str(d) + ',' 
        # ... process book elements ...
        root.clear()

print out[:-1] + '}'
