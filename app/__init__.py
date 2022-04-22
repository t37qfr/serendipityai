# flask run
from flask import Flask

from views.topics import topics

app = Flask(__name__)

app.run(debug=True)
app.register_blueprint(topics)