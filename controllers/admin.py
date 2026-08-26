from services.db_service import DatabaseService
from services.bot_service import BotService


class AdminController:
    def __init__(self):
        self.db = DatabaseService()
        self.bot = BotService()

    def list_users(self):
        return self.db.load_users()

    def list_all_records(self):
        return self.db.load_records()

    def create_user(self, user):
        self.db.add_user(user)
        self.bot.notify_admin_action("create_user", f"user={user.username}")

    def delete_user(self, user_id, current_user_id):
        if user_id == current_user_id:
            return False

        self.db.delete_user(user_id)
        self.bot.notify_admin_action("delete_user", f"user_id={user_id}")
        return True