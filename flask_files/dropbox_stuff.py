import config
import requests
import base64
import dropbox
import re

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




        url,_ = url.split("?")
        type = get_file_extension(url)

        url = url+"?raw=1"
        



    
        size = entry.size
        size = (size/1024)/1024
        size = round(size,2)
        size = str(size)+' MB'

        dp_files[entry.name] = [url,size,entry.path_display,type]




    return dp_files

def validate_token(token):

    header = {
        "Authorization": f"Bearer {token}",
        "Content-Type":"application/json"
    }
    data = {
        "query": "balls"
    }


    r = requests.post("https://api.dropboxapi.com/2/check/user",headers=header,json=data)
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


def DeleteFile(token,path):
    dbx = dropbox.Dropbox(token)
    dbx.files_delete(path)
    return True


def write_file_to_dropbox(token, path, file_contents):
    # Create a Dropbox API client using the access token
    dbx = dropbox.Dropbox(token)
    # Use the files_upload() method to write the file to Dropbox
    dbx.files_upload(file_contents, path)