from datetime import datetime


class Record:
    def __init__(self, id, user_id, student_name, student_group, gpa, created_at=None):
        self.id = id
        self.user_id = user_id
        self.student_name = student_name
        self.student_group = student_group
        self.gpa = gpa
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_name": self.student_name,
            "student_group": self.student_group,
            "gpa": self.gpa,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["user_id"],
            data["student_name"],
            data["student_group"],
            data["gpa"],
            data["created_at"]
        )