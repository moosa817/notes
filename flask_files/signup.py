import mysql.connector
from flask import session,request,blueprints,redirect,url_for,render_template
import config
import re
import bcrypt

# make a blueprints

signup_page = blueprints.Blueprint('signup', __name__,static_folder='static',template_folder='templates')

@signup_page.route("/signup",methods=['POST','GET'])
def signup():
    if session.get("username"):
        return redirect(url_for('index.index'))

    conn = mysql.connector.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        database=config.database)
    cursor = conn.cursor()
    sql = "SELECT username,email FROM notes"
    
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    usernames = []
    emails = []

    for i in range(len(result)):
        usernames.append(result[i][0])
        emails.append(result[i][1])
        

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        pwd = request.form['pwd1']
        confirm_pwd = request.form['pwd2']

        emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        userRegex = "^[a-zA-Z0-9_.-]+$"

        # print(username,email,pwd,confirm_pwd)

        if username == "" or email == "" or pwd == "" or confirm_pwd == "":
            return render_template("signup.html",error="Please fill out all the forms",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        elif len(username) > 150 or len(email) > 150 or len(pwd) >150:
            return render_template("signup.html",error="Smth too big")
        elif len(pwd) < 8:
            return render_template("signup.html",error="Password must be at least 8 characters long",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        elif pwd != confirm_pwd:
            return render_template("signup.html",error="Passwords do not match",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        # check for email 
        elif not re.match(emailRegex,email):
            return render_template("signup.html",error="Please enter a valid email address",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        # check for username
        elif not re.match(userRegex,username):
            return render_template("signup.html",error="Please enter a valid username",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        elif username in usernames:
            return render_template("signup.html",error="Username already exists",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        elif email in emails:
            return render_template("signup.html",error="Email already exists",email=email,username=username,pwd=pwd,confirm_pwd=confirm_pwd)
        else:
            pwd = pwd.encode('UTF-8')
            hash_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            # pwd = hash_pwd.decode('UTF-8')
            conn = mysql.connector.connect(
                host=config.host,
                user=config.user,
                passwd=config.passwd,
                database=config.database)
            cursor = conn.cursor()
            sql = "INSERT INTO notes (username,email,password,pfp,email_confirmation) VALUES (%s,%s,%s,%s,%s)"
            val = (username,email,hash_pwd,'static/img/Default.png','False')
            cursor.execute(sql,val)
            conn.commit()
            conn.close()
            session["login"] = True
            session["username"] = username
            session["email"] = email
            session["verified"] = False
            session["pfp"] = '/static/img/Default.png'
            return redirect(url_for("index.index"))




        
            
    return render_template("signup.html")