import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()

def init_database() -> Database:
    client: MongoClient = MongoClient(os.getenv("MONGO_URI"))
    return client.human_resources

def init_employee_repo(database: Database) -> Collection:
    return database.employee_repo

def init_department_repo(database: Database) -> Collection:
    return database.department_repo

def init_benefit_repo(database: Database) -> Collection:
    return database.benefit_repo

db = init_database()
employee_repo = init_employee_repo(db)
department_repo = init_department_repo(db)
benefit_repo = init_department_repo(db)
