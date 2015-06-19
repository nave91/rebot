import ast

from pyspark import SparkContext, SparkConf
from bluebook import conf as bluebook_conf

es_write_conf = {
    "es.nodes": bluebook_conf.ES_FQDN,
    "es.resource": bluebook_conf.ES_INDEX + "/" + bluebook_conf.ES_TYPE
}

def stackexchange_json_parser(line):
    d = {}
    json_line = ast.literal_eval(line)
    if not json_line: return ('key', {'NULL':'NULL'})
    for key,value in json_line.items():
        d[key] = value
    return d
    
def stackexchange_json_mapper(line, _type):
    dic = stackexchange_json_parser(line)
    return (_type, dic)

def stackexchange_json_spark_job(line):
    conf = SparkConf().setAppName("stackexchange_json_spark_job")
    spark_context = SparkContext(conf=conf)
    
    json_ques_folder_address = "hdfs://" + server + "/" +\
                              bluebook_conf.STACKEXCHANGE_JSON_QUES_FOLDER_NAME +\
                              "/part-*"
    json_ans_folder_address = "hdfs://" + server + "/" +\
                              bluebook_conf.STACKEXCHANGE_JSON_ANS_FOLDER_NAME +\
                              "/part-*"

    ques_file = spark_context.textFile(json_ques_folder_address)
    ans_file = spark_context.textFile(json_ans_folder_address)
    
    ques_tups = file.map(lambda line: stackexchange_json_mapper(line, 'ques'))
    ans_tups = file.map(lambda line: stackexchange_json_mapper(line, 'ans'))

    # DO SOMETHING

    ques_ans.saveAsNewAPIHadoopFile(
    path='-', 
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable", 
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
    conf=es_write_conf)