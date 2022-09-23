from os import path
from urllib.parse import urlparse

BASE_PATH = path.abspath(path.join(__file__, "../"))
DISCORD_TOKEN = ""
DEFAULT_DISCORD_WEBHOOK = ""
USER = ""
ADMIN_ROLE = ""
RECON_PATH = ""
DEBUG = True
ADMIN_CHANNEL = 812515205082906644
ADMIN_CHANNEL = int(urlparse(str(ADMIN_CHANNEL)).path.split('/')[-1:][0])
DISABLE_NUCLEI_INFO = True
NUCLEI_WEBHOOK = ""
COMMANDS_PREFIX = "."

TOOLS = {
    "dirsearch": f"{BASE_PATH}/tools/dirsearch/",
    "gitgraber": f"{BASE_PATH}tools/gitGraber/",
    "findomain": f"{BASE_PATH}/tools/findomain-linux",
    "nuclei-templates": f"{BASE_PATH}/tools/nuclei-templates/",
    "paramspider": f"{BASE_PATH}/tools/ParamSpider/",
    "smuggler": f"{BASE_PATH}/tools/smuggler/"
}

RCE = [';' , '`' , '$' , '(' , ')' , '|' , '&' , '%', '\n', '<', '>']
