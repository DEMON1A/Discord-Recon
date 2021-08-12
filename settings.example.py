from os import path

BASE_PATH = path.abspath(path.join(__file__, "../"))
DISCORD_TOKEN = "1234567890ABCD"
SERVER_NAME = "My-Server"
DEFAULT_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/xyz"
USER = "/home/username"
ADMIN_ROLE = "Admins"
RECON_PATH = "/home/user/recon"
DEBUG = False
ADMIN_CHANNEL = 812515205082906641
DISABLE_NUCLEI_INFO = True
NUCLEI_WEBHOOK = "https://discord.com/api/webhooks/xyz"
COMMANDS_PREFIX = "."

TOOLS = {
    "dirsearch":f"/{USER}/tools/dirsearch/",
    "arjun":f"/{USER}/tools/Arjun/",
    "gitgraber":f"/{USER}/tools/gitGraber/",
    "findomain":f"/{USER}/tools/Finddomain/findomain-linux",
    "nuclei-templates":f"/{USER}/nuclei-templates/",
    "paramspider":f"{USER}/tools/ParamSpider/",
    "smuggler":f"{USER}/tools/smuggler/"
}

RCE = [';' , '`' , '$' , '(' , ')' , '|' , '&' , '%', '\n', '<', '>']
