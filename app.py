# Project Title: NRD Portfolio "Static" Final
# MySQL convert to SQL Alchemy for Flask/AWS "Static" Deployment.
# Coder: Neil Denning


from flask import Flask, render_template, redirect, request, session, flash

from datetime import datetime

'''
C - create - INSERT
R - read - SELECT
U - update - UPDATE
D - delete - DELETE
'''

app = Flask(__name__)


@app.route("/")
def home_page():
        return render_template("mainNew.html")

@app.route("/frontend_proj")
def frontend_proj():
    return render_template("frontend_proj.html")

@app.route("/backend_proj")
def backend_proj():
    return render_template("backend_proj.html")

@app.route("/jayneDoe_proj")
def jayneDoe_proj():
    return render_template("jayneDoe_proj.html")

@app.route("/jayneDoe_original")
def jayneDoe_original():
    return render_template("jayneDoe_original.html")

@app.route("/aboutPython_proj")
def aboutPython_proj():
    return render_template("aboutPython_proj.html")

@app.route("/about_python_original")
def about_python_original():
        return render_template("aboutPython_original.html")

@app.route("/internet_proj")
def internet_proj():
    return render_template("internet_proj.html")

@app.route("/internet_original")
def internet_original():
        return render_template("internet_original.html")

@app.route("/modernize_proj")
def modernize_proj():
    return render_template("modernize_proj.html")

@app.route("/dojo_tweet_code_preview")
def dojo_tweet_code_preview():
        return render_template("dojo_tweet_code_preview.html")

@app.route("/dojo_tweet_main_preview")
def dojo_tweet_main_preview():
        return render_template("dojo_tweet_main_preview.html")

@app.route("/belt_exam_main_preview")
def belt_exam_main_preview():
        return render_template("belt_exam_main_preview.html")






if __name__ == "__main__":
        app.run(debug=True)
