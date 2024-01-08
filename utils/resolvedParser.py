from os import path

# Define globals
resolvedItems = {}

def resolvedExists():
    return path.exists('data/logs/resolved.easy')

def resolvedParser():
    global resolvedItems

    if not resolvedExists():
        open('data/logs/resolved.easy' , 'a').close()

    resolvedContent = open('data/logs/resolved.easy', 'r').readlines()
    if len(resolvedContent) == 0:
        return False
    else:
        for singleLine in resolvedContent:
            singleLine = singleLine.rstrip('\n')
            items = singleLine.split('=')

            websiteName = items[0]
            fileName = items[1]

            resolvedItems[websiteName] = fileName

        return resolvedItems

def resolvedWriter(Target , fileName):
    with open('data/logs/resolved.easy' , 'a') as logsFile:
        logsFile.write(f"{Target}={fileName}")
        logsFile.close()
