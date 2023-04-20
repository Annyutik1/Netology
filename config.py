from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

DB_URI = environ.get("DB_URI")
VK_TOKEN_CLIENT = environ.get("VK_TOKEN_CLIENT")
VK_TOKEN_GROUP = environ.get("VK_TOKEN_GROUP")
VK_GROUP_ID = environ.get("VK_GROUP_ID")
