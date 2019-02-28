import os

''' GENERATE SECRET KEY '''

if not os.environ.get('SECRET_KEY'):
    # Attempt to read the secret from the secret file
    # This will fail if the secret has not been written
    try:
        with open('.secret_key', 'rb') as secret:
            key = secret.read()
    except (OSError, IOError):
        key = None

    if not key:
        key = os.urandom(64)
        # Attempt to write the secret file
        # This will fail if the filesystem is read-only
        try:
            with open('.secret_key', 'wb') as secret:
                secret.write(key)
                secret.flush()
        except (OSError, IOError):
            pass

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or key
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///{}/database.db'.format(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'
    OAUTHLIB_INSECURE_TRANSPORT=True
    SERVER_NAME="localhost:4523"

    with open('.google_oauth') as f:
        GOOGLE_OAUTH_CLIENT_ID = f.readline().strip()
        GOOGLE_OAUTH_CLIENT_SECRET = f.readline().strip()

