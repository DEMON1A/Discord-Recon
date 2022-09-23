import discord , subprocess, sys
from discord.ext import commands
from settings import *
from datetime import datetime
from urllib.parse import urlparse
from os import path, getcwd, chdir, execl

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
from assets import subdomainsFilter
from assets import pyExecute
from assets import commandsLogger
from assets import statusCode

discordIntents = discord.Intents.default()
discordIntents.members = True
discordIntents.message_content = True

Client = commands.Bot(command_prefix=COMMANDS_PREFIX, intents=discordIntents)

# Define globals
logsItems = logsParser.logsParser()
if not logsItems or len(logsItems) == 0:
    logsItems = {}

resolvedItems = resolvedParser.resolvedParser()
if not resolvedItems or len(resolvedItems) == 0:
    resolvedItems = {}

# Bot commands 
@Client.command()
@commands.has_role(ADMIN_ROLE)
async def exec(ctx , *, argument):
    try:
        Process = subprocess.Popen(argument, shell=True, executable="/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        await ctx.send("**Your Command Returned an Error.**")

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def sudo(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"> Successfully added **{role.name}** to **{member.name}**")

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def unsudo(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"> Successfully removed **{role.name}** from **{member.name}**")

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def shutdown(ctx):
    await ctx.send("**Stoping the bot based on admin command**")
    await ctx.bot.logout()

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def restart(ctx):
    await ctx.send(f"**Restarting DisordRecon, It might take up to one minute**")
    python = sys.executable
    execl(python, python, * sys.argv)

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def compile(ctx, *, argument):
    Message = pyExecute.detectContent(argument)

    if Message != '':
        await ctx.send("**Compiled Python Code Output:**")
        await ctx.send(Message)
    else:
        await ctx.send("**The Python Code You Compiled Didn't Return an Output**")

@Client.command()
async def nslookup(ctx , *, argument):
    Results = subprocess.check_output(['nslookup', f'{argument}'] , shell=False).decode('UTF-8')
    await ctx.send(f'{Results}')

@Client.command()
async def whois(ctx , *, argument):
    Output = subprocess.check_output(['whois', f'{argument}'], shell=False).decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            await ctx.send("Whois Results: ", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send("**Whois Results:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def dig(ctx , * , argument):
    Output = subprocess.check_output(['dig', f'{argument}'] , shell=False).decode('UTF-8')
    
    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            await ctx.send("Dig Results: ", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send("**Dig Results:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def ip(ctx , *, argument):
    Message = getIp.getIp(Domain=argument)
    await ctx.send(Message)

@Client.command()
async def statuscode(ctx, *, argument):
    URLparts = urlparse(argument)
    URLscheme = URLparts.scheme

    if URLscheme == '':
        argument = f"http://{argument}"
    elif URLscheme not in ["http", "https"]:
        await ctx.send("**The URL scheme you're using isn't allowed**")
        return
    else:
        pass

    statusCodeDict = statusCode.getStatusCodes(argument)
    Message = ""

    for method,code in statusCodeDict.items():
        Message += f"{method}: {str(code)}\n"

    await ctx.send(Message)

@Client.command()
async def prips(ctx, *, argument):
    Output = subprocess.check_output(['prips', f'{argument}'] , shell=False)
    Output = Output.decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            await ctx.send("Prips Results: ", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send("**Prips Results:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\n**- {ctx.message.author}**")

# Tools commands
@Client.command()
async def dirsearch(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    fileName = randomStrings.Genrate()

    dirsearchPath = TOOLS['dirsearch']
    chdir(dirsearchPath)

    await ctx.send(f"**Running Your Dirsearch Scan, We Will Send The Results When It's Done**")
    _ = subprocess.Popen(f'python3 dirsearch.py -u {argument} -e "*" -o {BASE_PATH}/messages/{fileName} && python3 {BASE_PATH}/notify.py --mode 2 -m "Dirsearch results:" -f "- {ctx.message.author}" --file {fileName}', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    
    chdir(BASE_PATH)
    await ctx.send("**Dirsearch just started, The results gonna be sent when the process is done**")

@Client.command()
async def arjun(ctx , *, argument):
    if not CommandInjection.commandInjection(argument=argument , RCE=RCE):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    await ctx.send(f"**Running Your Arjun Scan, We Will Send The Results When It's Done**")
    await ctx.send(f"**Note: The Bot Won't Respond Until The Scan is Done. All Of Your Commands Now Will Be Executed After This Process is Done.")
    Process = subprocess.Popen(f'arjun -u {argument}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')
    Output = removeColors.Remove(Output)
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

@Client.command()
async def trufflehog(ctx, *, argument):
    if not CommandInjection.commandInjection(RCE=RCE, argument=argument):
        await ctx.send("**Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return 

    # URL validation
    urlParsed = urlparse(argument)
    urlHost = urlParsed.netloc
    if urlHost != "github.com" and urlHost != "gitlab.com":
        await ctx.send("**You're trying to scan unallowed URL, please use a github/gitlab URL.**")
        return
    
    urlScheme = urlParsed.scheme
    if urlScheme not in ["http", "https"]:
        await ctx.send("**You're trying to scan unallowed URL, please use a github/gitlab URL.**")
        return

    # status code validation
    statusCodeInteger = statusCode.getCode(argument)
    if statusCodeInteger == 404:
        await ctx.send("**The project you're trying to scan doesn't exists, double check the URL**")
        return

    await ctx.send(f"**Scanning {argument} for possible data leaks using truffleHog**")
    _ = subprocess.Popen(f"trufflehog --regex --entropy=False {argument} | python3 notify.py --mode 1 -m 'truffleHog Results:' -f '- {ctx.message.author}'", shell=True , stdin=None, stdout=None, stderr=None, close_fds=True)
    await ctx.send(f"**pyNotify gonna send the results when it's done**")

@Client.command()
async def gitls(ctx, *, argument):
    if not CommandInjection.commandInjection(RCE=RCE, argument=argument):
        await ctx.send("Your Command Contains Unallowed Chars. Don't Try To Use It Again.**")
        return

    await ctx.send("**Collecting github projects using gitls**")
    Process = subprocess.Popen(f"echo https://github.com/{argument} | gitls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
                    await ctx.send(f"Gitls Results: {URL_}")
            else:
                await ctx.send("**Gitls Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    elif len(Output) == 0:
        await ctx.send(f"**Gitls didn't reutrn an output for your command**")
    else:
        await ctx.send(f'**Gitls Results:**')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

# My Own Recon Data. It Isn't About You.
@Client.command()
async def recon(ctx , *, argument):
    if path.exists(f'/{USER}/{RECON_PATH}/{argument}'):
        try:
            Path = f'/{USER}/{RECON_PATH}/{argument}'.replace('//' , '/').replace('..', '')
            Data = open(Path).read().rstrip()
            Data = removeColors.Remove(Text=Data)
            Message = f"""```{Data}```"""
        except Exception:
            Message = f"**Couldn't Find The Recon Data With This Path: {argument}**"
    else:
        Message = "**Sorry The Path You Added Doesn't Exists On Our Records**"

    if len(Message) > 2000:
        RandomStr = randomStrings.Genrate()

        with open(f'messages/{RandomStr}' , 'w') as writerHere:
            writerHere.write(Message)
            writerHere.close()

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
async def subdomains(ctx ,* , argument):
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
    allSubdomains = subdomainsFilter.vSubdomains(sList=allSubdomains, huntingTarget=argument)

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

    try:
        subdomainsFile = logsItems[argument]
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**Scanning {argument} For Possible Issues Using Nuclei.**")
    if DISABLE_NUCLEI_INFO:
        _ = subprocess.Popen(f"nuclei -l data/subdomains/{subdomainsFile} -t {nucleiTemplates} -silent | grep -v 'info.*\]' | python3 notify.py --mode 0 --discord-webhook {NUCLEI_WEBHOOK}",shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
    else:
         _ = subprocess.Popen(f"nuclei -l data/subdomains/{subdomainsFile} -t {nucleiTemplates} -silent | python3 notify.py --mode 0 --discord-webhook {NUCLEI_WEBHOOK}", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
    await ctx.send("**Results gonna be sent to nuclei webhook channel**")

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
    _ = subprocess.Popen(f"subjack -w data/hosts/{resolvedFile} -t 100 -timeout 30 -o data/subjack/{argument}-{fileStr}.subjack -ssl | python3 notify.py --mode 1 -m 'Subjack results:' -f '- {ctx.message.author}'", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)

    await ctx.send(f"**Results gonna be sent to the results channel soon**")

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
    _ = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | subjs | python3 notify.py --mode 1 -m 'Subjs results:' -f '- {ctx.message.author}'", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
    await ctx.send(f"**Results gonna be sent soon on the results channel**")

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
@commands.has_role(ADMIN_ROLE)
async def show(ctx):
    global logsItems

    targetsList = []
    for site,_ in logsItems.items():
        targetsList.append(site)

    targetsMessage = '\n'.join(targetsList)
    await ctx.send(f"**Available records: \n\n{targetsMessage}**")

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def count(ctx , *, argument):
    global logsItems , resolvedItems

    try:
        resolvedFile = resolvedItems[argument]
        resolvedContent = open(f'data/hosts/{resolvedFile}' , 'r').readlines()
        resolvedLength = len(resolvedContent)
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use ** `.subdomains [TARGET]` ** Then try again.**")
        return

    try:
        subdomainsFile = logsItems[argument]
        subdomainsContent = open(f'data/subdomains/{subdomainsFile}' , 'r').readlines()
        subdomainsLength = len(subdomainsContent)
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**{argument}:\n\t\tResolved hosts: {str(resolvedLength)}\n\t\tLive subdomains: {str(subdomainsLength)}**")

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def history(ctx):
    commandsContent = open('data/logs/commands.easy', 'r').read()
    await ctx.send(f"**DiscordRecon gonna send you the results in DM**")

    if len(commandsContent) < 2000:
        await ctx.message.author.send('**Users Commands:**')
        await ctx.message.author.send(f'```{commandsContent}```')
    else:
        RandomStr = randomStrings.Genrate()
        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(commandsContent)
            Message.close()

        await ctx.message.author.send("**Users Commands:**", file=discord.File(f"messages/{RandomStr}"))

# Main Event With Admin Channel Logger.
@Client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("**Invalid command, please type `.help` to see the list of commands and tools.**")
    elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send("**You don't have permession to use this command, role is required**")
    else:
        await ctx.send(f"**Unknown error: {error}**")

@Client.event
async def on_command(ctx):
    Author = ctx.author
    Command = ctx.command
    Message = ctx.message.content

    Date = datetime.now()
    Date = f"{Date.year}:{Date.month}:{Date.day}"

    commandsLogger.logCommand(Command, Author, Date, Message)

@Client.event
async def on_member_join(member):
    welcomeMessage = f"""```
    Welcome to Discord-Recon, a discord bot created to help bug bounty hunters with thier reconnaissance process from discord using simple commands
    You can use the bot on the server, or if you wanna keep your recon data private you can always use the bot commands on the chat here 

    In case you wanna host your own discord-recon server you can always use the source code at https://github.com/DEMON1A/Discord-Recon
    And you can always support us at https://www.patreon.com/MohammedDief or https://paypal.me/MohammedDieff 
    All of the donations goes for upgrading the server, and paying some of the VPS monthly payment
    ```"""
    await member.send(welcomeMessage)

@Client.event
async def on_member_remove(member):
    adminChannel = Client.get_channel(ADMIN_CHANNEL)
    await adminChannel.send(f"**{member}** has left the server.")

@Client.event
async def on_ready():
    adminChannel = Client.get_channel(ADMIN_CHANNEL)
    Dates = datetime.now()
    Message = f"**ReconServer started to work at {Dates.year}-{Dates.month}-{Dates.day}**"
    await adminChannel.send(Message)

if __name__ == "__main__":
    Client.run(DISCORD_TOKEN)
