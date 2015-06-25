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

@demo_page.route("/demo", methods=['GET', 'POST'])  
def live_demo(): 
    form = SearchForm()
    default_log = "Traceback (most recent call last):\n  File 'pyspark/hbase/hbase_tests.py'," +\
                  "line 81, in <module>\n    test._test()\n  File 'pyspark/hbase/hbase_tests.py," +\
                  "line 76, in _test\n    self.create_test_tables()\n  File 'pyspark/hbase/hbase_tests.py'," +\
                  "line 46, in create_test_tables\n    self._ctx().sql(create_sql).toRdd().collect()\n" +\
                  "    File '/shared/pyjava/python/pyspark/sql.py', line 1620, in sql" +\
                  "        return SchemaRDD(self._ssql_ctx.sql(sqlQuery).toJavaSchemaRDD(), self)\n" +\
                  "    File '/shared/pyjava/python/pyspark/hbase/hbase.py', line 58, in _ssql_ctx"+\
                  " self._scala_HBaseSQLContext = self._get_hbase_ctx()\n" +\
                  "  File '/shared/pyjava/python/pyspark/hbase/hbase.py', line 83, in _get_hbase_ctx\n" +\
                  "    return self._jvm.HBaseSQLContext(self._jsc.sc())" +\
                  "  File '/shared/pyjava/python/lib/py4j-0.8.2.1-src.zip/py4j/java_gateway.py', line 726, in __getattr__" +\
                  "                  py4j.protocol.Py4JError: Trying to call a package."
    if request.method == 'POST':
        result = search_error(default_log)
        return render_template('demo.html', form=form, default_log=default_log, result=result)
    return render_template('demo.html', form=form, default_log=default_log, result={})

@demo_page.route("/search", methods=['GET', 'POST'])  
def search(): 
    form = SearchForm()
    if request.method == 'POST' and form.validate():
        result = search_error(form.logs.data)
        return render_template('search.html', form=form, result=result)
    return render_template('search.html', form=form, result={})
