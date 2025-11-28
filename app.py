from flask import Flask, render_template, request, redirect, session, jsonify
from bson import ObjectId
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta, time, date
#from mailer import send_admin_email, send_client_email
from mailer import send_admin_email, send_client_email

from db import appointments, users

app = Flask(__name__)
app.secret_key = "this_is_my_secret_key_123"


# -------------------
# דף הבית
# -------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------
# יצירת שעות זמינות
# -------------------
def generate_time_slots():
    start = time(10, 0)
    end = time(20, 0)
    interval = timedelta(minutes=20)

    slots = []
    current = datetime.combine(date.today(), start)
    end_dt = datetime.combine(date.today(), end)

    while current <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += interval

    return slots


# -------------------
# API להחזרת שעות פנויות לפי תאריך
# -------------------
@app.route("/api/free-slots")
def api_free_slots():
    selected_date = request.args.get("date")

    if not selected_date:
        return jsonify(slots=[])

    slots = generate_time_slots()

    taken = appointments.find({"date": selected_date})
    taken_hours = {a["hour"] for a in taken}

    free_slots = [s for s in slots if s not in taken_hours]

    return jsonify(slots=free_slots)


# -------------------
# דף קביעת התור
# -------------------
@app.route("/book", methods=["GET"])
def book_form():
    today = date.today().isoformat()
    return render_template("book.html", today=today)


# -------------------
# שמירת תור
# -------------------
@app.route("/book", methods=["POST"])
def book_submit():

    date_selected = request.form["date"]
    dt = datetime.strptime(date_selected, "%Y-%m-%d").date()

    if dt < date.today():
        return jsonify(status="error", msg="אי אפשר לקבוע תור בעבר.")

    if dt.weekday() == 5:
        return jsonify(status="error", msg="אין עבודה בשבת.")

    name = request.form["name"]
    phone = request.form["phone"]
    service = request.form["service"]
    hour = request.form["hour"]
    email = request.form["email"]

    existing = appointments.find_one({
        "date": date_selected,
        "hour": hour
    })

    if existing:
        return jsonify(status="error", msg="השעה שבחרת כבר תפוסה.")

    appointments.insert_one({
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "date": date_selected,
        "hour": hour,
        "status": "pending"
    })

    # מייל למנהל
    send_admin_email(name, phone, service, date_selected, hour)

    # ללקוח – בקשה ממתינה לאישור
    send_client_email(
        email,
        name,
        service,
        date_selected,
        hour,
        status="pending"
    )

    return jsonify(status="success")


# -------------------
# ניהול תורים
# -------------------
@app.route("/admin/appointments")
def admin_appointments():
    if not session.get("admin_logged"):
        return redirect("/admin/login")

    selected_date = request.args.get("date")  # נלקח מה-query string ?date=...

    query = {}
    if selected_date:
        query["date"] = selected_date  # אצלך התאריך נשמר כ-"YYYY-MM-DD"

    appts = list(
        appointments.find(query).sort([("date", 1), ("hour", 1)])
    )

    return render_template(
        "admin_appointments.html",
        appointments=appts,
        selected_date=selected_date
    )

@app.route("/admin/approve/<id>")
def admin_approve(id):
    if not session.get("admin_logged"):
        return redirect("/admin/login")

    appt = appointments.find_one({"_id": ObjectId(id)})
    if not appt:
        return redirect("/admin/appointments")

    appointments.update_one(
        {"_id": appt["_id"]},
        {"$set": {"status": "approved"}}
    )

    # מייל ווואטסאפ ללקוח – התור אושר
    send_client_email(
        appt["email"],
        appt["name"],
        appt["service"],
        appt["date"],
        appt["hour"],
        status="approved",
    )
   
    return redirect("/admin/appointments")


@app.route("/admin/cancel/<id>")
def admin_cancel(id):
    if not session.get("admin_logged"):
        return redirect("/admin/login")

    appt = appointments.find_one({"_id": ObjectId(id)})
    if not appt:
        return redirect("/admin/appointments")

    appointments.update_one(
        {"_id": appt["_id"]},
        {"$set": {"status": "canceled"}}
    )

    # מייל ווואטסאפ ללקוח – התור בוטל
    send_client_email(
        appt["email"],
        appt["name"],
        appt["service"],
        appt["date"],
        appt["hour"],
        status="canceled",
    )
   

    return redirect("/admin/appointments")


@app.route("/admin/delete/<id>")
def admin_delete(id):
    if not session.get("admin_logged"):
        return redirect("/admin/login")
    appointments.delete_one({"_id": ObjectId(id)})
    return redirect("/admin/appointments")


# -------------------
# התחברות מנהל
# -------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = users.find_one({"username": username})

    if not user:
        return "משתמש לא קיים"

    if not check_password_hash(user["password"], password):
        return "סיסמה שגויה"

    session["admin_logged"] = True
    return redirect("/admin/appointments")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged"):
        return redirect("/admin/login")

    today = date.today().isoformat()

    total_today = appointments.count_documents({"date": today})
    pending = appointments.count_documents({"status": "pending"})
    approved = appointments.count_documents({"status": "approved"})
    canceled = appointments.count_documents({"status": "canceled"})

    today_dt = date.today()
    week_dt = today_dt - timedelta(days=7)

    total_week = appointments.count_documents({
        "date": {"$gte": week_dt.isoformat()}
    })

    # תורים של היום להצגה בדשבורד
    appts_today = list(appointments.find(
        {"date": today}
    ).sort([("hour", 1)]))

    return render_template(
        "admin_dashboard.html",
        total_today=total_today,
        total_week=total_week,
        pending=pending,
        approved=approved,
        canceled=canceled,
        appointments_today=appts_today,
        today=today
    )

@app.route("/admin/logout")
def admin_logout():
    # מוחק את כל המידע מה־session
    session.clear()

    # הפניה לדף ניתוק
    return redirect("/logout-message")
@app.route("/logout-message")
def logout_message():
    return render_template("logout_message.html")

# -------------------
# הרצה
# -------------------
if __name__ == "__main__":
    app.run(debug=True, port=5009)
