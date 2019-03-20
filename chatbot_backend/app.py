from datetime import datetime, timedelta
# Just disables the warning, doesn't enable AVX/FMA
from flask import current_app, Flask, flash, make_response, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm 
from functools import update_wrapper
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import InputRequired, Email, Length

import chatbot
import conn_manager
import io
import json
import numpy as np
import os
import pandas as pd
import requests
import spacy
import time

class Config:
    SQLALCHEMY_DATABASE_URI = conn_manager.get_conn()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
app = Flask(__name__)
app.secret_key = '6666'
CORS(app, support_credentials=True)
app.config.from_object(Config)
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ljn@920506@localhost/chatbot'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = ''
chatbot.load_data()  

# username = admin, password = oneconnect@2019
class User(db.Model, UserMixin):
    __tablename__= 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('user_name',db.String(15), unique=True)
    password = db.Column('user_password',db.String(80), unique=True)
    first_name = db.Column('user_first_name',db.String(15), unique=True)
    last_name = db.Column('user_last_name', db.String(15), unique=True)
    email = db.Column('user_email',db.String(50), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Class for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('remember me')

# Class for registration
class RegisterForm(FlaskForm):    
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=30)])

# Class for resetPassword
class ResetPasswordForm(FlaskForm):
    current_password = PasswordField('Old Password', validators=[InputRequired(), Length(min=8, max=80)])
    new_password = PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm_new_password', message='New Password and Confirm New Password must match!')])
    confirm_new_password = PasswordField('Confirm New Password')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome_msg',methods=['GET'])
@cross_origin(support_credentials=True)
def welcome_msg():
    welcomemsg = "Hi, I am OneConnectChatBot!. How can I help you?"
    return jsonify({"status":"success","response":welcomemsg})

# Login backend method
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    error = ""
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for('home'))

        error = 'Invalid username or password!' 
        
    return render_template('admin_login.html', form = form, error = error)

# Change password backend method
@app.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    
    form = ResetPasswordForm()
    message = ""
    if form.validate_on_submit():
        user = current_user
        if check_password_hash(user.password, form.current_password.data):
            
            if form.new_password.data and form.confirm_new_password.data:
                
                hashed_password = generate_password_hash(form.new_password.data, method='sha256')
                
                user = current_user
                user.password = hashed_password
                db.session.add(user)
                db.session.commit()
                message = "Your password has been changed successfully!"
                return redirect(url_for('home'))
  
        message = "Invalid password. Please try again!"

    return render_template('admin_changepassword.html', form=form, message = message)

# Signup backend method
@app.route('/signup',methods=['GET','POST'])
# @login_required
def signup():
    form = RegisterForm()
    error = ""
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        error = "This username already inside database! Please try another one~"
    return render_template('admin_signup.html', form=form, error = error)

# Process the logic to log out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# The landing Dashboard page for home 
@app.route('/admin')
@cross_origin(support_credentials=True)
def home():
    
    conn = conn_manager.get_conn()    
    df = pd.read_sql_query('select analysis_timestamp as timestamp,faq_id from analysis',con=conn)
    
    if conn != None:
        conn.close()

    if df.empty:
        return render_template('homepage.html', sorted_date=['empty'])

    df = df[df['faq_id'] != 0]

    sorted_date = df.timestamp.dt.strftime('%Y-%-m-%d %H:%M:%S').unique()    
    list_date = sorted_date.tolist()
   
    year_list = df.timestamp.dt.strftime('%Y').unique().tolist()    
    month_value_list = df.timestamp.dt.strftime('%m').unique().tolist()
    month_label_list = df.timestamp.dt.strftime('%B').unique().tolist()
    month_list = sorted(zip(month_value_list,month_label_list))

    list_date.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    return render_template('homepage.html',yearlist = year_list,monthlist = month_list,sorted_date=json.dumps(list_date))

