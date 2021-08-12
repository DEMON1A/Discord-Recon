from os import path
from settings import BASE_PATH

# Define globals
logsItems = {}

def logsExists():
    return path.exists(f'{BASE_PATH}/data/logs/logs.easy')

def logsParser():
    global logsItems

    if not logsExists():
        open('data/logs/logs.easy' , 'a').close()

    logsContent = open(f'{BASE_PATH}/data/logs/logs.easy', 'r').readlines()
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
    with open(f'{BASE_PATH}/data/logs/logs.easy' , 'a') as logsFile:
        logsFile.write(f"{Target}={fileName}\n")
        logsFile.close()
