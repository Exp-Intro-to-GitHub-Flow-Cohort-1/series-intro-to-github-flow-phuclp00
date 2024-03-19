# Generate some code for python 3.6

import os
import sys
import time
import random
import string
import requests
import json
import re

# Import the Flask Framework
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

# Create an instance of Flask
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_ORIGINS'] = '*'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['CORS_EXPOSE_HEADERS'] = 'Content-Type'
app.config['CORS_ALLOW_CREDENTIALS'] = True
app.config['CORS_AUTOMATIC_OPTIONS'] = True
app.config['CORS_MAX_AGE'] = 3600
app.config['CORS_SEND_WILDCARD'] = False
app.config['CORS_ALWAYS_SEND'] = True

# Create an instance of SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)

# Define the model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
# Define the routes
@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))
    users = User.query.all()
    return render_template('users.html', users=users)
  
@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('api_users'))
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])
  
@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def api_user(id):
    if request.method == 'PUT':
        user = User.query.get(id)
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('api_users'))
    if request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('api_users'))
    user = User.query.get(id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
  
@app.route('/api/users/<string:username>', methods=['GET'])
def api_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@app.route('/api/users/<string:email>', methods=['GET'])
def api_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
  
  
#   Comment 1