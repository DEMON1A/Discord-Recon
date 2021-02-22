from os import path

def getSize(filePath):
    if path.exists(filePath):
        sizeInBytes = path.getsize(filePath)
        sizeInMegaBytes = sizeInBytes / 1000000
        fileSize = int(sizeInMegaBytes)
        if fileSize == 0: fileSize = True

        return fileSize
    else:
        return False
