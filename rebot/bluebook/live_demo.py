import requests

from flask import Blueprint, render_template, request
from flask.ext.wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired

from lib import search_error

def call_server(error):
    server = 'http://localhost:5000/api/v1/error'
    params = {
        'error_log': error
    }
    result = {}
    r = requests.post(server, params)
    if r.status_code == 200:
        result['answer_link'] = r.json()['answer_link']
        result['num_results'] = r.json()['num_results']
    return result

class SearchForm(Form):
    logs = TextAreaField('logs', validators=[DataRequired()])

demo_page = Blueprint('demo_page', __name__, template_folder='templates')

@demo_page.route("/demo")  
def live_demo(): 
    return render_template('demo.html')

@demo_page.route("/search", methods=['GET', 'POST'])  
def search(): 
    form = SearchForm()
    if request.method == 'POST' and form.validate():
        result = search_error(form.logs.data)
        return render_template('search.html', form=form, result=result)
    return render_template('search.html', form=form, result={})
