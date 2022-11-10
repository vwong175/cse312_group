from flask import Flask, render_template, url_for, request, session, redirect
from server import app
from models import User

@app.route('/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/', methods=['POST'])
def changeToSignup():
  return redirect('/signup', code= 302)

@app.route('/profile/signout')
def signout():
  return User().signout()

@app.route('/login', methods=['POST'])
def login():
  return User().login()