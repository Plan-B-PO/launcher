from flask import Flask
import json

app = Flask(__name__)
counter = 0


@app.route('/logs', methods={'GET'})
def send_logs():
    global counter
    counter = counter + 1
    return json.dumps(counter), 200