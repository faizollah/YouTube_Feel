# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class LoginForm(Form):
    email = StringField('Email:', validators=[validators.optional(), validators.Length(min=0, max=50)])
    username = StringField('Username:', validators=[validators.optional(), validators.Length(min=1, max=30)])
    password = StringField('Password:', validators=[validators.required(), validators.Length(min=1, max=30)])