#--- arquivo de rotas
from flask import Flask, render_template, request, url_for, session, jsonify
from flask_session import Session
import main
data=main.Data()
app=Flask(__name__)
app.config["SESSION_PERMANENT"]=data.conf.sysSession["PERMANENT"]
app.config["SESSION_TYPE"]=data.conf.sysSession["TYPE"]
app.config["SESSION_FILE_DIR"]=data.conf.sysSession["FOLDER"]
app.config["SESSION_FILE_THRESHOLD"]=data.conf.sysSession["MAX"]
app.config["PERMANENT_SESSION_LIFETIME"]=data.conf.sysSession["LIFETIME"]
Session(app)

@app.route("/")
def Home(): return render_template("index.html",data=conect())

@app.route("/<page>")
def Page(page): return render_template("index.html",data=conect(page))

@app.route("/<page>/<detail>")
def Detail(page,detail): return render_template("index.html",data=conect(page,detail))

@app.route("/<page>/<detail>/<description>")
def Description(page,detail,description): return render_template("index.html",data=conect(page,detail,description))

@app.route("/<page>/<detail>/<description>/<information>")
def Information(page,detail,description,information): return render_template("index.html",data=conect(page,detail,description,information))

@app.route("/listener",methods=['GET','POST'])
def Listener():return data.listener(request.get_json())

def conect(page = 'inicio',detail ='',description = '',information = ''):
    if not session.get("sid"): session["sid"]=data.conf.getSid()
    return(data.conect(session["sid"],[page,detail,description,information]))

if __name__== "__main__": app.run(debug=True)