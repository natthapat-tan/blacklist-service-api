from dotenv import load_dotenv
import os

load_dotenv("src/env/.env")

# ===========================================
# Config
# ===========================================

APP_NAME = os.getenv("APP_NAME")
LOG_LEVEL = os.getenv("LOG_LEVEL")

# *******************************************
