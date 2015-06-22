from flask import render_template
from bluebook import app

@app.route('/api')
def api_view():
    return render_template('something.html')
