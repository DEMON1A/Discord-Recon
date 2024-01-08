import sys, optparse
from dhooks import Webhook, File

from utils.uio import utilities
from settings import DEFAULT_DISCORD_WEBHOOK
from settings import BASE_PATH

def collectOptions():
    Parser = optparse.OptionParser()
    Parser.add_option("-m", "--message", dest="message", default="PyNotify Output", help="The message you want to show before the output")
    Parser.add_option("-f", "--footer", dest="footer", default="- PyNotify 0.0.1", help="The footer you want to show after the output")
    Parser.add_option("--discord-webhook", dest="webhook", default=DEFAULT_DISCORD_WEBHOOK, help="The discord webhook you want to use to send results to")
    Parser.add_option("--mode", dest="mode", default="0", help="The mode you want to use to send the output")
    Parser.add_option("--file", dest="file", default=False, help="The file you want to send in-case you're sending a message")

    Options, _ = Parser.parse_args()
    return Options

def sendLineByLine(DiscordWebhook):
    try:
        Hook = Webhook(DiscordWebhook)

        for singleLine in sys.stdin:
            singleLine = singleLine.rstrip('\n')
            singleLine = utilities.remove_escape_sequences(singleLine)
            Hook.send(singleLine)
    except Exception:
        print("Can't connect to the webhook you added")

def sendFullInput(DiscordWebhook, Options):
    try:
        Hook = Webhook(DiscordWebhook)
        pipeOutput = sys.stdin.read()
        pipeOutput = utilities.remove_escape_sequences(pipeOutput)

        if len(pipeOutput) < 2000:
            Hook.send(f"**{Options.message}**")
            Hook.send(f"```\n{pipeOutput}```")
            Hook.send(f"**{Options.footer}**")
        else:
            randomFilename = utilities.generate_random_string()

            with open(f'messages/{randomFilename}', 'w') as outputFile:
                outputFile.write(pipeOutput)
                outputFile.close()

            messageSize = utilities.get_size(filePath=f'{BASE_PATH}/messages/{randomFilename}')
            if messageSize > 8:
                Hook.send("We currently don't support sending outputs w/ size over 8mb")
            else:
                discordFile = File(f"{BASE_PATH}/messages/{randomFilename}", name=randomFilename)
                Hook.send(f"**{Options.message}**", file=discordFile)
                Hook.send(f"**{Options.footer}**")
    except Exception:
        print("Can't connect to the webhook you added")

def sendMessage(DiscordWebhook, Options):
    try:
        Hook = Webhook(DiscordWebhook)

        if Options.file:
            messageSize = utilities.get_size(filePath=f"{BASE_PATH}/messages/{Options.file}")
            if messageSize > 8:
                Hook.send("We currently don't support sending outputs w/ size over 8mb")
            else:
                discordFile = File(f"{BASE_PATH}/messages/{Options.file}")
                Hook.send(f"**{Options.message}:**", file=discordFile)
                Hook.send(f"**{Options.footer}**")
        else:
            print("This mode only works with files")
    except Exception as e:
        print("Error:", e)
        print("Can't connect to the webhook you added")

def mainFunction():
    Options = collectOptions()
    if Options.mode == "0":
        sendLineByLine(Options.webhook)
    elif Options.mode == "1":
        sendFullInput(Options.webhook, Options)
    elif Options.mode == "2":
        sendMessage(Options.webhook, Options)
    else:
        pass

if __name__ == '__main__':
    mainFunction()
