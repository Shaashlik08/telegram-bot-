import json
import os

from config import Config
from models.user import User
from models.record import Record


class DatabaseService:
    def __init__(self):
        self.users_file = os.path.join(Config.DB_PATH, "users.json")
        self.records_file = os.path.join(Config.DB_PATH, "records.json")

    def load_users(self):
        with open(self.users_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [User.from_dict(item) for item in data]

    def save_users(self, users):
        data = [user.to_dict() for user in users]
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_records(self):
        with open(self.records_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Record.from_dict(item) for item in data]

    def save_records(self, records):
        data = [record.to_dict() for record in records]
        with open(self.records_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def get_user_by_username(self, username):
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(self, user_id):
        users = self.load_users()
        for user in users:
            if user.id == user_id:
                return user
        return None

    def add_user(self, user):
        users = self.load_users()
        users.append(user)
        self.save_users(users)

    def delete_user(self, user_id):
        users = self.load_users()
        users = [user for user in users if user.id != user_id]
        self.save_users(users)

        records = self.load_records()
        records = [record for record in records if record.user_id != user_id]
        self.save_records(records)

    def add_record(self, record):
        records = self.load_records()
        records.append(record)
        self.save_records(records)

    def get_records_by_user_id(self, user_id):
        records = self.load_records()
        return [record for record in records if record.user_id == user_id]