from os import path
from urllib.parse import urlparse

BASE_PATH = path.abspath(path.join(__file__, "../"))
DISCORD_TOKEN = "1234567890ABCD"
DEFAULT_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/xyz"
USER = "/home/username"
ADMIN_ROLE = "Admins"
RECON_PATH = "/home/user/recon"
DEBUG = False
ADMIN_CHANNEL = 812515205082906641
ADMIN_CHANNEL = int(urlparse(str(ADMIN_CHANNEL)).path.split('/')[-1:][0])
DISABLE_NUCLEI_INFO = True
NUCLEI_WEBHOOK = "https://discord.com/api/webhooks/xyz"
COMMANDS_PREFIX = "."

TOOLS = {
    "dirsearch":f"{BASE_PATH}/tools/dirsearch/",
    "arjun":f"{BASE_PATH}/tools/Arjun/",
    "gitgraber":f"{BASE_PATH}/tools/gitGraber/",
    "findomain":f"{BASE_PATH}/tools/Finddomain/findomain-linux",
    "nuclei-templates":f"{BASE_PATH}/nuclei-templates/",
    "paramspider":f"{BASE_PATH}/tools/ParamSpider/",
    "smuggler":f"{BASE_PATH}/tools/smuggler/"
}

RCE = [';' , '`' , '$' , '(' , ')' , '|' , '&' , '%', '\n', '<', '>']
