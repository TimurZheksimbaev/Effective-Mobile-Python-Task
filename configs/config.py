import os

from dotenv import load_dotenv


load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int("SERVER_PORT")