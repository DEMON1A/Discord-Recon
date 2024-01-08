import random, string, socket, re
from os import path
from requests import get, request

# GLOBALS
subdomains_set = set()

def generate_random_string(length=12):
    chars = string.ascii_letters
    random_str = ''.join(random.choice(chars) for _ in range(length)) + ".txt"
    return random_str

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} is pointing to {ip}"
    except socket.gaierror:
        return "Sorry, We can't resolve this domain"
    
def filter_subdomains(subdomain_list, hunting_target):
    return [subdomain for subdomain in subdomain_list if subdomain.endswith(hunting_target)]

def remove_duplicates(subdomains):
    global subdomains_set
    subdomains_set.update(subdomains.split('\n'))
    return list(subdomains_set)

def get_size(file_path):
    return path.getsize(file_path) / 1000000 if path.exists(file_path) else False

def remove_escape_sequences(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def remove_string(bad_text, output):
    return ''.join(line + '\n' for line in output.split('\n') if bad_text not in line.rstrip('\n'))

def get_code(url):
    return get(url).status_code

def get_status_codes(url):
    methods = ["GET", "POST", "PUT", "TRACE", "HEAD", "OPTIONS", "PATCH", "DELETE", "ANYTHING"]
    return {method: request(method, url).status_code for method in methods}

def log_command(command, author, date, message):
    message = message.replace('\n', '')
    formatted_message = f"[{date}] {author}:{command}, Command: {message}\n"

    with open('logs/commands.log', 'a') as log_file:
        log_file.write(formatted_message)