
from flask import request, render_template
from flask_restful import Resource, Api

from bluebook import app
from bluebook import conf as bluebook_conf

from lib import search_error, write_response_to_flume

api = Api(app)

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
        response = search_error(error)
        write_response_to_flume(error, response)
        return response

api.add_resource(IndexV1, '/api/v1')
api.add_resource(ErrorV1, '/api/v1/error')
