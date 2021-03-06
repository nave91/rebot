import json
import xml.etree.ElementTree as ET
from bluebook import conf as bluebook_conf
from HTMLParser import HTMLParser
from pyspark import SparkContext, SparkConf
            

def jsoner(dic):
    return json.dumps(dic)

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
        self.output = {}
        if self.input[-2] == '/':
            row = ET.fromstring(self.input.encode('UTF-8'))
            for header, value in row.items():
                self.output[header] = value
            self.body_parser.feed(self.output['Body'])
            self.output['snippets'] = self.body_parser.snippets
            return self.output

    def format(self):
        if self.output == {}:
            return {}
        out = {}
        for _i, _xml in self.header.items():
            if _xml == 'AcceptedAnswerId':
                if _xml in self.output.keys():
                    out[_i] = self.output[_xml]
                else:
                    out[_i] = 'NULL'
                continue
            out[_i] = self.output[_xml]
        self.output = out
        return self.output
    
    def map_xml(self, xml_line):
        self.load(xml_line)
        return self.format()

    
class SparkJob:
    def __init__(self):
        #self.server = conf.HDFS_FQDN
        pass

class StackSparkJob(SparkJob):
    def __init__(self):
        SparkJob.__init__(self)
        

        

    def map(self):
        server = bluebook_conf.HDFS_FQDN
        xml_file_address = "hdfs://" + server + "/" +\
                                bluebook_conf.STACKEXCHANGE_XML_FOLDER_NAME +\
                                bluebook_conf.STACKEXCHANGE_XML_FILE_NAME
                         
        json_ques_folder_address = "hdfs://" + server + "/" +\
                                        bluebook_conf.STACKEXCHANGE_JSON_QUES_FOLDER_NAME
        json_ans_folder_address = "hdfs://" + server + "/" +\
                                        bluebook_conf.STACKEXCHANGE_JSON_ANS_FOLDER_NAME
        
        stack_parser = StackParser()
        conf = SparkConf().setAppName('test')
        spark_context = SparkContext(conf=conf)
        file = spark_context.textFile(xml_file_address)
        ques = file.map(stack_parser.map_xml)\
            .filter(lambda dic: 'posttypeid' in dic.keys())\
            .filter(lambda dic: dic['posttypeid'] == '1')\
            .map(lambda d: jsoner(d))
        ques.saveAsTextFile(json_ques_folder_address)
        # def save(self):
        
        # self.filtered_dict = self.dics.filter(lambda dic: 'posttypeid' in dic.keys())
        
        # self.ques_dict = self.filtered_dict.filter(lambda dic: dic['posttypeid'] == '1')
        # self.ques_json = self.ques_dict.map(lambda d: jsoner(d))

        # self.ans_dict = self.filtered_dict.filter(lambda dic: dic['posttypeid'] == '2')
        # self.ans_json = self.ans_dict.map(lambda d: jsoner(d))

        # self.ques_json.saveAsTextFile(self.json_ques_folder_address)
        # self.ans_json.saveAsTextFile(self.json_ans_folder_address)


    def run(self):
        self.map()
        self.save()

if __name__ == '__main__':
    
    # ssj = StackSparkJob()
    # ssj.run()
    server = bluebook_conf.HDFS_FQDN
    xml_file_address = "hdfs://" + server + "/" +\
                       bluebook_conf.STACKEXCHANGE_XML_FOLDER_NAME +\
                       bluebook_conf.STACKEXCHANGE_XML_FILE_NAME
    
    json_ques_folder_address = "hdfs://" + server + "/" +\
                               bluebook_conf.STACKEXCHANGE_JSON_QUES_FOLDER_NAME
    json_ans_folder_address = "hdfs://" + server + "/" +\
                              bluebook_conf.STACKEXCHANGE_JSON_ANS_FOLDER_NAME
    
    stack_parser = StackParser()
    conf = SparkConf().setAppName('test')
    spark_context = SparkContext(conf=conf)
    file = spark_context.textFile(xml_file_address)
    ques = file.map(stack_parser.map_xml)\
               .filter(lambda dic: 'posttypeid' in dic.keys())\
               .filter(lambda dic: dic['posttypeid'] == '1')\
               .map(lambda d: jsoner(d))
    ques.saveAsTextFile(json_ques_folder_address)
        
