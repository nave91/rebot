from flask import Blueprint, render_template, request
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


demo_page = Blueprint('demo_page', __name__, template_folder='templates')

@demo_page.route("/demo")  
def live_demo(): 
    return render_template('demo.html')
    
    

class SearchForm(Form):
    logs = StringField('logs', validators=[DataRequired()])


@demo_page.route("/search", methods=['GET', 'POST'])  
def search(): 
    form = SearchForm()
    if request.method == 'POST' and form.validate():
        import ipdb; ipdb.set_trace()
        return 'some'
    
    return render_template('search.html', form=form)
