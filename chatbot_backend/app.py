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
import io
import json
import os
import pandas as pd
import pymysql
import requests
import spacy
import time

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
app = Flask(__name__)
app.secret_key = '6666'
CORS(app, support_credentials=True)

def run_quickstart():
    # Instantiates a client
    # [START speech_python_migration_client]
    client = speech.SpeechClient()
    # [END speech_python_migration_client]

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]

@app.route('/')
def index():
    chatbot.load_data()

    conn = conn_manager.get_conn()
    df = pd.read_sql_query('select * from announcement', con = conn)

    if conn != None:
        conn.close()

    return render_template('index.html')


@app.route('/welcome_msg',methods=['GET','POST'])
def welcome_msg():

    welcomemsg = "Hi, I am OneConnectChatBot!. How can I help you?"
  
    return jsonify({"status":"success","response":welcomemsg})

@app.route("/chat",methods=['POST'])
@cross_origin(support_credentials=True)
def chat():

    try:
        data = request.json
        
        if data is None:
            user_message = request.form["text"]
        else:
            user_message = data["request"]

        response = make_response()
        messagelist = chatbot.process_input(user_message,response)
        responses = [{'recipient_id': 'default', messagelist[1] : messagelist[0]}]
        responses_message = {"status":"success","response":responses}
        response.set_data(json.dumps(responses_message))
        
    except Exception as e:
        print(e)
        error_message = {"status":"success","response":[{"Sorry, chatbot is currently unavailable","Text"}]}
        response.set_data(json.dumps(error_message))

    return response

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)
