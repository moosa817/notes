from flask import Flask,jsonify,render_template,request,redirect,url_for,session
import re
import mysql.connector
import sqlite3
import config
import bcrypt
# create flask app
app = Flask(__name__)

app.secret_key = "super secret key"
app.url_map.strict_slashes = False

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        filename = request.form['filename']
        file_regex = "^[ a-zA-Z0-9_.-]+$"
        if re.match(file_regex, filename) and len(filename) > 0 and len(filename) < 50:
            conn = sqlite3.connect("notes_data.db")
            cur = conn.cursor()
            username = session["username"]

            res = cur.execute("SELECT * FROM editor WHERE username=:username AND filename=:filename", {"username":username, "filename":filename})

            if not res.fetchall():
                cur.execute("INSERT INTO editor (username, filename) VALUES (:username, :filename)", {"username":username, "filename":filename})
                conn.commit()
                conn.close()
                session["files"].append(filename)

                return render_template("index.html",username= session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],success="File Created",files=session["files"])
            else:
                return render_template("index.html",username= session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],error="File Already Exists",files=session["files"])
        else:
            return render_template("index.html",username= session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],error="Enter a valid filename",files=session["files"])
        
    if session.get("username"):
        username = session["username"]
        conn = sqlite3.connect("notes_data.db")
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM editor WHERE username=:username", {"username":username})

        result = result.fetchall()
        # print(result)

        files = []
        for i in result:
            files.append(i[2])

        session["files"] = files

        return render_template("index.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"])
    else:
        return render_template("index.html")


@app.route("/mynotes", methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        editor_data = request.form["editordata"]

    if session.get("username"):
        return render_template("notes.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"])
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
            val = (username,email,hash_pwd,'Default.png','False')
            cursor.execute(sql,val)
            conn.commit()
            conn.close()
            session["login"] = True
            session["username"] = username
            session["email"] = email
            session["verified"] = 'False'
            session["pfp"] = 'Default.png'
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
            else:
                return render_template("login.html",error="Wrong password",umail=umail)



        return render_template("login.html")



@app.route("/edit_name",methods=["POST","GET"])
def edit_name():
    if request.method == "POST":
        file_regex = "^[ a-zA-Z0-9_.-]+$"
        input1 = request.form["input1"]
        input2 = request.form["input2"]
        if len(input1) == 0:
            return jsonify({"error":"Please Enter a name."})
        elif len(input1) > 50:
            return jsonify({'errror':"Rename failed , name too long"})
        elif not re.match(file_regex, input1):
            return jsonify({"error": "Enter a valid name."})
        else:
            new_input = input1
            original_input = input2
            index = session["files"].index(original_input)
            session["files"][index] = new_input
            # add new input to database replacing it with original input
            conn = sqlite3.connect("notes_data.db")
            cur = conn.cursor()
            cur.execute("UPDATE editor SET filename = :new_input WHERE filename= :orignal_input",{"new_input":new_input, "orignal_input":original_input})

            conn.commit()
            conn.close()
            return jsonify({"success":"renamed successfully"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5000)