from flask import Flask

app = Flask(__name__)


@app.route('/test')
def hello():
    speech_text = "Hello"
    return speech_text


app.run()
