import requests
from os import path

def uploadFiles(filePath):
    if path.exists(filePath):
        uploadURL = "https://api.anonfiles.com/upload"
        uploadFiles = {"file": open(filePath , 'rb')}

        jsonResponse = requests.post(uploadURL , files=uploadFiles , data={}).json()
        fileURL = jsonResponse['data']['file']['url']['full']

        return fileURL
    else:
        return False
