# es_spark_test.py
from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName("ESTest")
sc = SparkContext(conf=conf)

es = "ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200"
hdfs = "ec2-52-8-194-49.us-west-1.compute.amazonaws.com:9000"
es_write_conf = {
    "es.nodes" : es,
    "es.resource" : "wtf/me"
} 

def mapper(line):
    d = {}
    import ast
    json_line = ast.literal_eval(line)
    if not json_line: return ('key', {'NULL':'NULL'})
    for key,value in json_line.items():
        d[key] = value
    return ('key', d)

file = sc.textFile("hdfs://"+hdfs+"/raw/sample.csv")

words = file.map(lambda line: mapper(line))

words.collect()

words.saveAsNewAPIHadoopFile(
    path='-', 
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable", 
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
    conf=es_write_conf)

    
        
#$SPARK_HOME/bin/spark-submit --master spark://ip-172-31-2-242:7077 --jars /home/ubuntu/elasticsearch-hadoop-2.1.0.Beta2.jar /home/ubuntu/git/rebot/scripts/spark_to_es.py

# DELETE /stack_data/

# GET /fuck/_search
# {
#    "query": {
#       "match_all": {}
#    }
# }

# POST /stack_data/
# POST /stack_data/fail
# {
#     "id": "-1",
#     "posttypeid": "-2",
#     "score": "-1",
#     "answer": "-1"
# }

# GET /_cat/indices/

# PUT /stack_data/_settings
# {
#     "index.indexing.slowlog.threshold.index.info": "1ms" 
# }
