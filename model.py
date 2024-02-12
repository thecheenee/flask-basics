from app import db

class Todo(db.Model):
  __tablename__="todo"

  id = db.Column('id', db.Integer, primary_key = True)
  user_id = db.Column('user_id', db.Integer)
  title = db.Column(db.String(100))
  description = db.Column(db.String(250))
  created_on = db.Column(db.String(100))

class User(db.Model):
  __tablename__="user"

  id = db.Column('id', db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  password = db.Column(db.String(100))
  type = db.Column(db.String(100))

class UserTodo(db.Model):
  __tablename__="user_todo_vw"

  userid = db.Column('userid', db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  tasks = db.Column(db.Integer)