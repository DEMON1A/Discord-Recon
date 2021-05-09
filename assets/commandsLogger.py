def logCommand(Command, Author, Date):
    Message = f"User: {Author}, Used this command: {Command}, at: {str(Date)}\n"

    with open('data/logs/commands.easy', 'a') as logFile:
        logFile.write(Message)
        logFile.close()
