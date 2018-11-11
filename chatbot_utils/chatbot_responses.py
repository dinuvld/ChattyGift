# If youre getting error with the invalid google credentials run the terminal code from below:
# export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"

from flask import Flask, request, jsonify, render_template
from google.protobuf.json_format import MessageToJson
from random import randint
import os
import dialogflow
import requests
import json
import struct

# API Authentification
GOOGLE_AUTHENTICATION_FILE_NAME = "Gift-Card-52cf85c91a3b.json"
current_directory = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

# Input parameters
GOOGLE_PROJECT_ID = "gift-card-61e41"
session_Id = "unique"
language = "en"

# Initialise the session
session_client = dialogflow.SessionsClient()
session = session_client.session_path(GOOGLE_PROJECT_ID, session_Id)

context_short_name = "does_not_matter"
context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_Id + "/contexts/" + \
               context_short_name.lower()
context = dialogflow.types.context_pb2.Context(name=context_name)

final = dict()
recommendation_dict = {"sports": ["nike", "halfords"], "cooking": "tesco",
                     "gardening":["tesco"], "shoes":["debenhams", "foot-locker", "nike"],
                      "clothes": ["nike", "debenhams"]}
isBrandLast = False
lastBrand = ""
lastRecommendation = ""
isWaitingForYes = False

def choose_recommendation(recommendation):
    if not recommendation:
        return recommendation_dict["sports"][1]
    if recommendation in recommendation_dict:
        size = len(recommendation_dict[recommendation]) - 1
        return recommendation_dict[recommendation][randint(0,size)]
    

def generateSuggestion (brand, amount, cost, recommendation):
    if not brand or not isBrandLast:
        brand = choose_recommendation(recommendation = recommendation)
    elif brand and not isBrandLast:
        brand = choose_recommendation(recommendation = recommendation)
    if not amount:
        amount = randint(1, 11)*5
    if not cost:
        cost = {"currency": "GBP", "amount": randint(1, 101)}

    return {"brands": brand, "card_amount": amount, "cost": cost}

def process_input( text = "", language_code = language):
    """
    Sends the text and receives the response
    Updates the choosen parameters
    """
    global lastBrand, isBrandLast, lastRecommendation, isWaitingForYes, final
    suggestion = ""
    if text:
        text_input = dialogflow.types.TextInput(text=text, 
                                                language_code=language_code)
        query_input = dialogflow.types.QueryInput (text = text_input)
        query_parameter = dialogflow.types.QueryParameters (contexts = [context])
        response = session_client.detect_intent (session=session,query_input = query_input,
                                                 query_params = query_parameter)  
        parameters = json.loads(MessageToJson(response.query_result.parameters))
        # check what has been updated most recently - the brand or the recommendation
        if parameters:
            if lastBrand != parameters["brands"]:
                isBrandLast = True
            if lastRecommendation != parameters["recommendations"]:
                isBrandLast = False

            lastBrand = parameters["brands"]
            lastRecommendation = parameters["recommendations"]
            suggestion = generateSuggestion(parameters["brands"], parameters["card_amount"], 
                                                parameters["cost"], parameters["recommendations"])

        answer = response.query_result.fulfillment_text
        if text.lower() == "yes" and isWaitingForYes is True:            
            answer = "Thank you for the purchase!"
            isWaitingForYes = False
            return {"answer": answer, "suggestion": suggestion, "final": final}

        if all(word in answer.lower().split() for word in ['do', 'you', 'confirm']):
            final = {"brands": parameters["brands"], "card_amount": parameters["card_amount"], "cost": parameters["cost"]}
            isWaitingForYes = True

        return {"answer": answer, "suggestion": suggestion, "final": {}}



if __name__ == "__main__":
    data_in = ""
    data_in_previous = ""
    while True:
        data_in = input()
        if data_in != data_in_previous:
            data_in_previous = data_in
            chatbot_output = process_input(data_in_previous)
            print(chatbot_output)
