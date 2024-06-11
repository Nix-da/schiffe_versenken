from flask import Flask, jsonify
import threading
import os

app = Flask(__name__)


@app.route('/test')
def hello():
    speech_text = "Hello"
    return speech_text


@app.route('/test2')
def hello2():
    speech_text = {"message": "Hello2"}
    return jsonify(speech_text)


import subprocess

def run_server():
    # Start the Flask server in a new thread
    server_thread = threading.Thread(target=lambda: app.run(port=5000))
    server_thread.start()

    # Run the ngrok command
    ngrok_command = "ngrok http --domain=fair-boa-genuine.ngrok-free.app 5000"
    os.system(ngrok_command)


# Create a thread that runs the server
server_thread = threading.Thread(target=run_server)

# Start the thread
server_thread.start()
