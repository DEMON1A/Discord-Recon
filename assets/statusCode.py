from requests import get

def getCode(URL):
    response = get(URL)
    return response.status_code
