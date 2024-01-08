import discord , subprocess, sys, psutil, asyncio
from discord.ext import commands
from settings import *
from datetime import datetime
from urllib.parse import urlparse
from os import path, getcwd, chdir, execl

from utils.uio import utilities
from utils import CommandInjection
from utils import logsParser
from utils import resolvedParser

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

# Admin only commands, Can't be used by normal users 
@Client.command()
@commands.has_role(ADMIN_ROLE)
async def exec(ctx, *, argument):
    try:
        process = subprocess.run(argument, shell=True, executable="/bin/bash", capture_output=True, text=True)
        results = process.stdout

        if len(results) > 2000:
            random_str = utilities.generate_random_string()

            with open(f'messages/{random_str}', 'w') as message_file:
                message_file.write(results)

            await ctx.send("Results:", file=discord.File(f"messages/{random_str}"))
        elif results:
            await ctx.send(f'```{results}```')
        else:
            await ctx.send("**The Command You Performed Didn't Return an Output.**")

    except subprocess.CalledProcessError as e:
        await ctx.send(f"**Error: {e.stderr.strip()}**")

    except Exception as e:
        await ctx.send("**An unexpected error occurred.**")

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
    await ctx.send("**Shutting down!**\nSomeone requested the shutdown command")
    await ctx.bot.close()

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def restart(ctx):
    await ctx.send(f"**Restarting ReconServer!**\nIt might take few minutes to restart the server.")
    execl(sys.executable, sys.executable, * sys.argv)

@Client.command()
@commands.has_role(ADMIN_ROLE)
async def history(ctx):
    commandsContent = open(f'{BASE_PATH}/logs/commands.log', 'r').read()
    await ctx.send(f"Sending the commands history to your DM :rocket:\nRequested by **{ctx.message.author}**")

    if len(commandsContent) < 2000:
        await ctx.message.author.send("Users Commands:")
        await ctx.message.author.send(f'```swift\n{commandsContent}```')
    else:
        RandomStr = utilities.generate_random_string()
        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(commandsContent)
            Message.close()

        await ctx.message.author.send("Users Commands:", file=discord.File(f"messages/{RandomStr}"))

# normal users commands
@Client.command()
async def nslookup(ctx , *, argument):
    Results = subprocess.check_output(['nslookup', f'{argument}'] , shell=False).decode('UTF-8')
    await ctx.send(f'{Results}')

