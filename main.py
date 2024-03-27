from flask import Flask, render_template, redirect, request, flash, url_for
import flask, random, string, os
from deta import Deta

app = Flask(__name__)
app.secret_key = "kys"
db = Deta(os.environ["DETA_KEY"]).Base("URLShortener")

def checkKey(key):
  if len(key) == 5:
    check = db.get(key)
    if not check:
      return False
    else:
      return check["url"]
  else:
    return False

def generateKey():
  key = ''.join(random.choices(string.ascii_letters+string.digits,k=5))
  if checkKey(key):
    generateKey()
  else:
    return key
    
def insertData(key, url):
  try:
    db.insert({"url":url},key)
    return True
  except:
    return False
    
@app.route("/",methods=["GET","POST"])
def index():
  if request.method == "POST":
    url = request.form["url"]
    if not url:
      flash('URL is required!')
      return redirect(url_for('index'))
    key = generateKey()
    insert = insertData(key, url)
    return render_template("index.html",url=request.base_url+key)
    
  return render_template("index.html")
  
@app.route("/<key>")
def redirectFunc(key):
  url = checkKey(key)
  if not url:
    return render_template("404.html")
  else:
    return redirect(url)

app.run()