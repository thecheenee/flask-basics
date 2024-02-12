from flask import render_template, session, request, redirect, flash
from app import *
from model import *
from helpers import *
from sqlalchemy import or_, func, desc
from datetime import datetime

@app.route("/")
def home():
  if "user_id" in session:
    user_id = session["user_id"]
    name = session["name"]
    todo_query = Todo.query.filter_by(user_id=user_id)
    df = True
    items = []
    view = {
      'name': '',
      'tasks': 0
    }
    if todo_query:
      df = False
      user_view_data = UserTodo.query.filter_by(userid=user_id).first()
      if user_view_data:
        view['name'] = user_view_data.name
        view['tasks'] = int(user_view_data.tasks)
      for el in todo_query:
        time_data = datetime.strftime(datetime.fromtimestamp(float(el.created_on)),"%a %b %d, %Y at %H-%M-%S")
        items.append({
          'id': el.id,
          'title':el.title,
          'desc':el.description,
          'added':time_data
        })
      # print(items)
    return render_template("index.html", login=True, username=name, items=items, empty=df, user_data=view)
  else:
    return redirect("/login")
  

@app.route("/add_item", methods=["GET","POST"])
def add_new_item():
  if "user_id" in session:
    user_id = session["user_id"]
    name = session["name"]
    if request.method=="POST":
      title=request.form['item_title']
      description=request.form['item_description']
      created_on=str(datetime.timestamp(datetime.now()))
      new_item = Todo(title=title, user_id=user_id, description=description, created_on=created_on)

      db.session.add(new_item)
      db.session.flush()
      db.session.commit()
      
      return redirect("/")
    else:
      return render_template("add_item.html", login=True, username=name)
  else:
    return redirect("/login")

@app.route("/edit_item/<int:id>", methods=["GET","POST"])
def edit_item_details(id):
  if "user_id" in session:
    user_id = session["user_id"]
    name = session["name"]
    item = Todo.query.filter_by(id=id, user_id=user_id)
    if request.method == "POST":
      
      title=request.form['item_title']
      description=request.form['item_description']
      check = [i for i in item]
      check[0].title = title
      check[0].description = description

      db.session.flush()
      db.session.commit()

      print('Item Updated')
      return redirect("/")
    else:
      # print(item[0])
      return render_template("edit_item.html", login=True, username=name, id=item[0].id, item=item[0])
  else:
    return redirect("/login")

@app.route("/delete_item/<int:id>", methods=["GET"])
def delete_selected_item(id):
  if "user_id" in session:
    user_id = session["user_id"]
    name = session["name"]
    Todo.query.filter_by(id=id, user_id=user_id).delete()
    db.session.flush()
    db.session.commit()
    return redirect("/")
  else:
    return redirect("/login")