@Client.command()
async def whois(ctx , *, argument):
    Output = subprocess.check_output(['whois', f'{argument}'], shell=False).decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            await ctx.send(f"Whois output for **{argument}**", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\nRequested by **{ctx.message.author}**")
    else:
        await ctx.send(f"Whois output for **{argument}**:")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\nRequested by **{ctx.message.author}**")

@Client.command()
async def dig(ctx , * , argument):
    Output = subprocess.check_output(['dig', f'{argument}'] , shell=False).decode('UTF-8')
    
    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            await ctx.send(f"Dig output for **{argument}**:", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\nRequested by **{ctx.message.author}**")
    else:
        await ctx.send(f"Dig output for **{argument}**:")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\nRequested by **{ctx.message.author}**")

@Client.command()
async def ip(ctx , *, argument):
    await ctx.send(utilities.get_ip(argument))

@Client.command()
async def statuscode(ctx, *, argument):
    url_parts = urlparse(argument)
    url_scheme = url_parts.scheme or 'http'

    if url_scheme not in ["http", "https"]:
        await ctx.send("**The URL scheme you're using isn't allowed**")
        return

    await ctx.send(f"Checking HTTP methods for <{argument}>")
    await ctx.message.edit(suppress=True)
    status_code_dict = utilities.get_status_codes(argument)
    message = "\n".join(f"{method}: {str(code)}" for method, code in status_code_dict.items())

    await ctx.send(message)
    await ctx.send(f"\nRequested by **{ctx.message.author}**")

@Client.command()
async def prips(ctx, *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    Output = subprocess.Popen(f"prips {argument}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    Output = Output.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            await ctx.send(f"Prips output for **{argument}**: ", file=discord.File(f"messages/{RandomStr}"))
            await ctx.send(f"\nRequested by **{ctx.message.author}**")
    else:
        await ctx.send(f"Prips output for **{argument}:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\nRequested by **{ctx.message.author}**")

# Tools commands
@Client.command()
async def dirsearch(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    fileName = utilities.generate_random_string()

    dirsearchPath = TOOLS['dirsearch']
    chdir(dirsearchPath)

    await ctx.send(f"**Running Your Dirsearch Scan, We Will Send The Results When It's Done**")
    _ = subprocess.Popen(f'python3 dirsearch.py -u {argument} -e "*" -o {BASE_PATH}/messages/{fileName} && python3 {BASE_PATH}/notify.py --mode 2 -m "Dirsearch results:" -f "- {ctx.message.author}" --file {fileName}', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    
    chdir(BASE_PATH)
    await ctx.send("**Dirsearch just started, The results gonna be sent when the process is done**")

@Client.command()
async def arjun(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    await ctx.send(f"**Running Your Arjun Scan, We Will Send The Results When It's Done**")
    await ctx.send(f"**Note: The Bot Won't Respond Until The Scan is Done. All Of Your Commands Now Will Be Executed After This Process is Done.")
    Process = subprocess.Popen(f'arjun -u {argument}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')
    Output = utilities.remove_escape_sequences(Output)
    Output = utilities.remove_string('Processing', Output)

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

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
    # argument = CommandInjection.sanitizeInput(argument)
    # Path = TOOLS['gitgraber']; MainPath = getcwd(); chdir(Path)
    # await ctx.send(f"**Running Your GitGraber Scan, See gitGraber Channel For Possible Leaks**")
    # _ = subprocess.Popen(f'python3 gitGraber.py -k wordlists/keywords.txt -q {argument} -d' , shell=True , stdin=None, stdout=None, stderr=None, close_fds=True)
    # chdir(MainPath)
    await ctx.send("Gitgrabber command is currently disabled, Might be implemented again in the next update.")

@Client.command()
async def waybackurls(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    await ctx.send(f"**Collecting Waybackurls, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"echo {argument} | waybackurls",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("Something went wrong while trying to read the message")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send(f"Waybackurls output for **{argument}**:", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\nRequested by **{ctx.message.author}**")
    else:
        await ctx.send(f'Waybackurls Results:')
        await ctx.send(f'```{Output}```')

@Client.command()
async def subfinder(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    await ctx.send(f"**Collecting Subdomains Using Subdinder, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"subfinder -d {argument} -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send("**Subfinder Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'Subfinder Results:')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def assetfinder(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    await ctx.send("**Collecting Subdomains Using Assetfinder, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"assetfinder --subs-only {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send("**Assetfinder Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'Results:')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def findomain(ctx , *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    findomainPath = TOOLS['findomain']
    await ctx.send("**Collecting Subdomains Using Findomain, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"{findomainPath} --target {argument} --quiet",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send("**Findomain Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send("**Findomain Results:**")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def paramspider(ctx, *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    paramPath = TOOLS['paramspider']
    await ctx.send("**Collecting Parameters Using ParamSpider, We Will Send The Results When It's Done**")
    Process = subprocess.Popen(f"python3 {paramPath}/paramspider.py -d {argument}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    Output = utilities.remove_escape_sequences(Output)
    Output = Output.split('\n')
    urlsList = []
    for singleLine in Output:
        if singleLine.startswith('http'):
            urlsList.append(singleLine)
        else:
            pass

    Output = '\n'.join(urlsList)

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send("**ParamSpider Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'**ParamSpider Results:**')
        await ctx.send(f'```{Output}```')
        await ctx.send(f"\n**- {ctx.message.author}**")

@Client.command()
async def trufflehog(ctx, *, argument):
    # # URL validation
    # urlParsed = urlparse(argument)
    # urlHost = urlParsed.netloc
    # if urlHost != "github.com" and urlHost != "gitlab.com":
    #     await ctx.send("**You're trying to scan unallowed URL, please use a github/gitlab URL.**")
    #     return
    
    # urlScheme = urlParsed.scheme
    # if urlScheme not in ["http", "https"]:
    #     await ctx.send("**You're trying to scan unallowed URL, please use a github/gitlab URL.**")
    #     return

    # # status code validation
    # statusCodeInteger = utilities.get_code(argument)
    # if statusCodeInteger == 404:
    #     await ctx.send("**The project you're trying to scan doesn't exists, double check the URL**")
    #     return

    # await ctx.send(f"**Scanning {argument} for possible data leaks using truffleHog**")
    # argument = CommandInjection.sanitizeInput(argument)
    # _ = subprocess.Popen(f"trufflehog --regex --entropy=False {argument} | python3 notify.py --mode 1 -m 'truffleHog Results:' -f '- {ctx.message.author}'", shell=True , stdin=None, stdout=None, stderr=None, close_fds=True)
    # await ctx.send(f"**pyNotify gonna send the results when it's done**")
    await ctx.send("Trufflehog is currently disabled, Might get added again in future updates.")

@Client.command()
async def gitls(ctx, *, argument):
    argument = CommandInjection.sanitizeInput(argument)
    await ctx.send(f"Collecting github repositories for **{argument}**")
    Process = subprocess.Popen(f"echo https://github.com/{argument} | gitls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    Output = Process.communicate()[0].decode('UTF-8')

    if len(Output) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(Output)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send(f"**Gitls output for **{argument}**:", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\nRequested by **{ctx.message.author}**")
    elif len(Output) == 0:
        await ctx.send(f"**Gitls didn't reutrn an output for your command**")
    else:
        await ctx.send(f"**Gitls output for **{argument}**:")
        await ctx.send(f"```{Output}```")
        await ctx.send(f"\nRequested by **{ctx.message.author}**")

# My Own Recon Data. It Isn't About You.
@Client.command()
async def recon(ctx , *, argument):
    if path.exists(f'/{USER}/{RECON_PATH}/{argument}'):
        try:
            Path = f'/{USER}/{RECON_PATH}/{argument}'.replace('//' , '/').replace('..', '')
            Data = open(Path).read().rstrip()
            Data = utilities.remove_escape_sequences(Data)
            Message = f"""```{Data}```"""
        except Exception:
            Message = f"**Couldn't Find The Recon Data With This Path: {argument}**"
    else:
        Message = "**Sorry The Path You Added Doesn't Exists On Our Records**"

    if len(Message) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as writerHere:
            writerHere.write(Message)
            writerHere.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send("**Recon Results:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\n**- {ctx.message.author}**")
    else:
        await ctx.send(f'{Message}')

# Recon Collections
async def collect_subdomains(ctx, *, argument):
    global logsItems, resolvedItems
    argument = CommandInjection.sanitizeInput(argument)

    await ctx.send(f"Collecting subdomains for **{argument}**, Might take up to a few minutes.")

    findomainPath = TOOLS['findomain']

    async def run_subprocess(command):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        results = await process.communicate()
        return results[0].decode('UTF-8')

    # Run subprocesses asynchronously
    findomainResults, assetfinderResults, subfinderResults = await asyncio.gather(
        run_subprocess(f"{findomainPath} --target {argument} --quiet"),
        run_subprocess(f"assetfinder --subs-only {argument}"),
        run_subprocess(f"subfinder -d {argument} -silent")
    )

    allSubdomains = findomainResults + assetfinderResults + subfinderResults
    allSubdomains = utilities.remove_duplicates(allSubdomains)
    allSubdomains = utilities.filter_subdomains(allSubdomains, argument)

    fileName = utilities.generate_random_string()
    resolvedName = utilities.generate_random_string()

    currentPath = getcwd()
    allSubdomains = '\n'.join(allSubdomains)

    with open(f'data/hosts/{resolvedName}', 'w') as subdomainsFile:
        subdomainsFile.write(allSubdomains)

    resolvedParser.resolvedWriter(Target=argument, fileName=f"{resolvedName}\n")
    resolvedItems[argument] = resolvedName

    httpxResults = await run_subprocess(f"cat data/hosts/{resolvedName} | httpx -silent")

    with open(f'data/subdomains/{fileName}', 'w') as subdomainsFile:
        subdomainsFile.write(httpxResults)

    logsParser.logsWriter(Target=argument, fileName=fileName)
    logsItems[argument] = fileName

    if len(httpxResults) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}', 'w') as Message:
            Message.write(httpxResults)

            messageSize = utilities.get_size(file_path=f"messages/{RandomStr}")
            if not messageSize:
                await ctx.send("Something went wrong reading the output.")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send(f"**Active subdomains collected for **{argument}**:", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\nRequested by **{ctx.message.author}**")
    else:
        await ctx.send(f"Active subdomains collected for **{argument}**:")
        await ctx.send(f'```{httpxResults}```')
        await ctx.send(f"\nRequested by **{ctx.message.author}**")

@Client.command()
async def subdomains(ctx, *, argument):
    asyncio.create_task(collect_subdomains(ctx, argument=argument))

@Client.command()
async def info(ctx , *, argument):
    global logsItems

    try:
        subdomainsFile = logsItems[argument]
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"Collecting information about subdomains for **{argument}**")
    Process = subprocess.Popen(f"cat data/subdomains/{subdomainsFile} | httpx -title -web-server -status-code -follow-redirects -silent",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    httpxResults = Process.communicate()[0].decode('UTF-8')
    httpxResults = utilities.remove_escape_sequences(httpxResults)

    if len(httpxResults) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(httpxResults)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')
            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
            else:
                await ctx.send(f"Subdomains information for **{argument}:**", file=discord.File(f"messages/{RandomStr}"))
                await ctx.send(f"\nRequested by **{ctx.message.author}**")
    else:
        await ctx.send(f"Subdomains information for **{argument}**:")
        await ctx.send(f'```{httpxResults}```')
        await ctx.send(f"\nRequested by **{ctx.message.author}**")

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
    argument = CommandInjection.sanitizeInput(argument)

    try:
        resolvedFile = resolvedItems[argument]
        fileStr = utilities.generate_random_string()
    except Exception:
        await ctx.send("**There's no subdomains has been collected for this target. please use** `.subdomains [TARGET]` **Then try again.**")
        return

    await ctx.send(f"**Scanning {argument} For Possible Subdomains Takeover Issues Using Subjack**")
    _ = subprocess.Popen(f"subjack -w data/hosts/{resolvedFile} -t 100 -timeout 30 -o data/subjack/{argument}-{fileStr}.subjack -ssl | python3 notify.py --mode 1 -m 'Subjack results:' -f '- {ctx.message.author}'", shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)

    await ctx.send(f"**Results gonna be sent to the results channel soon**")

@Client.command()
async def subjs(ctx , *, argument):
    global logsItems
    argument = CommandInjection.sanitizeInput(argument)

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
    argument = CommandInjection.sanitizeInput(argument)

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

    smugglerResults = utilities.remove_escape_sequences(smugglerResults)
    if len(smugglerResults) > 2000:
        RandomStr = utilities.generate_random_string()

        with open(f'messages/{RandomStr}' , 'w') as Message:
            Message.write(smugglerResults)
            Message.close()

            messageSize = utilities.get_size(f'messages/{RandomStr}')

            if not messageSize:
                await ctx.send("**There's Something Wrong On The Bot While Reading a File That's Already Stored. Check It.**")
                return
            elif messageSize > 8:
                await ctx.send("The output size is over 8mb, We can't send it over discord at the moment.")
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
    targetsMessage = f"""```
    {targetsMessage}
    ```
    """
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

    await ctx.send(f"**{argument}**:\n\t\tResolved hosts: {str(resolvedLength)}\n\t\tLive subdomains: {str(subdomainsLength)}")

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
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y/%m/%d")
    utilities.log_command(ctx.command, ctx.author, formatted_date, ctx.message.content)

@Client.event
async def on_member_join(member):
    welcome_message = f"""```    
Welcome to Discord-Recon, your go-to Discord bot designed to assist bug bounty hunters in streamlining their reconnaissance process through simple commands. Whether you prefer using the bot within your server or privately in this chat, the choice is yours.

If you're interested in hosting your own Discord-Recon server, feel free to explore the source code at https://github.com/DEMON1A/Discord-Recon. Donations are appreciated but not mandatory; they go towards server upgrades and covering the bot's hosting expenses. Contribute if you can, and thank you for being part of our community!
    ```"""
    await member.send(welcome_message)

@Client.event
async def on_member_remove(member):
    admin_channel = Client.get_channel(ADMIN_CHANNEL)
    await admin_channel.send(f"**{member}** either left the server or got kicked out.")

@Client.event
async def on_ready():
    admin_channel = Client.get_channel(ADMIN_CHANNEL)
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y/%m/%d")

    # Get system information
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage = psutil.disk_usage('/').percent

    message = (
        f"**ReconServer Started** :dizzy:\n\n"
        f"Operating on: **{formatted_date}**\n"
        f"Memory Usage: **{memory_usage}%**\n"
        f"CPU Usage: **{cpu_usage}**%\n"
        f"Disk Usage: **{disk_usage}**%"
    )

    await admin_channel.send(message)

if __name__ == "__main__":
    Client.run(DISCORD_TOKEN)
