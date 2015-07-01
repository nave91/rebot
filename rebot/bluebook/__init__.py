from flask import Flask
from bluebook.live_demo import demo_page

app = Flask(__name__)
#app.config.from_object('config')
app.register_blueprint(demo_page)

import api.views
