import hashlib
from datetime import datetime


class User:
    def __init__(self, id, username, password_hash, role="user", created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_password(self, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed == self.password_hash

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["username"],
            data["password_hash"],
            data["role"],
            data["created_at"]
        )