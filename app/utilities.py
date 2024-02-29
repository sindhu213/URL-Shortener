import secrets
import string

def generate_short_url(length = 6):
    id = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(id) for _ in range(length))
    return token