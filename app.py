from services.bot_service import BotService
import hashlib

from flask import Flask, render_template, request, redirect, url_for, session

from config import Config
from controllers.auth import AuthController, login_required
from controllers.admin import AdminController
from controllers.user import UserController
from models.user import User
from models.record import Record
from services.db_service import DatabaseService


app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

auth_controller = AuthController()
admin_controller = AdminController()
user_controller = UserController()
db = DatabaseService()
bot_service = BotService()

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))

    return redirect(url_for("user_dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success = auth_controller.login(username, password)

        if success:
            if session.get("role") == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("user_dashboard"))

        error = "Username or password incorrect."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    message = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, msg = auth_controller.register(username, password)

        if success:
            bot_service.notify_new_user(username)
            message = msg
        else:
            error = msg

    return render_template("register.html", error=error, message=message)


@app.route("/logout")
def logout():
    auth_controller.logout()
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
@login_required(role="admin")
def admin_dashboard():
    users = admin_controller.list_users()
    records = admin_controller.list_all_records()
    recent_users = users[-5:]

    return render_template(
        "admin_dashboard.html",
        total_users=len(users),
        total_records=len(records),
        recent_users=recent_users
    )


@app.route("/admin/users")
@login_required(role="admin")
def admin_users():
    users = admin_controller.list_users()
    return render_template("admin_users.html", users=users)


@app.route("/admin/users/create", methods=["POST"])
@login_required(role="admin")
def admin_create_user():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    users = db.load_users()
    new_id = len(users) + 1
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    user = User(
        id=new_id,
        username=username,
        password_hash=password_hash,
        role=role
    )

    admin_controller.create_user(user)

    return redirect(url_for("admin_users"))


@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required(role="admin")
def admin_delete_user(user_id):
    current_user_id = session.get("user_id")

    success = admin_controller.delete_user(user_id, current_user_id)

    if success:
        bot_service.notify_admin_action(
            "Delete User",
            f"User ID {user_id} deleted"
        )

    return redirect(url_for("admin_users"))


@app.route("/admin/data")
@login_required(role="admin")
def admin_data():
    page = request.args.get("page", 1, type=int)

    records = admin_controller.list_all_records()

    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    paginated_records = records[start:end]

    total_pages = (len(records) + per_page - 1) // per_page

    return render_template(
        "admin_data.html",
        records=paginated_records,
        page=page,
        total_pages=total_pages
    )

@app.route("/user/dashboard")
@login_required()
def user_dashboard():
    user_id = session.get("user_id")
    records = user_controller.get_my_records(user_id)

    return render_template("user_dashboard.html", records=records)


@app.route("/user/records/add", methods=["POST"])
@login_required()
def add_record():
    student_name = request.form.get("student_name")
    student_group = request.form.get("student_group")
    gpa = request.form.get("gpa")
    try:
        gpa = float(gpa)

        if gpa < 0 or gpa > 4:
            return "GPA must be between 0 and 4"

    except:
        return "Invalid GPA"

    user_id = session.get("user_id")

    records = db.load_records()
    new_id = len(records) + 1

    record = Record(
        id=new_id,
        user_id=user_id,
        student_name=student_name,
        student_group=student_group,
        gpa=gpa
    )

    db.add_record(record)
    bot_service.notify_admin_action(
        "New Record",
        f"{student_name} added with GPA {gpa}"
    )

    return redirect(url_for("user_dashboard"))


@app.route("/user/profile", methods=["GET", "POST"])
@login_required()
def profile():
    user_id = session.get("user_id")
    user = user_controller.get_profile(user_id)
    records = user_controller.get_my_records(user_id)

    message = None

    if request.method == "POST":
        new_password = request.form.get("password")

        if len(new_password) >= 6:
            user_controller.update_profile(user_id, new_password)
            bot_service.notify_admin_action(
                "Password Changed",
                f"User {user.username} changed password"
            )
            message = "Password updated successfully."
        else:
            message = "Password must be at least 6 characters long."

    return render_template(
        "profile.html",
        user=user,
        record_count=len(records),
        message=message
    )

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)