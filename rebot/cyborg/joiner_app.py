import ast

from pyspark import SparkContext, SparkConf
from bluebook import conf as bluebook_conf

stackoverflow_es_write_conf = {
    "es.nodes": bluebook_conf.ES_FQDN,
    "es.resource": bluebook_conf.ES_INDEX + "/" + bluebook_conf.SO_ES_TYPE
}

def stackexchange_json_parser(line):
    d = {}
    json_line = ast.literal_eval(line)
    for key,value in json_line.items():
        d[key] = value
    return d
    
def stackexchange_json_mapper(line, _type):
    dic = stackexchange_json_parser(line)
    if _type == 'ques':
        return (dic['answer'], dic)
    else:
        return (dic['id'], dic)

def stackexchange_json_spark_job():
    server = bluebook_conf.HDFS_FQDN
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
    ques_tups = ques_file.map(lambda line: stackexchange_json_mapper(line, 'ques'))
    ans_tups = ans_file.map(lambda line: stackexchange_json_mapper(line, 'ans'))

    ques_ans = ques_tups.join(ans_tups).map(lambda x: (x[0], {'ques': x[1][0], 'ans': x[1][1]}))
    ques_ans.saveAsNewAPIHadoopFile(
        path='-', 
        outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf=stackoverflow_es_write_conf)
    
if __name__ == '__main__':
    stackexchange_json_spark_job()

#$SPARK_HOME/bin/spark-submit --master spark://ip-172-31-8-51:7077 --driver-memory 2300m --executor-memory 2300m --conf spark.driver.maxResultSize=0 --jars /home/ubuntu/packages/elasticsearch-hadoop-2.1.0.Beta2.jar ~/git/rebot/rebot/cyborg/joiner_app.py 
