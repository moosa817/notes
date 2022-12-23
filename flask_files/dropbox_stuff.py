import config
import requests
import base64
import dropbox


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
        url,_ = url.split("?")
        url = url+"?raw=1"


        dp_files[entry.name] = [url,entry.size,entry.path_display]




    print(dp_files)

def validate_token(token):

    header = {
        "Authorization": f"Bearer {token}" 
    }
    data = {
        "query": "balls"
    }


    r = requests.post("https://api.dropboxapi.com/2/check/user",headers=header,data=data)

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
        "refresh_token":refresh_token,
        "grant_type":"refresh_token"
        }


    r = requests.post("https://api.dropboxapi.com/oauth2/token",headers=headers,data=data)


    stuff = r.json()
    access_token = stuff["access_token"]
    return access_token