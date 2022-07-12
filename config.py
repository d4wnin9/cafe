import os

# Flask SECRET_KEY
SECRET_KEY = os.urandom(24)

# Database URI
## user: team8
## pass: 1qazxsw2
## data: team8db
DATABASE_URI = 'postgresql://localhost/team8db?user=team8&password=1qazxsw2'

# Host
HOST = '0.0.0.0'

# Port
PORT = 8088

# Debug mode
DEBUG_MODE = True

# Threaded
THREADED = True

# Template folder
TEMPLATE_FOLDER = "templates"

# Static folder
STATIC_FOLDER = "static"

# SSL context
SSL_CONTEXT = ('pem/cert.pem', 'pem/key.pem')