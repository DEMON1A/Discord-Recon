import re
from os.path import exists
from os import mkdir
from os import popen
from assets import randomStrings

def detectContent(UserCommand):
    if UserCommand == "":
        return ''
    else:
        reGex = re.search(r'\`\`\`..*\`\`\`', UserCommand, re.DOTALL)
        if reGex:
            Code = reGex.group()
            Code = Code[:-3][4:]

            if not exists('codes/'):
                mkdir('codes/')

            if exists('codes/main.py'):
                if len(open('codes/main.py').read()) != 0:
                    rString = randomStrings.Genrate()
                    with open(f'codes/main-{rString}.py', 'w') as oPyCode:
                        oPyCode.write(open('codes/main.py').read())
                        oPyCode.close()

            with open('codes/main.py', 'w') as pyCode:
                pyCode.write(str(Code))
                pyCode.close()

            commandResults = popen('python3 codes/main.py').read()
            return commandResults
        else:
            return ''
