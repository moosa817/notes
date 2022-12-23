from flask import session,request,blueprints,redirect,url_for,render_template
from pysqlcipher3 import dbapi2 as sqlite
import config
from flask import current_app
import requests
import base64
from flask_files import dropbox_stuff as Db


media_page = blueprints.Blueprint('media_page', __name__,static_folder='static',template_folder='templates')



@media_page.route("/media")
def media():
    code = request.args.get("code")
    if code:
        
        client_creds = f"{config.drop_box_id}:{config.drop_box_pwd}"
        client_creds_bs64 = base64.b64encode(client_creds.encode())

        headers = {
            "Authorization": f"Basic {client_creds_bs64.decode()}"
        }

        data = {
            "code":code,
            "grant_type":"authorization_code",
            "redirect_uri":"http://localhost:5000/media"
        }


        r = requests.post("https://api.dropboxapi.com/oauth2/token",headers=headers,data=data)


        stuff = r.json()
        if r.status_code == 200:
            access_token = stuff["access_token"]
            refresh_token = stuff["refresh_token"]

            session["refresh_token"] = refresh_token
            session["access_token"] = access_token


            Db.MyStuff(session["access_token"])



            return render_template("mymedia.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"],token=True)
        else:
            return redirect('/media')

    if session.get("access_token"):
        if Db.validate_token(session["access_token"]):
            # token is good to go 
            print("here")
            Db.MyStuff(session["access_token"])
            return render_template("mymedia.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"],token=True)
            
        else:
            # refresh token
            try:
                session["access_token"] = Db.RefreshToken(session["refresh_token"])
            except:
                return render_template("mymedia.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"],token=False)

            Db.MyStuff(session["access_token"])

            return render_template("mymedia.html",username = session["username"],email = session["email"],verified=session["verified"],pfp=session["pfp"],files=session["files"],token=True)


    return render_template("mymedia.html")