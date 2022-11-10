import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>吳致葦Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=HsuTzuYang>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>吳致葦簡介網頁</a><br>"
    homepage += "<br><a href=/account>網頁表單輸入實例</a><br>"
    homepage += "<br><a href=/read>選修課程查詢</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/about")
def about():
    return render_template("aboutme.html")

@app.route("/account", methods=["GET", "POST"])
def account():

    if request.method == "POST":

        user = request.form["user"]

        pwd = request.form["pwd"]

        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd

        return result

    else:
        return render_template("account.html")

@app.route("/read", methods=["GET", "POST"])
def read():
    result =""

    if request.method == "POST":
        keyword = request.form["keyword"]
        Leacture = request.form["Leacture"]

        collection_ref = db.collection("111")
        docs = collection_ref.get()
        for doc in docs:
            dict = doc.to_dict()
            if keyword in dict["Course"] and Leacture in dict["Leacture"]:
                result += format(dict["Leacture"])+"老師開的"+format(dict["Course"])+"課程,每週"+format(dict["Time"])+"於"+format(dict["Room"])+"上課<br>"

         if result == "":
              result = "抱歉，查無相關條件的選修課程"    

        return result
    else:
        return render_template("read.html")