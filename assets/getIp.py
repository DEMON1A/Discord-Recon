import socket

def getIp(Domain):
    try:
        IP = socket.gethostbyname(Domain)
        return f"Your Domain IP Address: {IP}"
    except Exception:
        return "**Sorry We Can't Resolve This Domain**"