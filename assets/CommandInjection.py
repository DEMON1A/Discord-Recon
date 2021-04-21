import re

def commandInjection(argument , RCE):
    for char in argument:
        if char in RCE: return False
    
    argumentFinder = re.search(r"(..*\-|^\-)[a-zA-Z]", argument)
    if argumentFinder != None:
        return False
    else:
        return True
