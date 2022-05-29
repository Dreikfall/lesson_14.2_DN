from flask import Flask
from API.views import api_blueprint

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(api_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
