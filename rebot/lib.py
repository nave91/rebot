import re
from pyes import *
from kafka import SimpleProducer, KafkaClient

from bluebook import conf as bluebook_conf

def search_error(error):
    cleaned_error = clean_error(error)
    results = call_es(cleaned_error)
    link = 'https://stackoverflow.com/a/' + str(results[0]['ans']['id'])
    num_results = len(results)
    response = {
        'answer_link': link,
        'num_results': num_results
    }
    return response

def call_es(error):
    conn = ES(bluebook_conf.ES_FQDN)
    q = QueryStringQuery("body:{}".format(error))
    results = conn.search(query=q)
    return results

def clean_error(error):
    shortened_error = error[:500]
    cleaned_error = re.sub('[\W_]+', ' ', shortened_error)
    return cleaned_error

def write_response_to_flume(error, response):
    # To send messages synchronously
    kafka = KafkaClient(bluebook_conf.KAFKA_FQDN)
    producer = SimpleProducer(kafka)

    dic_to_write = {
        'error': error,
        'response': response
    }
    # Note that the application is responsible for encoding messages to type bytes
    producer.send_messages(bluebook_conf.KAFKA_TOPIC, str(dic_to_write))
