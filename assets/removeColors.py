import re

def Remove(Text):
    Escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return Escape.sub('' , Text)