# upon landing to the dashboard page, this back end will auto-process different datasets required from the dashboard to psa-dashboard-chart.js for further loading process to Dashboard
@app.route('/category_analysis', methods = ['POST'])
@login_required
def category_anlaysis():
    
    conn = conn_manager.get_conn()
    df = pd.read_sql_query('select f.faq_question, f.faq_answer, a.analysis_id, a.analysis_user_input, a.analysis_timestamp as timestamp, a.faq_id from analysis a LEFT JOIN faq f on f.faq_id = a.faq_id',con=conn)   
   
    if conn != None:
        conn.close()

    if not df.empty:
        df['accuracy'] = np.where(df['faq_id']!=-1,1,0)     
        
        year = datetime.now().year
        
        df = df[df['timestamp'].dt.year == year]
        df = df[df['faq_id'] != 0]

        #hit analysis  
        hit_analysis_df = df.groupby(pd.Grouper(key='timestamp', freq='1M')) \
        .agg({'analysis_user_input':'size', 'accuracy':'mean'}) \
        .rename(columns={'analysis_user_input':'total_count','accuracy':'accuracy_mean'}) \
        .reset_index()
        hit_analysis_df = hit_analysis_df[np.isfinite(hit_analysis_df['accuracy_mean'])]
        hit_analysis_df.timestamp = hit_analysis_df.timestamp.dt.strftime('%B')
           

        hit_day_list = hit_analysis_df['timestamp'].tolist()
        hit_day_count = hit_analysis_df['total_count'].tolist()
        hit_day_accuracy = hit_analysis_df['accuracy_mean'].tolist()
        
        accuracy_rate = 0

        df_copy = df[['timestamp','faq_id']]
      
        hit_amount = len(df_copy)
        resolved_num = len(df_copy.loc[df_copy['faq_id'] != -1])
        hit_day_unresolved_num = [round((1.0-x)*y) for x, y in zip(hit_day_accuracy, hit_day_count)]
        
        hit_day_resolved_num = [round(x*y) for x, y in zip(hit_day_accuracy, hit_day_count)]
        
        hit_day_resolved_rate = []
        for row in hit_day_accuracy:
            hit_day_resolved_rate.append(round(row*100))
        
        if hit_amount != 0:
            accuracy_rate = round(resolved_num * 100.0 / hit_amount )

    #top k question analysis 
    df3 = df[df.faq_question!='NA']
    question_analysis_df = df3.groupby('faq_question') \
    .agg({'analysis_id':'size'}) \
    .rename(columns={'faq_question':'faq_question','analysis_id':'count'}) \
    .reset_index()
    question_analysis_df_sorted  = question_analysis_df.nlargest(10,'count')
    question_analysis_df_sorted = question_analysis_df_sorted.reset_index(drop=True)
    question_analysis_index = question_analysis_df_sorted.index.tolist()
    question_analysis_list = question_analysis_df_sorted['faq_question'].tolist()
    question_analysis_count = question_analysis_df_sorted['count'].tolist()

    return jsonify(
        hit_day_list = hit_day_list,
        hit_day_count = hit_day_count,
        hit_day_resolved_num = hit_day_resolved_num,
        hit_day_unresolved_num = hit_day_unresolved_num,
        hit_day_resolved_rate = hit_day_resolved_rate,
        hit_amount = hit_amount,
        resolved_num = resolved_num,
        accuracy_rate = accuracy_rate,
        question_analysis_index = question_analysis_index ,
        question_analysis_list = question_analysis_list,
        question_analysis_count = question_analysis_count 
        )

