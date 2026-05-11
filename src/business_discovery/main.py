import os

import requests
from dotenv import load_dotenv
from pathlib import Path

from tools.web_search_tool.web_search_tool import searxng_web_search
from library.custom_log import log_errors
env_path = Path.cwd().parent.parent.joinpath("env").joinpath(".env")
log_errors(f"Environment FilePath {env_path}")
load_dotenv(override=True, dotenv_path=env_path)

print(os.getenv("APP_NAME"))

print(searxng_web_search.invoke({"searchStr" : "playwright"}))