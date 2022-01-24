<p align="center"><img width="100" height="100" src="/images/logo.svg"></p>

<h1 align="center">Discord-Recon</h1>
<p align="center">DiscordRecon server allows you to do your reconnaissance process from your discord server.</p>

<p align="center">
<a href="https://twitter.com/intent/tweet?text=check%20out%20discord-recon%20on%20github!&url=https://github.com/demon1a/discord-recon&via=demoniaslash&hashtags=recon,bugbounty"><img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"> <!-- twitter retweet button --> </a>
<a href="https://huntr.dev/bounties/disclose"> <img src="https://cdn.huntr.dev/huntr_security_badge_mono.svg" alt="huntr"> <!-- huntr badge --> </a>
<img src="https://tokei.rs/b1/github/demon1a/discord-recon"> <!-- total lines of code -->
<a href="https://discord.gg/rbkqk86x2g"> <img src="https://img.shields.io/discord/795756379700461589.svg?logo=discord"> <!-- discord chat widget --> </a>
</p>


## What's discord recon? :confused:
- DiscordRecon is a cool discord bot working on your server to make it easy to do recon from your discord server. the bot has been linked with many tools like: nuclei, findomain, assetfinder, subfinder, arjun, paramspider, waybackurls, dirsearch and gitgraber. you can use all of these tools via the bot using only discord commands. also, discord recon allows you to automate subdomains collection process. it's using assetfinder, findomain and subfinder to collect subdomains, sort them using python function. then filter them using httpx. and the output is getting saved on the server. anytime you want to use this data for nuclei scans or any other scans that wiil be added soon. you can just call the scan function and it will use the subdomains that got saved before. 

## Setup discord-recon on your server :relieved:
1. download discord-recon source code using

```
git clone https://github.com/demon1a/discord-recon/
cd discord-recon/
```

2. make sure you have both `python3`, `golang` and `pip3` on your system.
3. run discord-recon tools installer from the main folder and make sure there's no errors using:

```
sudo bash ./bash/installer.sh
```

4. modify your `settings.py` file with the options you like
5. add your discord webhook url into notify config
6. edit gitgraber config and add your github token and discord webhook
7. run `app.py` with the command: `python3 app.py` and feel free to open an issue if something isn't working

**note: running discord-recon on a vps will be much cooler, since it uses a lot of internet and memory based on your usage. and you don't really want to harm your machine.** <br> <br>
**note: discord-recon has been tested only on linux, and most of the commands on the code are based on bash, it's not possible to run discord-recon on windows os**

## Setup variables :star:
- `DISCORD_TOKEN` - your discord bot token
- `USER` - path to your os user
- `RECON_PATH` - path to your recon data
- `ADMIN_ROLE` - the admin role name on your server
- `DEBUG` - debug mode
- `COMMANDS_PREFIX` - the perfix of all bot commands
- `ADMIN_CHANNEL` - admin channel id for important messages.
- `DISABLE_NUCLEI_INFO` - disable nuclei from sending inf bugs
- `NUCLEI_WEBHOOK` - the webhook nuclei will be using to post bugs
- `DEFAULT_DISCORD_WEBHOOK` - the default discord-webhook discord-recon gonna send results with
- `TOOLS` - paths for the tools names inside your system
- `RCE` - command injection protection. don't ever remove one of it's items.

## Commands: :thought_balloon:
- `.exec` - execute shell commands on the server.
- `.sudo` - give discord roles to users
- `.unsudo` - remove discord roles from users
- `.compile` - execute a python3 code on the server
- `.shutdown` - shutdown the bot
- `.restart` - restart the bot.
- `.ip` - get the domain ip
- `.dig` - run dig
- `.prips` - genrate ips from a company ip range
- `.nslookup` - run nslookup
- `.whois` - run whois
- `.statuscode` - get status codes of subdomain/url
- `.dirsearch` - start dirsearch scan
- `.arjun` - start arjun scan
- `.gitgraber` - start gitgraber scan
- `.waybackurls` - start waybackurls
- `.subfinder` - start subfinder
- `.assetfinder` - start assetfinder
- `.findomain` - start findomain
- `.paramspider` - start paramspider
- `.trufflehog` - start trufflehog
- `.gitls` - start gitls
- `.recon` - read internal recon file
- `.subdomains` - collect subdomains
- `.show` - show targets we have on the database
- `.count` - show subdomains/hosts count in the database.
- `.history` - show the users commands from the logs.
- `.nuclei` - perform nuclei scan on collected subdomains
- `.subjack` - perform subjack scan on collected subdomains
- `.subjs` - run subjs on collected subdomains
- `.smuggler` - run smuggler on collected subdomains.

