import re

def commandInjection(argument , RCE):
    for char in argument:
        if char in RCE: return False
    
    argumentFinder = re.search(r"(..*\-|^\-)[a-zA-Z]", argument)
    if argumentFinder != None:
        argument = argument.split(' ')[1].strip()
        if not argument.startswith('https://') or not argument.startswith('http://'):
            return False
        else:
            return True
    else:
        return True
