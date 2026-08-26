import hashlib
from functools import wraps

from flask import session, redirect, url_for, abort

from models.user import User
from services.db_service import DatabaseService
from services.bot_service import BotService


def login_required(role=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))

            if role is not None and session.get("role") != role:
                abort(403)

            return function(*args, **kwargs)

        return wrapper
    return decorator


class AuthController:
    def __init__(self):
        self.db = DatabaseService()
        self.bot = BotService()

    def login(self, username, password):
        user = self.db.get_user_by_username(username)

        if user is None:
            return False

        if user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return True

        return False

    def logout(self):
        session.clear()

    def register(self, username, password):
        if len(username) < 3 or len(password) < 6:
            return False, "Username кемінде 3, password кемінде 6 символ болуы керек."

        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return False, "Бұл username already exists."

        users = self.db.load_users()
        new_id = len(users) + 1

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        new_user = User(
            id=new_id,
            username=username,
            password_hash=password_hash,
            role="user"
        )

        self.db.add_user(new_user)
        self.bot.notify_new_user(username)

        return True, "User registered successfully."