from flask import session, request, blueprints, jsonify, render_template, redirect
import re
import config
# import weasyprint
import base64
from pymongo import MongoClient
import requests


client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.notes_data




index_edit_page = blueprints.Blueprint(
    'index_edit_page', __name__, static_folder='static', template_folder='templates')

view_page = blueprints.Blueprint(
    'view_edit_page', __name__, static_folder='static', template_folder='templates')

download_name_page = blueprints.Blueprint(
    'download_name_page', __name__, static_folder='static', template_folder='templates')


delete_name_page = blueprints.Blueprint(
    'delete_name_page ', __name__, static_folder='static', template_folder='templates')


@index_edit_page.route("/edit_name", methods=["POST", "GET"])
def edit_name():
    if request.method == "POST":
        
        file_regex = "^[ a-zA-Z0-9_.-]+$"
        input1 = request.form["input1"]
        input2 = request.form["input2"]
        new_input = input1
        original_input = input2

        if len(input1) == 0:
            return jsonify({"error": "Please Enter a name."})
        elif new_input in session["files"]:
            return jsonify({"error": "File Exists Give another name"})
        elif len(input1) > 50:
            return jsonify({'errror': "Rename failed , name too long"})
        elif not re.match(file_regex, input1):
            return jsonify({"error": "Enter a valid name."})
        else:

            index = session["files"].index(original_input)
            session["files"][index] = new_input
            # add new input to database replacing it with original input


            records.update_one({"email":session["email"],"filename":original_input},{"$set":{"filename":new_input}})
            return jsonify({"success": "renamed successfully"})


@delete_name_page.route("/delete_name", methods=["POST"])
def delete_name():
    if request.method == "POST":
        delete_input = request.form["delete_input"]
        try:
            session["files"].remove(delete_input)

            records.delete_one({"email":session["email"],"filename":delete_input})
            return jsonify({"success": True})
        except:
            return jsonify({"success": False})


@download_name_page.route("/download_name", methods=["GET", "POST"])
def download_name():
    if request.method == "POST":
        download_file = request.form["download_file"]

        result = records.find_one({"email":session["email"],"filename":download_file})

        result = result["editor_data"]

        return jsonify({"success": True, "data": result})


@view_page.route("/view")
def view_name():
    name = request.args.get("name")
    if name:
        result = records.find_one({"email":session["email"],"filename":name})
        result = result["editor_data"]
        return render_template("view.html", stuff=result, file_name=name)
    else:
        return redirect("/")


@index_edit_page.route("/download_pdf", methods=["GET", "POST"])
def dPDF():
    if request.method == "POST":
        filename = request.form["filename"]
        editor_data = request.form["editor_data"]
        # Create a PDF from the HTML text using api :)

        headers = {
            'Content-Type': 'application/json',
        }

        params = {
            'pwd': config.db_pwd,
        }

        json_data = {
            'editor_data': editor_data,
        }

        response = requests.post(
            'https://myapiservices.moosa817.repl.co/convert_html_to_pdf',
            params=params,
            headers=headers,
            json=json_data,
        )

        pdf = response.json()
        data_url = pdf["url"]
        return jsonify({"success": True, 'pdf_download': data_url})