## Don't have a server to host the bot? :worried:
- i did already run the bot on my own discord server, you can join using this url: https://discord.gg/rbkqk86x2g. at the time of writing this, discord-recon is fully free for all users and doesn't require supporting to get access into some tools, but that might get changed soon when we update our service.

## Suggest new tool support? :boom:
- sure you can. just open an issue with the tool name. and it will be added in both. the source code and the our discord server.

## Wanna delete your bot data? :worried:
1. chmod +x bash/clean.sh
2. bash/clean.sh

## Security
- we care about discord-recon security specially because it interacts with the internal server and any security issues can result in server-side issues, if you think that you found a security issue on discord-recon with working proof of concept on the bot on our server. then you can report this issue via [huntr](https://huntr.dev/) to get awarded and help me fixing the issue by sumitting code fixes, otherwise you can just open an issue with it on github or email me at my personal email and i will respond asap.

- it's really not safe to run discord-recon from your system with high privileges, i would suggest creating a user with low privileges and run the bot from it, then give the user the access into the tools. 

## Found discord-recon helpful? :heartbeat:
- in case you see that discord-recon is helpful. giving the project a :star: will be great. but you can always support discord-recon via the sponser links on the project, to keep it active and updated with more server resources to serve many users as possible.

# Collaborators 💝
- [@0xwise64](https://github.com/0xwise64) - reported security issues on discord-recon, helped with the development process
- [@ry0tak](https://github.com/ry0tak) - reported security issues on discord-recon
- [@securityhook](https://github.com/securityhook) - reported security issues on discord-recon

# Credits :sparkles:
- [assetfinder](https://github.com/tomnomnom/assetfinder) - [@tomnomnom](https://github.com/tomnomnom)
- [subfinder](https://github.com/projectdiscovery/subfinder) - [@projectdiscovery](https://github.com/projectdiscovery)
- [findomain](https://github.com/findomain/findomain) - [@findomain](https://github.com/findomain)
- [arjun](https://github.com/s0md3v/arjun) - [@s0md3v](https://github.com/s0md3v)
- [dirsearch](https://github.com/maurosoria/dirsearch) - [@maurosoria](https://github.com/maurosoria)
- [gitgraber](https://github.com/hisxo/gitgraber) - [@hisxo](https://github.com/hisxo)
- [waybackurls](https://github.com/tomnomnom/waybackurls) - [@tomnomnom](https://github.com/tomnomnom)
- [nuclei](https://github.com/projectdiscovery/nuclei) - [@projectdiscovery](https://github.com/projectdiscovery)
- [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) - [@projectdiscovery](https://github.com/projectdiscovery)
- [subjack](https://github.com/haccer/subjack) - [@haccer](https://github.com/haccer)
- [subjs](https://github.com/lc/subjs) - [@lc](https://github.com/lc)
- [smuggler](https://github.com/defparam/smuggler) - [@defparam](https://github.com/defparam)
- [httpx](https://github.com/projectdiscovery/httpx) - [@projectdiscovery](https://github.com/projectdiscovery)
- [notify](https://github.com/projectdiscovery/notify) - [@projectdiscovery](https://github.com/projectdiscovery)
- [paramspider](https://github.com/devanshbatham/paramspider) - [@devanshbatham](https://github.com/devanshbatham)
- [trufflehog](https://github.com/trufflesecurity/trufflehog) - [@trufflesecurity](https://github.com/trufflesecurity)
- [gitls](https://github.com/hahwul/gitls) - [@hahwul](https://github.com/hahwul)
