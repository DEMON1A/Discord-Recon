from os import path

BASE_PATH = path.abspath(path.join(__file__, "../"))
DISCORD_TOKEN = ""
DEFAULT_DISCORD_WEBHOOK = ""
USER = ""
ADMIN_ROLE = ""
RECON_PATH = ""
DEBUG = True
ADMIN_CHANNEL = 812515205082906644
DISABLE_NUCLEI_INFO = True
NUCLEI_WEBHOOK = ""
COMMANDS_PREFIX = "."

TOOLS = {
    "dirsearch":"tools/dirsearch/",
    "gitgraber":"tools/gitGraber/",
    "findomain":"tools/findomain-linux",
    "nuclei-templates":"tools/nuclei-templates/",
    "paramspider":"tools/ParamSpider/",
    "smuggler":"tools/smuggler/"
}

RCE = [';' , '`' , '$' , '(' , ')' , '|' , '&' , '%', '\n', '<', '>']
