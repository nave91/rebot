import json
import xml.etree.ElementTree as ET
from bluebook import conf 
from HTMLParser import HTMLParser
            

class StackPostsBodyParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.recording = 0
        self.snippets = ''

    def handle_starttag(self, tag, attrs):
        if tag != 'code':
            return
        if self.recording:
            self.recording += 1
        self.recording = 1
    
    def handle_endtag(self, tag):
        if tag != 'code':
            return
        if self.recording:
            self.recording -= 1
    
    def handle_data(self, data):
        if self.recording:
            self.snippets += "<snippet>" + data + "</snippet>"

class Parser:
    def __init__(self):
        self.type = 'parser_generic'
        self.input = '' # line of xml
        self.output = '' # jsoned string

    def load(self, input):
        self.input = input
        raise NotImplementedError

class StackParser(Parser):
    def __init__(self):
        self.type = 'parser_stackexchange'
        self.body_parser = StackPostsBodyParser()
        self.header = {
            'id': 'Id',
            'posttypeid': 'PostTypeId',
            'score': 'Score',
            'answer': 'AcceptedAnswerId',
            'body': 'Body',
            'snippets': 'snippets'
        }

    def load(self, input):
        self.input = input
        if self.input[-2] == '/':
            row = ET.fromstring(line.encode('UTF-8'))
            self.output = {}
            for header, value in self.input.attrib.items():
                self.output[header] = value
            parser= self.body_parser.feed(self.output['Body'])
            self.output['snippets'] = parser.snippets
            return self.output

    def json_output(self):
        out = {}
        for actual, given in self.header.items():
            if given == 'AcceptedAnswerId':
                if given in self.output.keys():
                    out[actual] = self.output[given]
                else:
                    out[actual] = 'NULL'
                continue
            out[actual] = row[given]
        return json.dumps(out)

    
class SparkJob:
    def __init__(self):
        pass

