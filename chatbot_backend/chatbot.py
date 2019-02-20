from collections import OrderedDict
from datetime import datetime, timezone, timedelta
from dateutil import parser
from flask import request
from pympler import asizeof
from rasa_nlu.model import Interpreter

import conn_manager
import json
import requests
import re
import speech_recognition as sr
import spacy


NLP = spacy.load('en_core_web_lg')
INTERPRETER = Interpreter.load("models/current/nlu")
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

    FAQ_ID[:] = []
    FAQ_QN[:] = []
    FAQ_ANS[:] = []
    FAQ_TYPE[:] = []

    conn = conn_manager.get_conn()
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

    # Check for the need of two-tier handling of asking FAQs
    prep_answers = request.cookies.get("prep_answers")
    print(prep_answers)
    if prep_answers:
        resolved = second_confirm(input, prep_answers, response)
        if resolved[0] != None:
            print("Reach here?")
            return resolved[1]

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
       
    else:   # All top 3 similar FAQs have low similarity rate
        relevant_faq_ids = []
        relevant_match_rates = []
        prep_answers = []

        counter = 1

        for i in range(3):
            relevant_faq_ids.append(FAQ_ID[top_list[i][0]])
            relevant_match_rates.append(top_list[i][1])      
            prep_answers.append([ FAQ_ANS[top_list[i][0]] , FAQ_TYPE[top_list[i][0]] ])

            result[0] += str(i+1) + ". " + FAQ_QN[top_list[i][0]].text + "<br/>"
            counter += 1
  
        result[0] += str(counter) + ". None of the above"
        unresolved = ["So sorry I don't have an answer for your question.<br/>You may approach our staff for further enquiries.<br/>You can also visit our website at http://www.oneconnectft.com.sg/ </br>Thank you!","text"]
        prep_answers.append(unresolved)
        
        response.set_cookie("raw_qn", input)
        response.set_cookie("relevant_faq_ids", json.dumps(relevant_faq_ids))
        response.set_cookie("relevant_match_rates", json.dumps(relevant_match_rates))
        response.set_cookie("prep_answers", json.dumps(prep_answers))
        print(prep_answers)

    return result

# Two-tier handling of FAQs
def second_confirm(input, prep_answers, response):
    
    print("Start Two-tier handling of FAQs!")
    resolved = [None,["How can I help you?","Text"]]
    
    raw_qn = request.cookies.get("raw_qn")
    relevant_faq_ids = request.cookies.get("relevant_faq_ids")
    relevant_faq_ids = json.loads(relevant_faq_ids, object_pairs_hook = OrderedDict)
    relevant_match_rates = request.cookies.get("relevant_match_rates")
    relevant_match_rates = json.loads(relevant_match_rates, object_pairs_hook = OrderedDict)
    prep_answers = json.loads(prep_answers, object_pairs_hook = OrderedDict)
    analysis_id = request.cookies.get("analysis_id")

    response.set_cookie("raw_qn", expires=0)
    response.set_cookie("relevant_faq_ids", expires=0)
    response.set_cookie("relevant_match_rates", expires=0)
    response.set_cookie("prep_answers", expires=0)

    right_match_faq = None
    right_match_rate = None
    input_lower = input.lower()

    if input_lower == "1" or input_lower == "one" or input_lower == "first":        
        right_match_faq = relevant_faq_ids[0]
        right_match_rate = relevant_match_rates[0]
        
        resolved[0] = True
        resolved[1][0] = prep_answers[0][0]
        resolved[1][1] = prep_answers[0][1]

    elif input_lower == "2" or input_lower == "two" or input_lower == "second":      
        right_match_faq = relevant_faq_ids[1]
        right_match_rate = relevant_match_rates[1]
        
        resolved[0] = True
        resolved[1][0] = prep_answers[1][0]
        resolved[1][0] = prep_answers[1][1]

    elif input_lower == "3" or input_lower == "three" or input_lower == "third": 
        right_match_faq = relevant_faq_ids[2]
        right_match_rate = relevant_match_rates[2]

        resolved[0] = True
        resolved[1][0] = prep_answers[2][0]
        resolved[1][1] = prep_answers[2][1]

    else:
        resolved[0] = False
        resolved[1][0] = prep_answers[3][0]
        resolved[1][1] = prep_answers[3][1]
    


    return resolved
