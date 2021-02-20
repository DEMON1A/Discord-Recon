def commandInjection(argument , RCE):
    for char in argument:
        if char in RCE: return False
    
    return True