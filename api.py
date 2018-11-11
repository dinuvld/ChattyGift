import sys
sys.path.append("~/Developer/ChattyGift/utils")

from flask import Flask
from flask import Flask, render_template, session, request

 
import requests
import card_methods 
import chatbot_utils.chatbot_responses as chat
import json
import time
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/')
def get_client_message():
    message = unquote(request.args['message'])
    print(message)
    response = chat.process_input(message)
    if response['final'] != {}:
        response["code"] = card_methods.issue_digital_card(response["code"]["brands"], response["code"]["cost"]["amount"])
    response = json.dumps(response)
    return response

@app.route('/card')
def create_card():
    return card_methods.issue_digital_card("nike", 10)