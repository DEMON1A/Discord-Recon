from os import path
from urllib.parse import urlparse

BASE_PATH = path.abspath(path.join(__file__, "../"))
DISCORD_TOKEN = "Nzk1Nzc4OTQ0ODI0NjM5NTA3.Gy0DcW.7pjfbJO6K4wUsMXo9XV152vq3lX8nEOKLwql-U"
DEFAULT_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/873346709814661130/518-qLYwlCeiLZg_IrqPpoRf8oFVRpcQ9megHCl-shbKORJVerxS7OCFsmp7xvJ-xPEK"
USER = "root"
ADMIN_ROLE = "Admin"
RECON_PATH = "/root/bugbounty/"
DEBUG = True
ADMIN_CHANNEL = 912338344938205224
ADMIN_CHANNEL = int(urlparse(str(ADMIN_CHANNEL)).path.split('/')[-1:][0])
DISABLE_NUCLEI_INFO = False
NUCLEI_WEBHOOK = "https://discord.com/api/webhooks/1193089707341529159/XjotxEFmoFHCWvubkpuSLZVNzyLT5-JVMyUaFIM8dJHODBAjstiE7vG1Q1aJYfY8DWpE"
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
