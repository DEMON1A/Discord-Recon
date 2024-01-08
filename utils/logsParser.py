from os import path
from settings import BASE_PATH

# Define globals
logsItems = {}
logsBase = f'{BASE_PATH}/logs/targets.log'

def logsExists():
    return path.exists(logsBase)

def logsParser():
    global logsItems

    if not logsExists():
        open(logsBase , 'a').close()

    logsContent = open(logsBase, 'r').readlines()
    if len(logsContent) == 0:
        return False
    else:
        for singleLine in logsContent:
            singleLine = singleLine.rstrip('\n')
            items = singleLine.split('=')

            websiteName = items[0]
            fileName = items[1]

            logsItems[websiteName] = fileName

        return logsItems

def logsWriter(Target , fileName):
    with open(logsBase , 'a') as logsFile:
        logsFile.write(f"{Target}={fileName}\n")
        logsFile.close()