# filter user filter the timestamp on the dashboard page, this back end will process different filtered datasets required from the dashboard to psa-dashboard-chart.js for further loading process to Dashboard
@app.route("/breakdown_analysis", methods = ['POST'])
@cross_origin(supports_credentials=True)
@login_required
def breakdown_analysis():

    if request.method == 'POST':

        try : 
            data = request.get_json()
            choice = data['choice']
            year = data['year']
            month = data['month']

        except Exception:
            return jsonify(error=1)

        conn = conn_manager.get_conn()
        df = pd.read_sql_query('select f.faq_question, f.faq_answer, a.analysis_id, a.analysis_user_input, a.analysis_timestamp as timestamp, a.faq_id from analysis a LEFT JOIN faq f on f.faq_id = a.faq_id',con=conn)   
   
        if conn != None:
            conn.close()

        if not df.empty:

            df['accuracy'] = np.where(df['faq_id']!=-1,1,0)
            
           
            df = df[df['faq_id'] != 0]

            #hit analysis
            if choice =="year": 
                df = df[df['timestamp'].dt.year == year]

                hit_analysis_df = df.groupby(pd.Grouper(key='timestamp', freq='1M')) \
            .agg({'analysis_user_input':'size', 'accuracy':'mean'}) \
            .rename(columns={'analysis_user_input':'total_count','accuracy':'accuracy_mean'}) \
            .reset_index()
                hit_analysis_df = hit_analysis_df[np.isfinite(hit_analysis_df['accuracy_mean'])]
                hit_analysis_df.timestamp = hit_analysis_df.timestamp.dt.strftime('%B')
            
                            
            if choice == "month":

                df = df[df['timestamp'].dt.year == year]

                df= df[df['timestamp'].dt.month == month]

                hit_analysis_df = df.groupby(pd.Grouper(key='timestamp', freq='D')) \
            .agg({'analysis_user_input':'size', 'accuracy':'mean'}) \
            .rename(columns={'analysis_user_input':'total_count','accuracy':'accuracy_mean'}) \
            .reset_index()
                hit_analysis_df = hit_analysis_df[np.isfinite(hit_analysis_df['accuracy_mean'])]
                hit_analysis_df['timestamp'] = hit_analysis_df.timestamp.dt.strftime('%d')
            
                
            if choice =="day":
                year = data['year']
                month = data['month']
                day = data['day']

                df = df[df['timestamp'].dt.year == year]
                df = df[df['timestamp'].dt.month == month]
                df = df[df['timestamp'].dt.day == day]
                df['timestamp']= df['timestamp'].dt.floor('h')

                hit_analysis_df = df.groupby('timestamp') \
            .agg({'analysis_user_input':'size', 'accuracy':'mean'}) \
            .rename(columns={'analysis_user_input':'total_count','accuracy':'accuracy_mean'}) \
            .reset_index()
                hit_analysis_df = hit_analysis_df[np.isfinite(hit_analysis_df['accuracy_mean'])]
                hit_analysis_df['timestamp'] = hit_analysis_df.timestamp.dt.strftime('%I %p')
            
            hit_day_list = hit_analysis_df['timestamp'].tolist()
            hit_day_count = hit_analysis_df['total_count'].tolist()
            hit_day_accuracy = hit_analysis_df['accuracy_mean'].tolist()

            accuracy_rate = 0

            df_copy = df[['timestamp','faq_id']]
            hit_amount = len(df_copy)
            resolved_num = len(df_copy.loc[df_copy['faq_id'] != -1])
            hit_day_unresolved_num = [round((1.0-x)*y) for x, y in zip(hit_day_accuracy, hit_day_count)]
            
            hit_day_resolved_num = [round(x*y) for x, y in zip(hit_day_accuracy, hit_day_count)]


            hit_day_resolved_rate = []
            for row in hit_day_accuracy:
                hit_day_resolved_rate.append(round(row*100))
            

            if hit_amount != 0:
                accuracy_rate = round(resolved_num * 100.0 / hit_amount )
                print(accuracy_rate)

            if hit_amount != 0:
                accuracy_rate = round(resolved_num * 100.0 / hit_amount )

        #top k question analysis 
        df3 = df[df.faq_question!='NA']
        question_analysis_df = df3.groupby('faq_question') \
        .agg({'analysis_id':'size'}) \
        .rename(columns={'faq_question':'faq_question','analysis_id':'count'}) \
        .reset_index()
        question_analysis_df_sorted  = question_analysis_df.nlargest(10,'count')
        question_analysis_df_sorted = question_analysis_df_sorted.reset_index(drop=True)
        question_analysis_index = question_analysis_df_sorted.index.tolist()
        question_analysis_list = question_analysis_df_sorted['faq_question'].tolist()
        question_analysis_count = question_analysis_df_sorted['count'].tolist()

        return jsonify(
            hit_day_list = hit_day_list,
            hit_day_count = hit_day_count,
            hit_day_resolved_num = hit_day_resolved_num,
            hit_day_unresolved_num = hit_day_unresolved_num,
            hit_day_resolved_rate = hit_day_resolved_rate,
            hit_amount = hit_amount,
            resolved_num = resolved_num,
            accuracy_rate = accuracy_rate,
            question_analysis_index = question_analysis_index ,
            question_analysis_list = question_analysis_list,
            question_analysis_count = question_analysis_count,
            error = 0
            )

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
        chatbot.process_input(user_message,response)
        
    except Exception as e:
        print(e)
        error_message = {"status":"success","response":[{"Sorry, chatbot is currently unavailable","Text"}]}
        response.set_data(json.dumps(error_message))

    return response

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)


