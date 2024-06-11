from flask import Flask, jsonify
import threading
import os

skill_message = []


def get_skill_message():
    if skill_message:
        return skill_message.pop(0)
    else:
        return None


app = Flask(__name__)


@app.route('/test')
def hello():
    speech_text = "Hello"
    return speech_text


@app.route('/attack/<field>')
def attack(field):
    speech_text = {"message": "Hello2"}
    return jsonify(field)


@app.route('/mode/<mode>')
def mode(mode):
    global skill_message
    if mode == "bot modus":
        skill_message.append("bot modus")
        speech_text = "Das Spiel wird im Bot Modus gestartet. Bitte platziere deine Schiffe."
    else:
        skill_message.append("multiplayer modus")
        speech_text = "Das Spiel wird im Multiplayer Modus gestartet. Bitte gibt die IP deines Gegners ein."
    return speech_text


@app.route('/restart')
def restart():
    global skill_message
    skill_message.append("restart")
    speech_text = "Das Spiel wurde neu gestartet. Möchtest du im Bot Modus oder Multiplayer Modus spielen?"
    return speech_text


@app.route('/random_place_ships')
def random_place_ships():
    global skill_message
    skill_message.append("random place ships")
    speech_text = "Die Schiffe wurden zufällig platziert. Sie können Änderungen vornehmen oder das Spiel starten."
    return speech_text


@app.route('/start_game')
def start_game():
    global skill_message
    skill_message.append("start game")
    speech_text = "Das Spiel wird gestartet."
    return speech_text


@app.route('/set_ip/<ip>')
def set_ip(ip):
    global skill_message
    skill_message.append(ip)
    speech_text = "Die IP wurde auf " + ip + " gesetzt."
    return speech_text


@app.route('/connect')
def connect():
    global skill_message
    skill_message.append("connect")
    speech_text = "Die Verbindung wird hergestellt."
    return speech_text


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
