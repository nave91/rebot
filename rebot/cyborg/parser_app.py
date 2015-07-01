import json
import xml.etree.ElementTree as ET
from bluebook import conf as bluebook_conf 
from HTMLParser import HTMLParser
from pyspark import SparkContext, SparkConf


header = bluebook_conf.STACKEXCHANGE_HEADER_MAP
            
def jsoner(dic):
    return json.dumps(dic)

def stackexchange_xml_parser(xml_row):
    """
    Parses stackexchange type xml file into json.
    Also finds code snippets using tag <code> and stores it in a 
    new index.
    """
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
        output['sourcetype'] = 'stackoverflow'
    return output


def stackexchange_xml_formatter(dic):
    """
    Finds all accepted answers and places NULL for questions with no
    accepted answers
    """
    if dic == {}:
        return {}
    out = {}
    for _i, _xml in header.items():
        if _xml == 'AcceptedAnswerId':
            if _xml in dic.keys():
                out[_i] = dic[_xml]
            else:
                out[_i] = 'NULL'
            continue
        out[_i] = dic[_xml] if _xml in dic.keys() else 'NULL'
    return out
    
def stackexchange_xml_mapper(xml_line):
    """
    One point handler of all xml to json map operations.
    """
    dic = stackexchange_xml_parser(xml_line)
    return stackexchange_xml_formatter(dic)

def stackexchange_xml_spark_job():
    server = bluebook_conf.HDFS_FQDN
    conf = SparkConf()

    xml_file_address = "hdfs://" + server + "/" +\
                       bluebook_conf.STACKEXCHANGE_XML_FOLDER_NAME +\
                       bluebook_conf.STACKEXCHANGE_XML_FILE_NAME
                         
    json_ques_folder_address = "hdfs://" + server + "/" +\
                               bluebook_conf.STACKEXCHANGE_JSON_QUES_FOLDER_NAME
    json_ans_folder_address = "hdfs://" + server + "/" +\
                              bluebook_conf.STACKEXCHANGE_JSON_ANS_FOLDER_NAME
        
    conf.setAppName('stackexchange_xml_spark_job')
    spark_context = SparkContext(conf=conf)
        
    file = spark_context.textFile(xml_file_address)

    # Ques and Ans files are stored seperately depending of their 'posttypeid'
    # Ques -> posttypeid == 1
    # Ans -> posttypeid == 2
    ques = file.map(stackexchange_xml_mapper)\
               .filter(lambda dic: 'posttypeid' in dic.keys())\
               .filter(lambda dic: dic['posttypeid'] == '1')\
               .map(lambda d: jsoner(d))
    ans = file.map(stackexchange_xml_mapper)\
               .filter(lambda dic: 'posttypeid' in dic.keys())\
               .filter(lambda dic: dic['posttypeid'] == '2')\
               .map(lambda d: jsoner(d))
    ques.saveAsTextFile(json_ques_folder_address)
    ans.saveAsTextFile(json_ans_folder_address)


if __name__ == '__main__':    
    stackexchange_xml_spark_job()
    
