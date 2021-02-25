import discord , subprocess , datetime
from discord.ext import commands
from setting import *
from os import path , getcwd , chdir

from assets import CommandInjection
from assets import getIp
from assets import randomStrings
from assets import removeColors
from assets import Duplicates
from assets import removeString
from assets import logsParser
from assets import resolvedParser
from assets import fileSize
from assets import filesUploader

Client = commands.Bot(command_prefix=COMMANDS_PREFIX)

# Define globals
logsItems = logsParser.logsParser()
if not logsItems: logsItems = {}

resolvedItems = resolvedParser.resolvedParser()
if not resolvedItems: resolvedItems = {}

# Commands
@Client.command()
async def exec(ctx , *, argument):
    for ADMIN in ADMINS:
        if str(ctx.message.author) == ADMIN:
            try:
                Process = subprocess.Popen(f'{argument}' , shell=True , executable="/bin/bash" , stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                Results = Process.communicate()[0].decode('UTF-8')
                if len(Results) > 2000:
                    RandomStr = randomStrings.Genrate()

                    with open(f'messages/{RandomStr}' , 'w') as Message:
                        Message.write(Results); Message.close()
                        await ctx.send("Results: ", file=discord.File(f"messages/{RandomStr}"))
                else:
                    if Results != '': await ctx.send(f'```{Results}```')
                    else: await ctx.send(f"**The Command You Performed Didn't Return an Output.**")
            except Exception as e:
                print("Exception Happened!")
                if DEBUG == True: await ctx.send(f'Python Error: **{str(e)}**')
                else: await ctx.send("**Your Command Returned an Error.**")
            return None
        else: pass
    await ctx.send(f"**You're Not Authorized To Make Commands To The Server.**")

@Client.command()
async def nslookup(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    Results = subprocess.check_output([f'nslookup {argument}'] , shell=True).decode('UTF-8')
    await ctx.send(f'{Results}')

@Client.command()
async def whois(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    Output = subprocess.check_output([f'whois {argument}'] , shell=True).decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output); Message.close()
            await ctx.send("Whois Results: ", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send("**Whois Results:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def dig(ctx , * , argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    Output = subprocess.check_output([f'dig {argument}'] , shell=True).decode('UTF-8')
    await ctx.send("**Dig Results:**")
    await ctx.send(f"```{Output}```")
    await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def ip(ctx , *, argument):
    Message = getIp.getIp(Domain=argument)
    await ctx.send(Message)

@Client.command()
async def dirsearch(ctx , *, argument):
    Path = TOOLS['dirsearch']; MainPath = getcwd(); chdir(Path)
    await ctx.send(f"**Running Your Dirsearch Scan, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f'python3 dirsearch.py -u {argument} -e * -b' , shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')
    Output = removeColors.Remove(Output); chdir(MainPath)

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output); Message.close()
            await ctx.send("Results: ", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'Results:')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def arjun(ctx , *, argument):
    Path = TOOLS['arjun']; MainPath = getcwd(); chdir(Path)
    await ctx.send(f"**Running Your Arjun Scan, We Will Send The Results When It's Done**")
    await ctx.send(f"**Note: The Bot Won't Respond Until The Scan is Done. All Of Your Commands Now Will Be Executed After This Process is Done.")
    Process = subprocess.Popen(f'python3 arjun.py -u {argument}' , shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')
    Output = removeColors.Remove(Output); chdir(MainPath)
    Output = removeString.removeString('Processing' , Output=Output)

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output); Message.close()
            await ctx.send("**Arjun Results:**", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        targetName = argument.split(' ')[0].replace('http://' , '').replace('https://' , '')
        await ctx.send(f'Arjun Results For {targetName}:')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def gitgraber(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    Path = TOOLS['gitgraber']; MainPath = getcwd(); chdir(Path)
    await ctx.send(f"**Running Your GitGraber Scan, See gitGraber Channel For Possible Leaks**")
    _ = subprocess.Popen(f'python3 gitGraber.py -k wordlists/keywords.txt -q {argument} -d' , shell=True , stdin=None, stdout=None, stderr=None, close_fds=True)
    chdir(MainPath)

@Client.command()
async def waybackurls(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    await ctx.send(f"**Collecting Waybackurls, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"echo {argument} | waybackurls",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Waybackurls Results: {URL_}")
            else:
                await ctx.send("**Waybackurls Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'Waybackurls Results:')
        await ctx.send(f'```{Output}```')

@Client.command()
async def subfinder(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    await ctx.send(f"**Collecting Subdomains Using Subdinder, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"subfinder -d {argument} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Subfinder Results: {URL_}")
            else:
                await ctx.send("**Subfinder Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'Subfinder Results:')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def assetfinder(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    await ctx.send("**Collecting Subdomains Using Assetfinder, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"assetfinder --subs-only {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Assetfinder Results: {URL_}")
            else:
                await ctx.send("**Assetfinder Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'Results:')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def findomain(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    findomainPath = TOOLS['findomain']
    await ctx.send("**Collecting Subdomains Using Findomain, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"{findomainPath} --target {argument} --quiet",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Findomain Results: {URL_}")
            else:
                await ctx.send("**Findomain Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send("**Findomain Results:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def paramspider(ctx, *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    paramPath = TOOLS['paramspider']
    await ctx.send("**Collecting Parameters Using ParamSpider, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"python3 {paramPath}/paramspider.py -d {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    Output = removeColors.Remove(Text=Output)
    Output = Output.split('\n')
    urlsList = []
    for singleLine in Output:
        if singleLine.startswith('http'):
            urlsList.append(singleLine)
        else:
            pass

    Output = '\n'.join(urlsList)

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"ParamSpider Results: {URL_}")
            else:
                await ctx.send("**ParamSpider Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'**ParamSpider Results:**')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

# My Own Recon Data. It Isn't About You.
@Client.command()
async def recon(ctx , *, argument):
    if path.exists(f'/{USER}/{RECON_PATH}/{argument}'):
        try:
            Path = f'/{USER}/{RECON_PATH}/{argument}'.replace('//' , '/')
            Data = open(Path).read().rstrip()
            Data = removeColors.Remove(Text=Data)
            Message = f"""```{Data}```"""
        except Exception:
            Message = f"**Couldn't Find The Recon Data With This Path: {argument}**"
    else:
        Message = "**Sorry The Path You Added Doesn't Exists On Our Records**"

    if len(Message) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Message)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Recon Results: {URL_}")
            else:
                await ctx.send("**Recon Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'{Message}')

# Recon Collections
@Client.command()
async def subdomains(ctx , * , argument):
    global logsItems, resolvedItems

    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    '''
    Subdomains collections gonna use three tools
    subfinder, findomain, assetfinder

    it won't use amass until we upgrade the server. if you're a developer
    and you want to add amass. i guess you know what todo.
    '''

    await ctx.send(f"**Collecting Subdomains For {argument}, Gonna Send You It When It's Done**")

    # global paths
    findomainPath = TOOLS['findomain']

    # findomain Subdomains
    Process = subprocess.Popen(f"{findomainPath} --target {argument} --quiet",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    findomainResults = Process.communicate()[0].decode('UTF-8')

    # assetfinder Subdomains
    Process = subprocess.Popen(f"assetfinder --subs-only {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assetfinderResults = Process.communicate()[0].decode('UTF-8')

    # subfinder Subdomains
    Process = subprocess.Popen(f"subfinder -d {argument} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    subfinderResults = Process.communicate()[0].decode('UTF-8')

    # filter duplicates
    allSubdomains = findomainResults + assetfinderResults + subfinderResults
    allSubdomains = Duplicates.Duplicates(Subdomains=allSubdomains)

    # saving subdomains
    fileName = randomStrings.Genrate()
    resolvedName = randomStrings.Genrate()

    currentPath = getcwd()
    allSubdomains = '\n'.join(allSubdomains)

    with open(f'data/hosts/{resolvedName}' , 'w') as subdomainsFile:
        subdomainsFile.write(allSubdomains); subdomainsFile.close()

    # add resolved into logs
    resolvedParser.resolvedWriter(Target=argument , fileName=f"{resolvedName}\n")
    resolvedItems[argument] = resolvedName

    # validate subdomains
    Process = subprocess.Popen(f"cat data/hosts/{resolvedName} | httpx -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    httpxResults = Process.communicate()[0].decode('UTF-8')

    # saving httpx results
    with open(f'data/subdomains/{fileName}' , 'w') as subdomainsFile:
        subdomainsFile.write(httpxResults); subdomainsFile.close()

    # add results into logs
    logsParser.logsWriter(Target=argument , fileName=fileName)
    logsItems[argument] = fileName

    # send httpx results
    if len(httpxResults) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(httpxResults)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Httpx Results: {URL_}")
            else:
                await ctx.send("**Httpx Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f"**Subdomains For {argument}:**")
        await ctx.send(f'```{httpxResults}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def info(ctx , *, argument):
    global logsItems

    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    try:
        subdomainsFile = logsItems[argument]
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**Getting Subdomains Information (titles , status-codes, web-servers) for {argument} using httpx.**")
    Process = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | httpx -title -web-server -status-code -follow-redirects -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    httpxResults = Process.communicate()[0].decode('UTF-8')
    httpxResults = removeColors.Remove(Text=httpxResults)

    if len(httpxResults) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(httpxResults)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Httpx Results: {URL_}")
            else:
                await ctx.send("**Httpx Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f"**Httpx Results For {argument}:**")
        await ctx.send(f'```{httpxResults}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

# Tools collection
@Client.command()
async def nuclei(ctx, *, argument):
    global logsItems
    nucleiTemplates = TOOLS['nuclei-templates']

    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    try:
        subdomainsFile = logsItems[argument]
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**Scanning {argument} For Possible Issues Using Nuclei.**")
    Process = subprocess.Popen(f"nuclei -l data/subdomains/{subdomainsFile} -t {nucleiTemplates} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    nucleiResults = Process.communicate()[0].decode('UTF-8')
    nucleiResults = removeColors.Remove(Text=nucleiResults)

    if nucleiResults == '':
        await ctx.send(f"**Nuclei Couldn't Find Issue On {argument}**")
    elif len(nucleiResults) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(nucleiResults)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Nuclei Results: {URL_}")
            else:
                await ctx.send("**Nuclei Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f"**Nuclei Results For {argument}:**")
        await ctx.send(f'```{nucleiResults}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def subjack(ctx , *, argument):
    global resolvedItems

    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    try:
        resolvedFile = resolvedItems[argument]
        fileStr = randomStrings.Genrate()
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**Scanning {argument} For Possible Subdomains Takeover Issues Using Subjack**")
    Process = subprocess.Popen(f"subjack -w data/hosts/{resolvedFile} -t 100 -timeout 30 -o data/subjack/{argument}-{fileStr}.subjack -ssl",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    subjackResults = Process.communicate()[0].decode('UTF-8')
    subjackResults = removeColors.Remove(Text=subjackResults)

    if subjackResults == '':
        await ctx.send(f"**Subjack Couldn't Find Issue On {argument}**")
    elif len(subjackResults) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(subjackResults)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Subjack Results: {URL_}")
            else:
                await ctx.send("**Subjack Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f"**Subjack Results For {argument}:**")
        await ctx.send(f'```{subjackResults}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def subjs(ctx , *, argument):
    global logsItems

    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    try:
        subdomainsFile = logsItems[argument]
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**Extracting JS Files From {argument} Using Subjs**")
    Process = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | subjs",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    subjsResults = Process.communicate()[0].decode('UTF-8')

    if subjsResults == '':
        await ctx.send(f"**Subjs Couldn't Find Issue On {argument}**")
    elif len(subjsResults) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(subjsResults)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')

            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Subjs Results: {URL_}")
            else:
                await ctx.send("**Subjs Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f"**Subjs Results For {argument}:**")
        await ctx.send(f'```{subjsResults}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def smuggler(ctx, *, argument):
    global logsItems

    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    try:
        subdomainsFile = logsItems[argument]
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    smugglerPath = TOOLS['smuggler']
    await ctx.send(f"**Scanning {argument} For HTTP Request Smuggling Issues Using Smuggler**")

    if "http:" in argument or "https:" in argument:
        Process = subprocess.Popen(f"echo {argument} | python3 {smugglerPath}/smuggler.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        smugglerResults = Process.communicate()[0].decode('UTF-8')
    else:
        Process = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | python3 {smugglerPath}/smuggler.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        smugglerResults = Process.communicate()[0].decode('UTF-8')

    smugglerResults = removeColors.Remove(Text=smugglerResults)
    if len(smugglerResults) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(smugglerResults)
            Message.close()

            messageSize = fileSize.getSize(filePath=f'messages/{RandomStr}')

            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                URL_ = filesUploader.uploadFiles(filePath=f'messages/{RandomStr}')
                if not URL_:
                    await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                    return
                else:
                    await ctx.send(f"Smuggler Results: {URL_}")
            else:
                await ctx.send("**Smuggler Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f"**Smuggler Results For {argument}:**")
        await ctx.send(f'```{smugglerResults}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

# Showing Current Recon Data
@Client.command()
async def show(ctx):
    global logsItems

    targetsList = []
    for site,_ in logsItems.items():
        targetsList.append(site)

    targetsMessage = ', '.join(targetsList)
    await ctx.send(f"**We Have Subdomains For: {targetsMessage}**")

@Client.command()
async def count(ctx , *, argument):
    global logsItems , resolvedItems

    try:
        resolvedFile = resolvedItems[argument]
        resolvedContent = open(f'data/hosts/{resolvedFile}' , 'r').readlines()
        resolvedLength = len(resolvedContent)

        await ctx.send(f"**There's {str(resolvedLength)} Live Hosts For {argument}**")
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    try:
        subdomainsFile = logsItems[argument]
        subdomainsContent = open(f'data/subdomains/{subdomainsFile}' , 'r').readlines()
        subdomainsLength = len(subdomainsContent)

        await ctx.send(f"**There's {str(subdomainsLength)} Valid Subdomains For {argument}**")
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

# Main Event With Admin Channel Logger.
@Client.event
async def on_member_join(member):
    adminChannel = Client.get_channel(ADMIN_CHANNEL)
    await adminChannel.send(f"{member} Has Joined The Server.")

@Client.event
async def on_member_remove(member):
    adminChannel = Client.get_channel(ADMIN_CHANNEL)
    await adminChannel.send(f"{member} Has Left The Server.")

@Client.event
async def on_ready():
    Dates = datetime.datetime.now()
    Message = f"**ReconServer Started To Work On {Dates.year}-{Dates.month}-{Dates.day}**"
    adminChannel = Client.get_channel(ADMIN_CHANNEL)
    await adminChannel.send(Message)

if __name__ == "__main__":
    Client.run(DISCORD_TOKEN)
