from flask import render_template, url_for

from bluebook import app

@app.route("/")
@app.route("/index")  
def index(): 
    return render_template('index.html')

if __name__ == "__main__": 
    
    app.run(host='0.0.0.0', debug=True)
