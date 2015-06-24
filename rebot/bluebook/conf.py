HDFS_FQDN = "ec2-52-8-214-93.us-west-1.compute.amazonaws.com:9000"
ES_FQDN = "ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200"
KAFKA_FQDN = "ec2-52-8-178-211.us-west-1.compute.amazonaws.com:9092"

ES_INDEX = "rebot"
ES_TYPE = "skynet"

KAFKA_TOPIC = "test1"

STACKEXCHANGE_XML_FOLDER_NAME = "input/"
STACKEXCHANGE_XML_FILE_NAME = "Posts.xml" 
# STACKEXCHANGE_XML_FILE_NAME = "stackexchange-posts-sample.xml" 

STACKEXCHANGE_JSON_QUES_FOLDER_NAME = "jsons/ques/"
STACKEXCHANGE_JSON_ANS_FOLDER_NAME = "jsons/ans/"
# STACKEXCHANGE_JSON_QUES_FOLDER_NAME = "jsons/sample-ques/"
# STACKEXCHANGE_JSON_ANS_FOLDER_NAME = "jsons/sample-ans/"


STACKEXCHANGE_HEADER_MAP = {
    'id': 'Id',
    'posttypeid': 'PostTypeId',
    'score': 'Score',
    'answer': 'AcceptedAnswerId',
    'body': 'Body',
    'snippets': 'snippets'
}

AVAILABLE_ACTIONS = {
    'search for error': '/api/v1/error/'
}
