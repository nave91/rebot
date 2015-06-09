import json
from xml.etree.cElementTree import iterparse

# get an iterable and turn it into an iterator
context = iter(iterparse("../sample/stackexchange-posts-sample-big.xml", events=("start", "end")))

# get the root element
event, root = next(context)
assert event == "start"

for event, elem in context:
    if event == "end" and elem.tag == "row":
        print json.dumps(elem.items())
        # ... process book elements ...
        root.clear()
        
