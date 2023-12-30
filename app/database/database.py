from mongoengine import connect
from dotenv import load_dotenv
import os


def parse_database_creds():
    """
    Parses user creds and db host from config file
    :return:
    List - List[hostname, db_user, db_password]

    """
    try:
        load_dotenv()
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        return [host, user, password]
    except Exception as e:
        print(f"Error while getting creds from .env: {e}")


def global_init():
    """
    Function to connect MongoDB DB
    :return:
    """
    try:
        creds = parse_database_creds()
        connect(host=creds[0], username=creds[1], password=creds[2])
        print("DB Connection successfully done")
    except Exception as e:
        print(f"Error when connecting to DB: {e}")
