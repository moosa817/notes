from flask import Flask,render_template,request,redirect,url_for,session
import re
import mysql.connector
import config
import bcrypt
# create flask app
app = Flask(__name__)

app.secret_key = "super secret key"
app.url_map.strict_slashes = False

@app.route("/")
def index():
    if session.get("username"):
        return render_template("index.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"])
    else:
        return render_template("index.html")


@app.route("/mynotes")
def notes():
    if session.get("username"):
        return render_template("index.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"])
    else:
        return render_template("notes.html")

@app.route("/signup",methods=['POST','GET'])
def signup():
    if session.get("username"):
        return redirect(url_for('index'))

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
            val = (username,email,hash_pwd,'Default','False')
            cursor.execute(sql,val)
            conn.commit()
            conn.close()
            session["login"] = True
            session["username"] = username
            session["email"] = email
            session["verified"] = 'False'
            session["pfp"] = 'Default'
            return redirect(url_for("index"))




        
            
    return render_template("signup.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))
    else:
        if request.method == 'POST':
            umail = request.form['umail']
            pwd = request.form['pwd']
            conn = mysql.connector.connect(
                host=config.host,
                user=config.user,
                passwd=config.passwd,
                database=config.database)
            cursor = conn.cursor()
            sql = "SELECT username,email,password,pfp,email_confirmation FROM notes"
            
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.commit()
            conn.close()
         
            emails = []
            users = []
            pwds = []
            email_verifications = []
            pfps = []
            for i in range(len(result)):
                users.append(result[i][0])
                emails.append(result[i][1])
                pwds.append(result[i][2])
                pfps.append(result[i][3])
                email_verifications.append(result[i][4])

            if umail in emails:
                form1 = umail
            elif umail in users:
                form1 = umail
            else:
                return render_template("login.html",error="Username or Email doesn't exist",umail=umail,pwd=pwd)


            try:
                index = emails.index(form1)
            except:
                index = users.index(form1)


            hashed_pwd = pwds[index]
            pwd = pwd.encode('UTF-8')
            hashed_pwd  = hashed_pwd.encode("UTF-8")
            if bcrypt.checkpw(pwd, hashed_pwd):
                session["username"] = users[index]
                session["email"] = emails[index]
                session["verified"] = email_verifications[index]
                session["pfp"] = pfps[index]
                return redirect(url_for("index"))



        return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5000)