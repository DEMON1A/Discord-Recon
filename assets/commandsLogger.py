def logCommand(Command, Author, Date, Message):
    Message = Message.replace('\n', '')
    Message = f"[{str(Date)}] {Author}:{Command}, Command: {Message}\n"

    with open('data/logs/commands.easy', 'a') as logFile:
        logFile.write(Message)
        logFile.close()
