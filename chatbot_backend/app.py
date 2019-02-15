from flask import Flask, render_template,jsonify,request,make_response
# Just disables the warning, doesn't enable AVX/FMA
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from pympler import asizeof
from models import *
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_nlu.model import Interpreter

import chatbot
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import pandas as pd
import pymysql
import requests
import spacy
import time


app = Flask(__name__)
app.secret_key = '6666'
CORS(app, support_credentials=True)


@app.route('/')
def index():
    chatbot.load_data()
    return render_template('index.html')


@app.route('/welcome_msg',methods=['GET','POST'])
def welcome_msg():

    welcomemsg = "Hi, I am OneConnectChatBot!. How can I help you?"
    print("Call this method!")

    return jsonify({"status":"success","response":welcomemsg})

@app.route('/chat',methods=['POST'])
@cross_origin(support_credentials=True)
def chat():

    try:
        data = request.json
        
        if data is None:
            user_message = request.form["text"]
        else:
            user_message = data["request"]

        # interpreter = RasaNLUInterpreter('models/current/nlu')

        # agent = Agent.load('models/current/dialogue', interpreter=interpreter)

        # responses = agent.handle_message(user_message)
        
        # print(responses)

        response = make_response()
        messagelist = chatbot.process_input(user_message,response)

        responses = [{'recipient_id': 'default', messagelist[1] : messagelist[0]}]
        # print("Chatbot reply")
        # print(responses)

        return jsonify({"status":"success","response":responses})

   
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)
