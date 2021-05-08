# Discord-Recon [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Check%20out%20Discord-Recon%20on%20github!&url=https://github.com/DEMON1A/Discord-Recon&via=DemoniaSlash&hashtags=recon,bugbounty) <a href="https://huntr.dev/bounties/disclose"><img src="https://cdn.huntr.dev/huntr_security_badge_mono.svg" alt="Huntr"></a> ![](https://tokei.rs/b1/github/DEMON1A/Discord-Recon)
- Discord Recon Server Allows You To Do Your Reconnaissance Process From Your Discord.

## What's Discord Recon? :confused:
- Discord Recon is a Cool Discord Bot Working On Your Server To Make It Easy To Do Recon From Your Discord Server. The Bot Has Been Linked With Many Tools Like: Nuclei, Findomain, Assetfinder, Subfinder, Arjun, ParamSpider, Waybackurls, Dirsearch And gitGraber. You Can Use All Of These Tools Via The Bot Using Only Discord Commands. Also, Discord Recon Allows You To Automate Subdomains Collection Process. It's Using Assetfinder, Findomain And Subfinder To Collect Subdomains, Sort Them Using Python Function. Then Filter Them Using httpx. And The Output Is Getting Saved On The Server. Anytime You Want To Use This Data For Nuclei Scans Or Any Other Scans That Wiil Be Added Soon. You Can Just Call The Scan Function And It Will Use The Subdomains That Got Saved Before. 

## Setup Discord-Recon On Your Server :relieved:
1. Download Discord-Recon Source Code Using

```
git clone https://github.com/DEMON1A/Discord-Recon/
```

2. Make Sure You Have Both `python3` and `golang` On Your System.
3. Run Discord-Recon Tools Installer From The Main Folder And Make Sure There's No Errors Using:

```
bash ./bash/installer.sh
```

4. Modify Your `setting.py` File With The Options You Like
5. Add Your Discord Webhook URL Into Notify Config
6. Run `app.py` With The Command: `python3 app.py` And Feel Free To Open an Issue If Something Isn't Working

**NOTE: Running discord-recon on a VPS will be much cooler, since it uses a lot of internet and memory based on your usage. and you don't really want to harm yourself.**

## Setup Variables :star:
- `DISCORD_TOKEN` - Your Discord Bot Token
- `USER` - Path To Your OS User
- `RECON_PATH` - Path To Your Recon Data
- `ADMINS` - Admins That Can Run OS Commands On The Server With `exec`
- `DEBUG` - Debug Mode
- `COMMANDS_PREFIX` - The Perfix Of All Bot Commands
- `ADMIN_CHANNEL` - Admin Channel ID For Important Messages.
- `TOOLS` - Paths For The Tools Names Inside Your System
- `RCE` - Command Injection Protection. Don't Ever Remove One Of It's Items.

## Commands: :thought_balloon:
- `.exec` - Execute Shell Commands On The Server.
- `.compile` - Execute a Python3 Code On The Server
- `.ip` - Get The Domain IP
- `.dig` - Run dig
- `.prips` - Genrate IPs from a company IP range
- `.nslookup` - Run nslookup
- `.whois` - Run Whois
- `.dirsearch` - Start dirsearch Scan
- `.arjun` - Start Arjun Scan
- `.gitgraber` - Start GitGraber Scan
- `.waybackurls` - Start Waybackurls
- `.subfinder` - Start Subfinder
- `.assetfinder` - Start Assetfinder
- `.findomain` - Start Findomain
- `.paramspider` - Start ParamSpider
- `.recon` - Read Internal Recon File
- `.subdomains` - Collect Subdomains
- `.show` - Show Targets We Have On The Database
- `.count` - Show Subdomains/Hosts Count In The DataBase.
- `.nuclei` - Perform Nuclei Scan On Collected Subdomains
- `.subjack` - Perform Subjack Scan On Collected Subdomains
- `.subjs` - Run Subjs On Collected Subdomains
- `.smuggler` - Run Smuggler On Collected Subdomains.

## Don't Have a Server To Host The Bot? :worried:
- I Did Already Run The Bot On My Own Discord Server, You Can Join Using This URL: https://discord.gg/RBkQk86x2g. But For Now, gitGraber Results Are Only Available For Supporters. And Some Other Scans Including The New Functions Will Be Like That. Supprting Discord Recon Will Give You Lifetime Access To The Bot. We Use The Donations To Upgrade The Server Resources So We Will Be Able To Add More Features. So We Need To Limit Bot Access.

## Suggest New Tool Support? :boom:
- Sure You Can. Just Open an Issue With The Tool Name. And It Will Be Added In Both. The Source Code And The Our Discord Server.

## Wanna Delete Your Bot Data? :worried:
1. chmod +x bash/clean.sh
2. bash/clean.sh

## Security
- We care about discord-recon security specially because it interacts with the internal server and any security issues can result in server-side issues, if you think that you found a security issue on discord-recon with working proof of concept on the bot on our server. then you can report this issue via [Huntr](https://huntr.dev/) to get awarded and help me fixing the issue by sumitting code fixes, otherwise you can just open an issue with it on github or email me at my personal email and i will respond ASAP.

- It's really not safe to run discord-recon from your system with high privileges, i would suggest creating a user with low privileges and run the bot from it, then give the user the access into the tools. 

## Found This Tool Helpful? :heartbeat:
- In case you see that this tool is helpful. supporting the developer will be great. but not recommended in the current time. otherwise, i will be really thankful if you give this repo a :star:. stars helps the project to be visible to more people.

# Collaborators 💝
- [@0xWise64](https://github.com/0xWise64) - Reported Security Issues On Discord-Recon, Helped With The Development Process
- [@Ry0taK](https://github.com/Ry0taK) - Reported Security Issues On Discord-Recon
- [@SecurityHook](https://github.com/SecurityHook) - Reported Security Issues On Discord-Recon

# Credits :sparkles:
- [assetfinder](https://github.com/tomnomnom/assetfinder) - [@tomnomnom](https://github.com/tomnomnom)
- [subfinder](https://github.com/projectdiscovery/subfinder) - [@projectdiscovery](https://github.com/projectdiscovery)
- [findomain](https://github.com/Findomain/Findomain) - [@Findomain](https://github.com/Findomain)
- [arjun](https://github.com/s0md3v/Arjun) - [@s0md3v](https://github.com/s0md3v)
- [dirsearch](https://github.com/maurosoria/dirsearch) - [@maurosoria](https://github.com/maurosoria)
- [gitGraber](https://github.com/hisxo/gitGraber) - [@hisxo](https://github.com/hisxo)
- [waybackurls](https://github.com/tomnomnom/waybackurls) - [@tomnomnom](https://github.com/tomnomnom)
- [nuclei](https://github.com/projectdiscovery/nuclei) - [@projectdiscovery](https://github.com/projectdiscovery)
- [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) - [@projectdiscovery](https://github.com/projectdiscovery)
- [subjack](https://github.com/haccer/subjack) - [@haccer](https://github.com/haccer)
- [subjs](https://github.com/lc/subjs) - [@lc](https://github.com/lc)
- [smuggler](https://github.com/defparam/smuggler) - [@defparam](https://github.com/defparam)
- [httpx](https://github.com/projectdiscovery/httpx) - [@projectdiscovery](https://github.com/projectdiscovery)
- [notify](https://github.com/projectdiscovery/notify) - [@projectdiscovery](https://github.com/projectdiscovery)
