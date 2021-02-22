import random , string

def Genrate():
    Chars = string.ascii_lowercase + string.ascii_uppercase
    RandomStr = ''.join(random.choice(Chars) for i in range(12)); RandomStr += ".txt"
    return RandomStr
