import os
import sqlalchemy
from sqlalchemy.sql import text

from datetime import datetime
from flask import Blueprint, Flask, flash, redirect, render_template, request, session
from flask_session import Session

#my helper functions
from app.helpers import apology, login_required
from app.models.account import Account, AccountException

birdserver = Blueprint('main', __name__)

@birdserver.route('/test')
def test_page():
    return '<h1>Testing the birdserver app</h1>'

@birdserver.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@birdserver.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")

@birdserver.get("/register")
def register_get():
    return render_template("register.html")

@birdserver.post("/register")
def register_post():
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure password and confirmation match
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords must match", 400)
    
    try:
        account = Account.create(request.form.get("username"), request.form.get("password"))
    except AccountException as e:
        return apology(str(e), 400)

    # Redirect user to home page
    return redirect("/")

@birdserver.get('/login')
def login_get():
    return render_template("login.html")

@birdserver.post('/login')
def login_post():

    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)
    
    try:
        Account.login(request.form.get("username"), request.form.get("password"))
    except AccountException as e:
        return apology(str(e), 400)
    
    return redirect("/")


@birdserver.route("/logout")
def logout():

    Account.logout()
    
    # Redirect user to login form
    return redirect("/")
