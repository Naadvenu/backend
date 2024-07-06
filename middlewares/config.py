import secrets
import string

SECRET_KEY = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
