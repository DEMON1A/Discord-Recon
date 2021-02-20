# Discord-Recon
Discord Recon Server Allows You To Do Your Reconnaissance Process From Your Discord.

## What's Discord Recon?
- Discord Recon is a Cool Discord Bot Working On Your Server To Make It Easy To Do Recon From Your Discord Server. The Bot Has Been Linked With Many Tools Like: Nuclei, Findomain, Assetfinder, Subfinder, Arjun, ParamSpider, Waybackurls, Dirsearch And gitGraber. You Can Use All Of These Tools Via The Bot Using Only Discord Commands. Also, Discord Recon Allows You To Automate Subdomains Collection Process. It's Using Assetfinder, Findomain And Subfinder To Collect Subdomains, Sort Them Using Python Function. Then Filter Them Using httpx. And The Output Is Getting Saved On The Server. Anytime You Want To Use This Data For Nuclei Scans Or Any Other Scans That Wiil Be Added Soon. You Can Just Call The Scan Function And It Will Use The Subdomains That Got Saved Before. 

## Setup Variables
- `DISCORD_TOKEN` - Your Discord Bot Token
- `USER` - Path To Your OS User
- `RECON_PATH` - Path To Your Recon Data
- `ADMINS` - Admins That Can Run OS Commands On The Server With `exec`
- `DEBUG` - Debug Mode
- `COMMANDS_PREFIX` - The Perfix Of All Bot Commands
- `ADMIN_CHANNEL` - Admin Channel ID For Important Messages.
- `TOOLS` - Paths For The Tools Names Inside Your System
- `RCE` - Command Injection Protection. Don't Ever Remove One Of It's Items.

## Commands:
- `.ip` - Get The Domain IP
- `.dig` - Run dig
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
- `.nuclei` - Perform Nuclei Scan On Collected Subdomains

## Don't Have a Server To Host The Bot?
- I Did Already Run The Bot On My Own Discord Server, You Can Join Using This URL: https://discord.gg/nvd2KMKB. But For Now, gitGraber Results Are Only Available For Supporters. And Some Other Scans Including The New Functions Will Be Like That. Supprting Discord Recon Will Give You Lifetime Access To The Bot. We Use The Donations To Upgrade The Server Resources So We Will Be Able To Add More Features. So We Need To Limit Bot Access.

## Suggest New Tool Support?
- Sure You Can. Just Open an Issue With The Tool Name. And It Will Be Added In Both. The Source Code And The Our Discord Server.
