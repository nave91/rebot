from py4j.java_gateway import java_import
java_import(sc._gateway.jvm, "org.elasticsearch.spark.Test")
test_object = sc._gateway.jvm.org.elasticsearch.spark.Test
test_object.run()
