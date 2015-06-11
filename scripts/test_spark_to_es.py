# es_spark_test.py
from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName("ESTest")
sc = SparkContext(conf=conf)

es = "ec2-52-8-185-215.us-west-1.compute.amazonaws.com:9200"

es_write_conf = {
    "es.nodes" : es,
    "es.resource" : "titanic/fail"
} 
some_data=sc.parallelize([1,2,3,4])
some_data_mapped_to_keys=some_data.map(lambda x: ('key', {'name': str(x), 'sim':0.22}))
some_data_mapped_to_keys.collect()


some_data_mapped_to_keys.saveAsNewAPIHadoopFile(
    path='-', 
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable", 
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
    conf=es_write_conf)
    
