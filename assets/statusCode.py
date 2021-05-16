from requests import get, post, put, head, options, patch, delete, request

def getCode(URL):
    response = get(URL)
    return response.status_code

def getStatusCodes(URL):
    getStatusCode = get(URL).status_code
    postStatusCode = post(URL).status_code
    putStatusCode = put(URL).status_code
    traceStatusCode = request("TRACE", URL).status_code
    headStatusCode = head(URL).status_code
    optionStatusCode = options(URL).status_code
    patchStatusCode = patch(URL).status_code
    deleteStatusCode = delete(URL).status_code
    noneStatusCode = request("ANYTHING", URL).status_code

    codesDict = {
        "GET" : getStatusCode,
        "POST" : postStatusCode,
        "PUT" : putStatusCode,
        "TRACE" : traceStatusCode,
        "HEAD" : headStatusCode,
        "OPTIONS" : optionStatusCode,
        "PATCH" : patchStatusCode,
        "DELETE" : deleteStatusCode,
        "CUSTOM" : noneStatusCode
    }

    return codesDict
