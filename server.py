# nrd_2020 Portfolio MAIN Server Script
# MySQL convert to SQL Alchemy for Flask/AWS Deployment.
# Neil Denning



from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
from flask_bcrypt import Bcrypt
from datetime import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

'''
C - create - INSERT
R - read - SELECT
U - update - UPDATE
D - delete - DELETE
'''

app = Flask(__name__)
app.secret_key = "nrd_key"
bcrypt = Bcrypt(app)
database = "belt_exam"


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/register", methods=["POST"])
def register_user():
    is_valid = True
    
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters long")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters long")
    if len(request.form['password']) < 3:
        is_valid = False
        flash("Password must be at least 3 characters long")
        
    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Passwords must match")

    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please use a valid email address")
    
    if is_valid:
        pass_hash = bcrypt.generate_password_hash(request.form['password'])
        mysql = connectToMySQL(database)

        query = "INSERT INTO users (first_name, last_name, email, password_hash, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pass_hash)s, NOW(), NOW())"
       
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],            
            'email': request.form['email'],
            'pass_hash': pass_hash,
        }
      
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id

        return redirect("/landing")
    else:
        return redirect("/")


@app.route("/login", methods=["POST"])
def login_user():
    is_valid = True

    if len(request.form['email']) < 1:
        is_valid = False
        flash("Please enter your email")

    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please use a valid email address")

    if len(request.form['password']) < 1:
        is_valid = False
        flash("Please enter your password")
    
        
    if is_valid:
        mysql = connectToMySQL(database)
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        data = {
            'email': request.form['email']
        }
        user = mysql.query_db(query, data)
        if user:
            hashed_password = user[0]['password_hash']
            if bcrypt.check_password_hash(hashed_password, request.form['password']):
                session['user_id'] = user[0]['id']
                return redirect("/landing")
            else:
                flash("Password is invalid")
                return redirect("/")
        else:
            flash("Please use a valid email address")
            return redirect("/")
    else:
        return redirect("/")
            

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/landing")
def landing():
    if 'user_id' not in session:
        return redirect("/")

    mysql = connectToMySQL(database)
    query = "SELECT * FROM users WHERE id = %(user_id)s"
    data = {'user_id': session['user_id']}
    user = mysql.query_db(query, data)

    mysql = connectToMySQL(database)
    query = "SELECT * FROM quotes LEFT JOIN users ON quotes.user_id = users.id LEFT JOIN likes ON quotes.id = likes.quote_id ORDER BY quotes.created_at DESC"
    quotes = mysql.query_db(query)
    
    print("*"*20)
    print(quotes)

    mysql = connectToMySQL(database)
    query = "SELECT * FROM likes WHERE user_id = %(user_id)s"
    data = {
        'user_id': session['user_id']
    }
    is_liked = mysql.query_db(query,data)
    liked_quotes = []
    print("*"*20)
    print(is_liked)
    
    for liked in is_liked:
        liked_quotes.append(liked['quote_id'])
    print("*"*20)
    print(liked_quotes)

    return render_template("/landing.html", user=user[0], quotes=quotes, liked_quotes=liked_quotes)

@app.route("/frontend_proj")
def frontend_proj():
    return render_template("frontend_proj.html")

@app.route("/backend_proj")
def backend_proj():
    return render_template("backend_proj.html")

@app.route("/jayneDoe_proj")
def jayneDoe_proj():
    return render_template("jayneDoe_proj.html")

@app.route("/aboutPython_proj")
def aboutPython_proj():
    return render_template("aboutPython_proj.html")

@app.route("/internet_proj")
def internet_proj():
    return render_template("internet_proj.html")

@app.route("/modernize_proj")
def modernize_proj():
    return render_template("modernize_proj.html")


if __name__=="__main__":
    app.run(debug=True)



'''<<<<<
Flask.redirect(location, statuscode, response)

"location" = URL where response should be directed.

"statuscode" = statuscode sent to browser's header.

"response" = response parametwer used to instantiate response.

"Statuscodes"

STATUS CODES

HTTP_300_MULTIPLR_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED

FLASK.ABORT(CODE)

400_BAD_REQUEST
401_UNATHENTICATED
403_FORBIDDEN
404_NOT_FOUND
406_NOT_ACCEPTABLE
415_UNSOPPORTED_MEDIA_TYPE
429_TOO_MANY_REQUESTS



"host" = hostname to listen to. Defaults to 127.0..0.1 (localhost).
Set to '0.0.0.0' to have server available externally.

"port" = defaults to 5000. this can be changed as well.

"debug" = defaults to false. if set to true, provides debug information.

"options" = to be forwarded to underlying Werkzeug server,

"HTTP Protocol Methods" <<<<<

"GET" = Sends data in unencrypted form to server

"HEAD" = Same as GET, but without response body

"POST" = Used to send HTML form data to server.

"PUT" = Replaces all current representations of target resource with uploaded content.

"DELETE" = Removes all current representations of target resource given by URL.



"additional parameters" <<<<<

"int" = accepts integer

"float" = for floating point value

"path" = accepts slashes uswed as directory separator

"JINJA template engine uses the following delimiters for escaping from HTML"

{%...%} for Statements

{{...}} for Expressions to print to the template output

{#...#} for Comments not included in the template output

#...## for Line Statements


"REQUEST OBJECT"

"Form" = Dictionary object containing key-value pairs of form parameters and values.

"args" = Parsed contents of query string which i spart of URL after question mark(?)

"Cookies" = Dictionary object holding Cookie names and values. Helps with tracking data.

"files" = Data pertaining to the upload file.

"Method" = Current request method.



'''
