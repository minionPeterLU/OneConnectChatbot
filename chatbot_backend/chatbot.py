from flask import request
from datetime import datetime, timezone, timedelta
from dateutil import parser
from collections import OrderedDict
from rasa_nlu.model import Interpreter
from pympler import asizeof
# import conn_manager
import spacy
import pymysql
import json
import requests
import re

# Local database connection
HOST = 'localhost'
DBNAME = 'chatbot'
USER = 'root'
PASSWORD = 'Ljn@920506'
PORT = 3306

NLP = spacy.load('en_core_web_lg')
INTERPRETER = Interpreter.load("models/current/nlu")
FAQ_ID = []
FAQ_QN = []
FAQ_ANS = []
FAQ_TYPE = []

MATCH_THRESHOLD = 0.9
# INTERPRETER = Interpreter.load("rasa/models/default/intents")


# Retrieve FAQs from database and put into NLP pipelines when web server is started or if there's any change in FAQs
def load_data():
    global FAQ_ID
    global FAQ_QN
    global FAQ_ANS
    global FAQ_TYPE

    FAQ_ID[:] = []
    FAQ_QN[:] = []
    FAQ_ANS[:] = []
    FAQ_TYPE[:] = []


    conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DBNAME)
    cur = conn.cursor()
    
    cur.execute("SELECT faq_id, faq_question, faq_answer, faq_type FROM faq ORDER BY faq_id")
    result = cur.fetchall()
    for row in result:
        FAQ_ID.append(row[0])
        FAQ_QN.append(NLP(row[1]))
        FAQ_ANS.append(row[2])
        FAQ_TYPE.append(row[3])
    cur.close()
    conn.close()


# Entry point of input from front-end
def process_input(input, response):

    result = ["Sorry, I'm not very sure what you mean.<br/>Are you asking:<br/>","text"]

    if len(FAQ_QN) == 0:
        load_data()


    # Put into NLP pipeline
    input_vector = NLP(input)
            
    # FAQ matching
    top_list = []
    for i in range(3):
        top_list.append([-1, 0.0])
    
    
    for i, faq_vector in enumerate(FAQ_QN):
        similar = input_vector.similarity(faq_vector)
        print(similar)
        for index_max in top_list:
            if similar > index_max[1]:
                index_max[0] = i
                index_max[1] = similar
                break
    
    if top_list[0][1] >= MATCH_THRESHOLD:   # Most similar FAQ has a similarity rate of > 90%
        result[0] = FAQ_ANS[top_list[0][0]]
        result[1] = FAQ_TYPE[top_list[0][0]]
        print(result)
        return result

    else:   # All top 3 similar FAQs have low similarity rate
        # to_return = "Sorry, I'm not very sure what you mean.<br/>Are you asking:<br/>"
        counter = 1

        for i in range(3):
            result[0] += str(i+1) + ". " + FAQ_QN[top_list[i][0]].text + "<br/>"
            counter += 1
            if top_list[i][0] == -1:
                break      
        
        result[0] += str(counter) + ". None of the above"

        return result
