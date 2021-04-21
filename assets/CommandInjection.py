import re

def commandInjection(argument , RCE):
    for char in argument:
        if char in RCE: return False
    
    argumentFinder = re.search(r"(..*\-|^\-)[a-zA-Z]", argument)
    if argumentFinder != None:
        argument = argument.split(' ')[1].strip()
        if argument.startswith('https://'):
            return True
        elif argument.startswith('http://'):
            return True
        else:
            return False
    else:
        return True
