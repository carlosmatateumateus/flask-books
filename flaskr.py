from sqlite3 import connect
from flask import Flask, g, request
from contextlib import closing
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)

load_dotenv() # Load all env variables...

app.config.from_pyfile('config.cfg', silent=True)
app.secret_key = getenv('SECRET_KEY')

def init_db():           
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as f:
      db.cursor().executescript(f.read().decode('utf-8'))
    db.commit()

def connect_db():
  return connect(app.config['DATABASE'])

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardow_request(exception):
  if (request.method in ['POST', 'PUT']):
    g.db.commit()
  g.db.close()

init_db() # Create database structure