from flask import Flask

app = Flask(__name__)

@app.route('/helloWorld')
def hello_world():
    return "Hello, World - das kommt aus deiner IDE!"

@app.route('/test')
def hello():
    speech_text = "Hello"
    return speech_text

if __name__ == '__main__':
    app.run(port=5001)
