from collections import OrderedDict
from datetime import datetime, timezone, timedelta
from dateutil import parser
from flask import request
from models import *
from pympler import asizeof
from rasa_nlu.model import Interpreter
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

import ast
import conn_manager
import json
import requests
import re
# import speech_recognition as sr
import spacy


NLP = spacy.load('en_core_web_lg')
FAQ_ID = []
FAQ_QN = []
FAQ_ANS = []
FAQ_TYPE = []
MATCH_THRESHOLD = 0.9

# Retrieve FAQs from database and put into NLP pipelines when web server is started or if there's any change in FAQs
def load_data():
    global FAQ_ID
    global FAQ_QN
    global FAQ_ANS
    global FAQ_TYPE
    # global agent
    
    FAQ_ID[:] = []
    FAQ_QN[:] = []
    FAQ_ANS[:] = []
    FAQ_TYPE[:] = []

    conn = conn_manager.get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT faq_id, faq_question, faq_answer, faq_type FROM faq ORDER BY faq_id")
        result = cur.fetchall()
        for row in result:
            FAQ_ID.append(row[0])
            FAQ_QN.append(NLP(row[1]))
            FAQ_ANS.append(row[2])
            FAQ_TYPE.append(row[3])
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

# Following 3 functions are for storing processed inputs into database
def store_data(input,faq_id):
    conn = conn_manager.get_conn()
    cur = conn.cursor()
   
    try:
        # ==================================================================================
        # If MySQL analysis table does not have auto-increment use the following code:
        # analysis_id = 1
        # cur.execute("SELECT MAX(analysis_id) FROM analysis")
        # if cur.fetchall()[0][0] is None:
        #     analysis_id = 1
        # else:
        #     analysis_id = cur.fetchall()[0][0] + 1
        # =================================================================================
        analysis_id = None
        analysis_timestamp =  datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        cur.execute("INSERT INTO analysis VALUES (%s,%s, %s, %s)", (analysis_id,input, analysis_timestamp, faq_id))
    except Exception as e:
        print(e)
    finally:  
        cur.close()
        conn.commit()
        conn.close()

# Entry point of input from front-end
def process_input(input, response):

    result = ["Sorry, I'm not very sure what you mean.<br/>Are you asking:<br/>","text"]
    
    # load FAQ from Database to NLP pipelines
    if len(FAQ_QN) == 0 or len(FAQ_ANS) == 0 or len(FAQ_ID) == 0:
        load_data()
    
    
    # Put into NLP pipeline
    input_vector = NLP(input)
    
    # FAQ matching
    top_list = []
    similarity_list = []
    
    for i, faq_vector in enumerate(FAQ_QN):
        similar = input_vector.similarity(faq_vector)
        similarity_list.append([similar,i])
        print(similar)
    
    similarity_list = sorted(similarity_list)
    topNum = len(similarity_list)-1

    for j in range(3):    
        top_list.append([similarity_list[topNum-j][1],similarity_list[topNum-j][0]])


    # Decide the correct answer to return based on similarity rate
    # Most similar FAQ has a similarity rate of > 90%  
    if top_list[0][1] >= MATCH_THRESHOLD:     
        result[0] = FAQ_ANS[top_list[0][0]]
        result[1] = FAQ_TYPE[top_list[0][0]]
        faq_id = FAQ_ID[top_list[0][0]]
        print(type(result[0]))
        store_data(input, faq_id)
        print("User input recorded!")

        if result[1] =="buttons":
            print(result[0])
            # print(len(result[0]))
            # buttonList = ast.literal_eval(result[0])  
            buttonList = result[0].split(",")
            print(buttonList)
            buttons = []
            # [{'payload': 'great', 'title': 'great'}, {'payload': 'super sad', 'title': 'super sad'}]
            for i in range( len(buttonList) ):
                buttons.append({"payload": buttonList[i], "title": buttonList[i]})
            responses = []  
            # for i in range(len(buttons)):
            responses.append({'recipient_id': 'default', result[1] : buttons})
            responses_message = {"status":"success","response":responses}
            response.set_data(json.dumps(responses_message))
            print(responses_message)
        else:
            responses = [{'recipient_id': 'default', result[1] : result[0]}]
            responses_message = {"status":"success","response":responses}
            response.set_data(json.dumps(responses_message))
    else :
        faq_id = -1
        store_data(input, faq_id)
        interpreter = RasaNLUInterpreter('models/current/nlu')
        agent = Agent.load('models/current/dialogue', interpreter=interpreter)
        responses = agent.handle_message(input)
        
        if responses == []:
            responses = [{'recipient_id': 'default', 'text' : 'Sorry, I cound not understand what you mean! Can you say again?'}]

        responses_message = {"status":"success","response":responses}
        response.set_data(json.dumps(responses_message))
