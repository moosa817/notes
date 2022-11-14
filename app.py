from flask import Flask,render_template,request
import re
# create flask app
app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mynotes")
def notes():
    return render_template("notes.html")

@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        pwd = request.form['pwd1']
        confirm_pwd = request.form['pwd2']

        emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        userRegex = "^[a-zA-Z0-9_.-]+$"

        print(username,email,pwd,confirm_pwd)

        if username == "" or email == "" or pwd == "" or confirm_pwd == "":
            return render_template("signup.html",error="Please fill out all the forms")
        elif len(pwd) < 8:
            return render_template("signup.html",error="Password must be at least 8 characters long")
        elif pwd != confirm_pwd:
            return render_template("signup.html",error="Passwords do not match")
        # check for email 
        elif not re.match(emailRegex,email):
            return render_template("signup.html",error="Please enter a valid email address")
        # check for username
        elif not re.match(userRegex,username):
            return render_template("signup.html",error="Please enter a valid username")
        
            
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5000)