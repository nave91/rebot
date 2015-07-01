import re
from pyes import *
from kafka import SimpleProducer, KafkaClient

from bluebook import conf as bluebook_conf

def search_error(error):
    """
    Handle the response sent to user. Can define more options here for user to use.
    """
    cleaned_error = clean_error(error)
    results = call_es(cleaned_error)
    link = 'https://stackoverflow.com/a/' + str(results[0]['ans']['id'])
    num_results = len(results)
    features_set = bluebook_conf.features
    response = {
        'answer_link': link,
        'num_results': num_results,
        'feature_set': feature_set
    }
    return response

def call_es(error):
    """
    Call elasticsearch and submit a text based search.
    """
    conn = ES(bluebook_conf.ES_FQDN)
    q = QueryStringQuery("body:{}".format(error))
    results = conn.search(query=q)
    return results

def clean_error(error):
    """
    Get the first 500 characters and strip it off all non-alphanumerics.
    """
    shortened_error = error[:500]
    cleaned_error = re.sub('[\W_]+', ' ', shortened_error)
    return cleaned_error

def write_response_to_flume(error, response):
    """
    To send messages synchronously to kafka and to be written into hdfs.
    """
    kafka = KafkaClient(bluebook_conf.KAFKA_FQDN)
    producer = SimpleProducer(kafka)

    dic_to_write = {
        'error': error,
        'response': response
    }
    producer.send_messages(bluebook_conf.KAFKA_TOPIC, str(dic_to_write))
