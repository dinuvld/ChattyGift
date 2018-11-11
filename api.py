import sys
sys.path.append("~/Developer/ChattyGift/utils")

from flask import Flask
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
 
import requests
import card_methods 
import chatbot_utils.chatbot_responses as chat
import json
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def get_client_message():
    message = request.args("message")
    response = chat.chatbot_output(message)
    if response['final'] != {}:
        response["code"] = card_methods.issue_digital_card(response["code"]["brands"], response["code"]["cost"]["amount"])
    response = json(response)
    return response

@app.route('/card')
def create_card():
    return card_methods.issue_digital_card("nike", 10)