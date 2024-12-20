import config
import requests
import base64
import dropbox
import re
# import weasyprint
import time
from dropbox.files import WriteMode
from pymongo import MongoClient



client = MongoClient(config.mongo_str)
db = client.get_database('notes')
records = db.sync
editor_record = db.notes_data

def get_file_extension(filename):
    # Use a regular expression to search for the pattern of a file extension
    match = re.search(r'\.([^.]+)$', filename)
    if match:
        # Return the file extension if the pattern was found
        return match.group(1)
    else:
        # Return None if the pattern was not found
        return None


def MyStuff(token):
    dbx = dropbox.Dropbox(token)

    dp_files = {}

    file_exist = False
    for entry in dbx.files_list_folder('').entries:
        if entry.name == 'Notes-817':
            file_exist = True

    if not file_exist:
        dbx.files_create_folder('/Notes-817')

    for entry in dbx.files_list_folder('/Notes-817').entries:
        url = dbx.sharing_create_shared_link(entry.path_display).url

        url, _ = url.split("?")
        type = get_file_extension(url)

        url = url+"?raw=1"

        size = entry.size
        size = (size/1024)/1024
        size = round(size, 2)
        size = str(size)+' MB'

        dp_files[entry.name] = [url, size, entry.path_display, type]

    return dp_files


def validate_token(token):

    header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "query": "balls"
    }

    r = requests.post("https://api.dropboxapi.com/2/check/user",
                      headers=header, json=data)
    if r.status_code == 200:
        return True
    else:
        return False


def RefreshToken(refresh_token):
    client_creds = f"{config.drop_box_id}:{config.drop_box_pwd}"
    client_creds_bs64 = base64.b64encode(client_creds.encode())

    headers = {
        "Authorization": f"Basic {client_creds_bs64.decode()}"
    }

    data = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    r = requests.post("https://api.dropboxapi.com/oauth2/token",
                      headers=headers, data=data)

    stuff = r.json()
    access_token = stuff["access_token"]
    return access_token


def DeleteFile(token, path):
    try:
        dbx = dropbox.Dropbox(token)
        dbx.files_delete(path)
        return True
    except Exception as E:
        print(E)
        return False


def write_file_to_dropbox(token, path, file_contents):
    # Create a Dropbox API client using the access token
    dbx = dropbox.Dropbox(token)
    # Use the files_upload() method to write the file to Dropbox
    dbx.files_upload(file_contents, path, mode=WriteMode.overwrite)


def SyncStuff(email):

    result = records.find_one({"email":email})

    if not result:
        records.insert_one({"email":email,"sync_time":time.ctime()})
        return '0'
    else:
        return result["sync_time"]


def SyncThings(token, email):
    file_exist = False
    file2_exist = False
    dbx = dropbox.Dropbox(token)
    for entry in dbx.files_list_folder('').entries:
        if entry.name == 'Notes-html':
            file_exist = True
        if entry.name == 'Notes-pdf':
            file2_exist = True

    if not file_exist:
        dbx.files_create_folder('/Notes-html')

    if not file2_exist:
        dbx.files_create_folder('/Notes-pdf')

    result = editor_record.find({"email":email})
    
    files = []
    editor_data = []
    for i in result:
        files.append(i["filename"])
        editor_data.append(i["editor_data"].encode('utf-8'))

    # html
    for g in range(len(files)):
        path = '/Notes-html/'+files[g]+".html"
        
        dbx.files_upload(f=editor_data[g],path=path, mode=WriteMode.overwrite)
        
        headers = {
            'Content-Type': 'application/json',
        }

        params = {
            'pwd': config.db_pwd,
        }

        json_data = {
            'editor_data': editor_data[g].decode('utf-8'),
        }

        response = requests.post(
            'https://myapiservices.moosa817.repl.co/convert_html_to_pdf',
            params=params,
            headers=headers,
            json=json_data,
        )

        pdf = response.json()
        b_pdf = pdf["url"].split(",")[1]
        pdf_data = b_pdf.encode()
        
        pdf_bytes = base64.b64decode(pdf_data)

        pdf_path = '/Notes-pdf/'+files[g]+".pdf"
        dbx.files_upload(f=pdf_bytes,path=pdf_path, mode=WriteMode.overwrite)

    mytime = time.ctime()

    records.update_one({"email":email},{"$set":{"sync_time":mytime}})
    return mytime

#using dropbox as service for uploading pfp using own token
def upload_pfp(token,path,file_contents):
    dbx = dropbox.Dropbox(token)
    g=[]
    for entry in dbx.files_list_folder('/projects/notes').entries:
        g.append(entry.name)
        counter = 0
    while path in g:
        counter = counter + 1
        match = re.match(r'(.+)\.([^.]+)$', path)
        name = match.group(1)
        ext = match.group(2)
        path = f"{name}{counter}.{ext}"

    path = "/projects/notes/" + path
    dbx.files_upload(file_contents, path, mode=WriteMode.overwrite)


    url = dbx.sharing_create_shared_link(path).url
    url = url.replace("?dl=0","?raw=1")
    return url