import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_ADDRESS = os.environ.get("DB_ADDRESS")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
ENV = os.environ.get("ENV", "DEV")

STARK_BANK_BASE_URL = {
    "SANDBOX": "https://sandbox.api.starkbank.com/v2",
    "DEV": "https://dev.external.com",
}.get(ENV.upper())
DEBUG = True if os.environ.get("DEBUG", "TRUE").upper() == "TRUE" else False
