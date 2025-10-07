import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("APP_URL")
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

