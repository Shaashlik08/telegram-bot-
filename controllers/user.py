import hashlib

from services.db_service import DatabaseService


class UserController:
    def __init__(self):
        self.db = DatabaseService()

    def get_profile(self, user_id):
        return self.db.get_user_by_id(user_id)

    def get_my_records(self, user_id):
        return self.db.get_records_by_user_id(user_id)

    def update_profile(self, user_id, new_password):
        users = self.db.load_users()

        for user in users:
            if user.id == user_id:
                user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                self.db.save_users(users)
                return True

        return False