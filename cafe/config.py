import os

# Flask SECRET_KEY
SECRET_KEY = os.urandom(24)

# Host
HOST = '0.0.0.0'

# Port
PORT = 80

# Debug mode
DEBUG_MODE = True

# Threaded
THREADED = True

# Template folder
TEMPLATE_FOLDER = "templates"

# Static folder
STATIC_FOLDER = "static"
