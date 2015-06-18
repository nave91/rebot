import json
import xml.etree.ElementTree as ET
from bluebook import conf 
from HTMLParser import HTMLParser
from pyspark import SparkContext, SparkConf
            

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
        self.input = '' # line of xml
        self.output = '' # jsoned string

    def load(self, input):
        self.input = input
        raise NotImplementedError

class StackParser(Parser):
    def __init__(self):
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

    def map_xml(self, xml_line):
        self.load(xml_line)
        return self.json_output()

    
class SparkJob:
    def __init__(self):
        self.server = conf.HDFS_FQDN
        self.conf = SparkConf()

class StackSparkJob(SparkJob):
    def __init__(self):
        SparkJob.__init__(self)
        self.xml_folder_name = conf.STACKEXCHANGE_XML_FOLDER_NAME
        self.xml_file_name = conf.STACKEXCHANGE_XML_FILE_NAME
        self.xml_file_address = "hdfs://" + self.server + "/" +\
                            self.xml_folder_name + self.xml_file_name
        
        self.json_folder_name = conf.STACKEXCHANGE_JSON_FOLDER_NAME
        self.json_folder_address = "hdfs://" + self.server + "/" +\
                                   self.json_folder_name

        self.conf.setAppName(self.__class__.__name__)
        self.spark_context = SparkContext(conf=self.conf)
        
        self.file = self.spark_context.textFile(self.xml_file_address)

        self.stack_parser = StackParser()
        

    def map(self):
        self.lines = self.file.map(lambda line: self.stack_parser.map_xml(line))

    def reduce(self):
        self.lines.saveAsTextFile(self.json_folder_address)

    def run(self):
        self.map()
        self.reduce()

if __name__ == '__main__':
    
    ssj = StackSparkJob()
    ssj.run()
    
