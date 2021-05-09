def logCommand(Command, Author, Date):
    Message = f"[{str(Date)}] {Author}: {Command}\n"

    with open('data/logs/commands.easy', 'a') as logFile:
        logFile.write(Message)
        logFile.close()
