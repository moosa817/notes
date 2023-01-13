import mysql.connector
from flask import session, request, blueprints, redirect, url_for, render_template
import config
import bcrypt
import random
import requests


def Email_To(email):
    random_no = random.randrange(1, 10**6)

    headers = {
        'Authorization': f'Bearer {config.courier_api}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = """{"message": {"to": {"email":"%s"},
    "content": { "title": "Change Your Password!",  "body": "Your Verification Code is {{code}}"},"data": {"code": %s }}}""" % (email, random_no)

    response = requests.post(
        'https://api.courier.com/send', headers=headers, data=data)
    return random_no


login_page = blueprints.Blueprint(
    'login', __name__, static_folder='static', template_folder='templates')

reset_page = blueprints.Blueprint(
    'reset_page', __name__, static_folder='static', template_folder='templates')


@login_page.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index.index"))
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
                return render_template("login.html", error="Username or Email doesn't exist", umail=umail, pwd=pwd)

            try:
                index = emails.index(form1)
            except:
                index = users.index(form1)

            hashed_pwd = pwds[index]
            pwd = pwd.encode('UTF-8')
            hashed_pwd = hashed_pwd.encode("UTF-8")
            if bcrypt.checkpw(pwd, hashed_pwd):
                session["username"] = users[index]
                session["email"] = emails[index]
                session["verified"] = email_verifications[index]
                session["pfp"] = pfps[index]
                return redirect(url_for("index.index"))
            else:
                return render_template("login.html", error="Wrong password", umail=umail)

        return render_template("login.html")


@reset_page.route("/reset", methods=["GET", "POST"])
def reset():
    if session.get("username"):
        return redirect(url_for("index.index"))
    else:
        if request.method == 'POST':
            if request.form.get('umail'):
                umail = request.form['umail']
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
                    return render_template("reset.html", error="Username or Email doesn't exist", umail=umail)

                try:
                    index = emails.index(form1)
                except:
                    index = users.index(form1)

                email = emails[index]
                session["code"] = Email_To(email)
                session["email"] = email

                return render_template("reset.html", code=session["code"], email=session["email"])

            if request.form.get('code'):
                code = request.form["code"]
                if int(code) == int(session["code"]):
                    session["change_pwd"] = True
                    return render_template("reset.html", change_pwd=True, email=session["email"], code=session["code"])
                else:
                    return render_template("reset.html", error="Wrong Code", umail=session["email"], code=session["code"])

            if request.form.get('pwd1'):
                pwd1 = request.form["pwd1"]
                pwd2 = request.form["pwd2"]
                if pwd1 == "" or pwd2 == "":
                    return render_template("reset.html", change_pwd=True, email=session["email"], code=session["code"], error="Field empty")
                elif len(pwd1) > 150:
                    return render_template("reset.html", change_pwd=True, email=session["email"], code=session["code"], error="Too Long")
                elif len(pwd1) < 8:
                    return render_template("reset.html", change_pwd=True, email=session["email"], code=session["code"], error="Password Too Short")
                elif pwd1 != pwd2:
                    return render_template("reset.html", change_pwd=True, email=session["email"], code=session["code"], error="Passord Do not match")
                else:
                    pwd = pwd1.encode('utf-8')
                    new_hash = bcrypt.hashpw(pwd, bcrypt.gensalt())
                    new_hash = new_hash.decode('utf-8')

                    conn = mysql.connector.connect(
                        host=config.host,
                        user=config.user,
                        passwd=config.passwd,
                        database=config.database)
                    cursor = conn.cursor()
                    sql = "UPDATE notes SET password='%s' WHERE email='%s'"
                    val = (new_hash, session["email"])

                    cursor.execute(sql % val)
                    conn.commit()
                    conn.close()
                    return render_template("reset.html", change_pwd=True, email=session["email"], code=session["code"], success="Password Updated", reseted=True)

        return render_template("reset.html")
