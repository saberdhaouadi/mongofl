from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import os



app = Flask(__name__)
title = "TODO application"
heading = "TODO My Daily tasks"

client = MongoClient("mongodb+srv://saber123:saber123@cluster0.auc0l.mongodb.net/mymongodbtodo?retryWrites=true&w=majority")
db = client.mymongodbtodo
todos = db.todo

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

@app.route("/list")
def lists():
    todos_1 = todos.find()
    a1="active"
    return render_template('index.html',a1=a1,todos=todos_1,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks():
    todos_1 = todos.find({"done":"no"})
    a2="active"
    return render_template('index.html',a2=a2,todos=todos_1,t=title,h=heading)

@app.route("/completed")
def completed():
    todos_1 = todos.find({"done":"yes"})
    a3="active"
    return render_template('index.html',a3=a3,todos=todos_1,t=title,h=heading)

@app.route("/done")
def done():
    id=request.values.get("_id")
    tasks=todos.find({"_id":ObjectId(id)})
    if(tasks[0]["done"]=="yes"):
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
    else:
        todos.update({"_id":ObjectId(id)},{"$set": {"done":"yes"}})
    redir=redirect_url()

    return redirect(redir)

@app.route("/action", methods=['POST'])
def action():
    name=request.values.get("name")
    desc=request.values.get("desc")
    date=request.values.get("date")
    pr=request.values.get("pr")
    todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
    return redirect("/list")

@app.route("/remove")
def remove():
    key=request.values.get("_id")
    todos.remove({"_id":ObjectId(key)})
    return redirect("/")

@app.route("/update")
def update():
    id=request.values.get("_id")
    task=todos.find({"_id":ObjectId(id)})
    return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3():
    name=request.values.get("name")
    desc=request.values.get("desc")
    date=request.values.get("date")
    pr=request.values.get("pr")
    id=request.values.get("_id")
    todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date,   "pr":pr }})
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    key=request.values.get("key")
    refer=request.values.get("refer")
    if(key=="_id"):
        todos_1 = todos.find({refer:ObjectId(key)})
    else:
        todos_1 = todos.find({refer:key})
    return render_template('searchlist.html',todos=todos_1,t=title,h=heading)

if __name__ == "__main__":
    app.run()
