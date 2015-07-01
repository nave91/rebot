# Constants to be used across app
# Very very bad to do this. Replace FQDN with env variables
HDFS_FQDN = "ec2-52-8-214-93.us-west-1.compute.amazonaws.com:9000"
ES_FQDN = "ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200"
KAFKA_FQDN = "ec2-52-8-178-211.us-west-1.compute.amazonaws.com:9092"

# Index for ques/ans to be written into elasticsearch
# ES_INDEX = "rebot"
ES_INDEX = "fearebot"
SO_ES_TYPE = "stackoverflow_accepted"

# Kafka topic for ingestion of user logs
KAFKA_TOPIC = "test1"

# Config for HDFS
STACKEXCHANGE_XML_FOLDER_NAME = "input/"
STACKEXCHANGE_XML_FILE_NAME = "Posts.xml" 
# STACKEXCHANGE_XML_FILE_NAME = "stackexchange-posts-sample.xml" 

STACKEXCHANGE_JSON_QUES_FOLDER_NAME = "jsons/stackoverflowfea/ques/"
STACKEXCHANGE_JSON_ANS_FOLDER_NAME = "jsons/stackoverflowfea/ans/"
# STACKEXCHANGE_JSON_QUES_FOLDER_NAME = "jsons/sample-ques/"
# STACKEXCHANGE_JSON_ANS_FOLDER_NAME = "jsons/sample-ans/"

# Header for stackexchange mapping our own variables to stackoverflows schema
STACKEXCHANGE_HEADER_MAP = {
    'id': 'Id',
    'posttypeid': 'PostTypeId',
    'score': 'Score',
    'answer': 'AcceptedAnswerId',
    'body': 'Body',
    'snippets': 'snippets',
    'sourcetype': 'sourcetype',
    'score': 'Score',
    'viewcount': 'ViewCount',
    'tags': 'Tags',
    'anscount': 'AnswerCount',
    'commentcount': 'CommentCount',
    'favoritecount': 'FavoriteCount',
}

# Actions available using our API
AVAILABLE_ACTIONS = {
    'search for error': '/api/v1/error/'
}

# Features to be shot out to user querying through API
FEATURES = [
    'Score',
    'ViewCount',
    'LastActivityDate',
    'LastEditDate',
    'Tags',
    'AnswerCount',
    'CommentCount',
    'FavoriteCount'
]
