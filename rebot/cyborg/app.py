import json
import xml.etree.ElementTree as ET
from bluebook import conf as bluebook_conf 
from HTMLParser import HTMLParser
from pyspark import SparkContext, SparkConf
            
def jsoner(dic):
    return json.dumps(dic)

def stackexchange_parser(xml_row):
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

    body_parser = StackPostsBodyParser()
    output = {}
    if xml_row[-2] == '/':
        row = ET.fromstring(xml_row.encode('UTF-8'))
        for header, value in row.items():
            output[header] = value
        body_parser.feed(output['Body'])
        output['snippets'] = body_parser.snippets
    return output


def stackexchange_formatter(dic):
    if dic == {}:
        return {}
    out = {}
    for _i, _xml in bluebook_conf.STACKEXCHANGE_HEADER_MAP.items():
        if _xml == 'AcceptedAnswerId':
            if _xml in dic.keys():
                out[_i] = dic[_xml]
            else:
                out[_i] = 'NULL'
            continue
        out[_i] = dic[_xml]
    return out
    
def stackexchange_mapper(xml_line):
    dic = stackexchange_parser(xml_line)
    return stackexchange_formatter(dic)


if __name__ == '__main__':
    
    server = bluebook_conf.HDFS_FQDN
    conf = SparkConf()

    xml_file_address = "hdfs://" + server + "/" +\
                       bluebook_conf.STACKEXCHANGE_XML_FOLDER_NAME +\
                       bluebook_conf.STACKEXCHANGE_XML_FILE_NAME
                         
    json_ques_folder_address = "hdfs://" + server + "/" +\
                               bluebook_conf.STACKEXCHANGE_JSON_QUES_FOLDER_NAME
    json_ans_folder_address = "hdfs://" + server + "/" +\
                              bluebook_conf.STACKEXCHANGE_JSON_ANS_FOLDER_NAME
        
    conf.setAppName('test')
    spark_context = SparkContext(conf=conf)
        
    file = spark_context.textFile(xml_file_address)
    ques = file.map(stackexchange_mapper)\
               .filter(lambda dic: 'posttypeid' in dic.keys())\
               .filter(lambda dic: dic['posttypeid'] == '1')\
               .map(lambda d: jsoner(d))
    ans = file.map(stackexchange_mapper)\
               .filter(lambda dic: 'posttypeid' in dic.keys())\
               .filter(lambda dic: dic['posttypeid'] == '2')\
               .map(lambda d: jsoner(d))
    ques.saveAsTextFile(json_ques_folder_address)
    ans.saveAsTextFile(json_ans_folder_address)
        
    
