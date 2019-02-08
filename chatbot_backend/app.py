from flask import Flask
from flask import render_template,jsonify,request
import requests
from models import *
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import time
# Just disables the warning, doesn't enable AVX/FMA
from flask_cors import CORS, cross_origin
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

app = Flask(__name__)
app.secret_key = '6666'
CORS(app, support_credentials=True)

@app.route('/')
def index():
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

        interpreter = RasaNLUInterpreter('models/current/nlu')

        agent = Agent.load('models/current/dialogue', interpreter=interpreter)

  

        responses = agent.handle_message(user_message)
        
        # messages = []
        # for r in responses:
        #     messages.append(r.get("text"))

        print(responses)

        # if len(messages) == 0:                
        #     messages.append("Sorry I don't understand what you said! Can you rephase your sentence?")

        # response_text = messages[0]

        return jsonify({"status":"success","response":responses})

    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)
