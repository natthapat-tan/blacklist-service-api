from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
import os

class Config(BaseSettings):

    # ===========================================
    # Config
    # ===========================================

    APP_NAME: str
    LOG_LEVEL: str

    # *******************************************

    model_config = ConfigDict(case_sensitive = True, extra = "allow", env_file = "/src/env/.env")

@lru_cache
def get_env():
    return Config()