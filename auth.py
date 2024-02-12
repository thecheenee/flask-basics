from flask import render_template, session, request, redirect, flash
from app import *
from model import *
from helpers import *
import hashlib

# User Authentication Methods

@app.route("/login", methods=["GET","POST"])
def user_auth():
  if "user_id" in session:
    session.pop("user_id")
    session.pop("name")
  if request.method=="POST":
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode())
    print(password.hexdigest())

    if not is_email_valid(username):
      return render_template("sign_in.html", user_error=True)
    else:
      user = User.query.filter_by(name=username, password=password.hexdigest()).first()
      if user:
        session["user_id"] = user.id
        session["name"] = user.name
        print(session["user_id"])
        print("authentication done")
        return redirect("/")
      else:
        print('Not found!')
        return render_template("sign_in.html", pasw_error=True)
  else:
    return render_template("sign_in.html")
  
@app.route("/register", methods=["GET","POST"])
def register_user():
  if "user_id" in session:
    session.pop("user_id")
    session.pop("name")
  
  if request.method=="POST":
    username=request.form['username']
    password=request.form['password']
    cpassword=request.form['cpassword']
    type = 'user'
    if not is_email_valid(username):
      return render_template("sign_up.html", user_error=True)
    else:
      if username.split('@')[1] == 'admin.com':
        type = 'admin'
      if len(password) < 5:
        return render_template("sign_up.html", pasw_error=True)
      if password!=cpassword:
        return render_template("sign_up.html", nomatch_error=True)
      try:
        existing_user_check = User.query.filter_by(name=username).first()
        if existing_user_check and existing_user_check.name == username:
          return render_template("sign_up.html", exists_error=True)
        new_user = User(name=username, password=password, type=type)
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        user = User.query.filter_by(name=username, password=password).first()
        if user:
          session["user_id"] = user.id
          session["name"] = user.name
          print(session["user_id"])
          print("authentication done")
          return redirect("/")
      except Exception as e:
        print("rollback", e)
        db.session.rollback()
        return redirect("/")
  else:
    return render_template("sign_up.html")
  
@app.route('/logout', methods=["GET","POST"])
def user_logout():
  if "user_id" in session:
    session.pop("user_id")
    session.pop("name")
    return redirect("/")
  else:
    return redirect("/")