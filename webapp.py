
# webapp.py
from flask import Flask, render_template, request, jsonify
from crm_db import init_db, add_client, add_session, get_upcoming_sessions

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    sessions = get_upcoming_sessions()
    return render_template("index.html", sessions=sessions)

@app.route("/api/create", methods=["POST"])
def api_create():
    data = request.json or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    contact = data.get("contact", "").strip()
    comment = data.get("comment", "").strip()
    date = data.get("date", "").strip()
    time = data.get("time", "").strip()
    master = data.get("master", "").strip()
    zone = data.get("zone", "").strip()
    price = float(data.get("price") or 0)
    status = data.get("status", "booked")

    if not name or not date or not time:
        return jsonify({"ok": False, "error": "Имя, дата и время обязательны"}), 400

    client_id = add_client(name, phone, contact, comment)
    session_id = add_session(client_id, date, time, master, zone, price, status)

    return jsonify({"ok": True, "session_id": session_id})
    
if __name__ == "__main__":
    # Локальный запуск Mini App
    app.run(host="0.0.0.0", port=8000, debug=True)
