# -*- coding: utf-8 -*-
#from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import sys
import os
import numpy as np
import pyrebase
import stripe
import urllib.parse
import requests
#import keras.models

pub_key = "pk_test_W2b9R7bWfljV3Rh6V0UE2RPN000mbzn7ms"
secret_key = "sk_test_EH43mAoPMXNrBpNB1Fg8r5sG00sZ99ltch"
stripe.api_key = secret_key

config = {
    "apiKey": "AIzaSyBCyC67MCLyEfaDqZ2ImcnHbpDceBZqBUQ",
    "authDomain": "u-sentiment-web.firebaseapp.com",
    "databaseURL": "https://u-sentiment-web.firebaseio.com",
    "projectId": "u-sentiment-web",
    "storageBucket": "",
    "messagingSenderId": "356912894146",
    "appId": "1:356912894146:web:8e223023a5ad1c93472b5b"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if form.validate():
                #auth = helpers.get_auth()
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    session['logged_in'] = True
                    session['idToken'] = user['idToken']
                    return json.dumps({'status': 'Login successful'})
                except:
                    return json.dumps({'status': 'Login unsuccessful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = auth.get_account_info(session['idToken'])
    e = user['users'][0]['email']
    print(e, file=sys.stderr)
    t = helpers.is_in_database(e)
    if t == "yes":
        return render_template('home.html', user=user)
    else:
        return render_template("pay.html", pub_key=pub_key)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['idToken'] = None
    return redirect(url_for('login'))

# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            password = request.form['password']
            email = request.form['email']
            try:
                #auth = helpers.get_auth()
                user = auth.create_user_with_email_and_password(email, password)
                print(user['idToken'], file=sys.stderr)
                session['logged_in'] = True
                session['idToken'] = user['idToken']
                return json.dumps({'status': 'Signup successful'})
            except:
                return json.dumps({'status': 'Login unsuccessful'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))
'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if (request.method == 'POST'):
            email = request.form['email']
            password = request.form['password']
            user = auth.create_user_with_email_and_password(email, password)
            print(user['idToken'], file=sys.stderr)
            return render_template('login.html')
    return render_template('login.html')
'''

# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            # TODO: configure update settings with firebase api
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))

'''
# -------- API --------------------------------------------------------------- #
@app.route('/api/lstm', methods=['POST'])
def lstm_predict():
    if session.get('logged_in'):
        data = request.get_json()
        model = helpers.get_lstm_model()
        predictions = model.predict(data)
        return jsonify(score)
    return redirect(url_for('login'))

@app.route('/api/models', methods=['GET']) # TODO: add post request
def models():
    if session.get('logged_in'):
        ml_models = helpers.get_ml_models()
        resp = jsonify(ml_models)
        return resp
    return redirect(url_for('login'))
'''
# -------- PAY --------------------------------------------------------------- #
@app.route('/pay', methods=['POST'])
def pay():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    charge = stripe.Charge.create(
        customer = customer.id,
        amount = 499,
        currency = 'usd',
        description = 'Youtube Feel'
    )
    helpers.add_paid_customer(request.form['stripeEmail'], request.form['stripeToken'])
    return render_template('home.html')


# -------- PROCESS --------------------------------------------------------------- #
@app.route('/process', methods=['POST'])
def process():
    print(request.form.getlist(key='firstname')[0], file=sys.stderr)
    link = request.form.getlist(key='firstname')[0]
    print(link, file=sys.stderr)
    url_data = urllib.parse.urlparse(link)
    query = urllib.parse.parse_qs(url_data.query)
    video = query["v"][0]
    print(video, file=sys.stderr)

    url = "http://faizollah.pythonanywhere.com/sentiment/"+video
    print(url, file=sys.stderr)
    r = requests.get(url = url) 
    data = r.json()
    p = data["positive"]
    n = data["negative"]
    print(p, file=sys.stderr)
    print(n, file=sys.stderr)
    return render_template('results.html', positive = p, negative = n)

@app.route('/sentiment/<number>')
def home(number):

    videoId = number
    comments = CE.commentExtract(videoId)
    if comments == "nocomment":
        return "nocomment"
    psent, nsent = CE.sentiment(comments)
    result = FS.fancySentiment(comments, videoId)
    return jsonify(positive = str(psent), negative = str(nsent))

@app.route('/wordcloud/<number>')
def wordclou(number):

    videoId = number
    #comments = CE.commentExtract(videoId)
    #result = FS.fancySentiment(comments)
    #if result == "success":
    #    return send_file("fig.png", mimetype='image/gif')
    name = "/home/faizollah/mysite/wc/"+videoId+".png"
    return send_file(name, mimetype='image/gif')

    

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5500, debug=True, use_reloader=True)