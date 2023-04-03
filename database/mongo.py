from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
import os

load_dotenv()

def init_database() -> Database:
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    CONNECTION_STRING = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.astc6fi.mongodb.net/retryWrites=true&w=majority"

    client: MongoClient = MongoClient(CONNECTION_STRING)

    return client.human_resources

def init_employee_repo():
    db = init_database()

    return db.employee_repo

def init_department_repo():
    db = init_database()

    return db.department_repo

def init_benefit_repo():
    db = init_database()

    return db.benefit_repo

if __name__ == "__main__":
    db = init_database()
    employee_repo = init_employee_repo()
    department_repo = init_department_repo()
    benefit_repo = init_benefit_repo()
