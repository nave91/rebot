import re
from flask import request
from flask_restful import Resource, Api
from pyes import *

from bluebook import app
from bluebook import conf as bluebook_conf

api = Api(app)


def call_es(error):
    conn = ES(bluebook_conf.ES_FQDN)
    q = QueryStringQuery("ques.snippets:{}".format(error))
    results = conn.search(query=q)
    return results

def clean_error(error):
    shortened_error = error[:500]
    cleaned_error = re.sub('[\W_]+', ' ', shortened_error)
    return cleaned_error

class IndexV1(Resource):
    def get(self):
        return {
            'ERROR': 'Specify action.',
            'available_actions': bluebook_conf.AVAILABLE_ACTIONS,
        }, 400

    def post(self):
        return {
            'ERROR': 'Specify action.',
            'available_actions': bluebook_conf.AVAILABLE_ACTIONS,
        }, 400
        
    def put(self):
        return {
            'ERROR': 'Specify action.',
            'available_actions': bluebook_conf.AVAILABLE_ACTIONS,
        }, 400
        
class ErrorV1(Resource):
    def get(self):
        return {
            'ERROR': 'Wrong request type.'
        }, 400
        
    def put(self):
        return {
            'ERROR': 'Wrong request type.'
        }, 400
        
    def post(self):
        error = request.form['error_log']
        cleaned_error = clean_error(error)
        results = call_es(cleaned_error)
        link = 'https://stackoverflow.com/a/' + str(results[0]['ans']['id'])
        num_results = len(results)
        response = {
            'answer_link': link,
            'num_results': num_results
        }
        return response 

api.add_resource(IndexV1, '/api/v1')
api.add_resource(ErrorV1, '/api/v1/error')
