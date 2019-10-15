# -*- coding: utf-8 -*-
from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import bcrypt
import pyrebase
import json
import pickle as p
#import numpy as np
import os
import sys
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("C:/Users/Ali Feizollah/OneDrive/Books/Siraj/1. Siraj Course/Week 5 - Midterm/flask_with_firebase/u-sentiment-web-firebase-adminsdk-pz77g-efd2bf7707.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()


def is_in_database(email):
    result = "no"
    doc_ref = store.collection(u'payment').stream()
    for doc in doc_ref:
	    #print(doc.id)
        d = doc.to_dict()
        print(d['email'], file=sys.stderr)
        if d['email'] == email:
            print("YESSSSSSSS", file=sys.stderr)
            result = "yes"
            return result
    return result

def add_paid_customer(email, token):
    doc_ref = store.collection(u'payment').document()
    doc_ref.set({ u'email': email, u'token': token })  
    

def get_user():
    auth = get_auth()
    user = auth.get_account_info(session['idToken'])
    return user


def add_user(username, password, email):
    """
    TODO: implement with firebase API
    """
    pass


def change_user(**kwargs):
    """
    TODO: implement with firebase API
    """
    pass


def hash_password(password):
    return bcrypt.hashpw(password.decode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
    """
    TODO: maybe not necessary actually
    """
    pass

def username_taken(username):
    """
    TODO: implement with firebase API
    """
    pass

def _get_default_firebase_config():
    '''
      var firebaseConfig = {
    apiKey: "AIzaSyBCyC67MCLyEfaDqZ2ImcnHbpDceBZqBUQ",
    authDomain: "u-sentiment-web.firebaseapp.com",
    databaseURL: "https://u-sentiment-web.firebaseio.com",
    projectId: "u-sentiment-web",
    storageBucket: "",
    messagingSenderId: "356912894146",
    appId: "1:356912894146:web:8e223023a5ad1c93472b5b",
    measurementId: "G-ZB89VJFKCF"
  };
    '''
    config = {
        'apiKey': os.environ['AIzaSyBCyC67MCLyEfaDqZ2ImcnHbpDceBZqBUQ'],
        'authDomain': os.environ['u-sentiment-web.firebaseapp.com'],
        'databaseURL': os.environ['https://u-sentiment-web.firebaseio.com'],
        'projectId': os.environ['u-sentiment-web'],
        'storageBucket': os.environ['storageBucket'],
        'messagingSenderId': os.environ['356912894146'],
        'appId': os.environ['1:356912894146:web:8e223023a5ad1c93472b5b']
    }
    return config

def _get_initialized_firebase():
    firebase = pyrebase.initialize_app(_get_default_firebase_config())
    return firebase

def get_auth():
    firebase = _get_initialized_firebase()
    auth = firebase.auth()
    return auth

def get_db():
    firebase = _get_initialized_firebase()
    db = firebase.database()
    return db

def get_storage():
    firebase = _get_initialized_firebase()
    storage = firebase.storage()
    return storage
'''
def get_lstm_model():
    modelfile = 'models/lstm_model'
    model = p.load(open(modelfile, 'rb'))
    return model

def get_mock_data():
    coordinates = np.random.uniform(size=(30, 1, 1))
    return coordinates

def get_ml_models():
    ml_models = ['LSTM']
    print(ml_models)
    return ml_models
'''