from flask import Flask, render_template, request, jsonify
from crm_db import *
app = Flask(__name__)
init_db()

@app.route("/")
def index():
    tg_init_data = request.args.get('tg_init_data', '')
    telegram_id = 0  # Парсим из tg_init_data для ролей
    if tg_init_data:
        # Простой парсинг user ID из Telegram data
        for param in tg_init_data.split('&'):
            if param.startswith('user%5fid'):
                telegram_id = int(param.split('=')[1])
                break
    
    is_admin_user = is_admin(telegram_id)
    slots = get_free_slots()
    bookings = get_bookings()
    masters = get_masters()
    
    return render_template("index.html", slots=slots, bookings=bookings, masters=masters, is_admin=is_admin_user)

@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.json
    if book_slot(data['slot_id']):
        create_booking(data['slot_id'], data['name'], data['phone'], data['place'])
        return jsonify({"ok": True, "message": "✅ Запись создана!"})
    return jsonify({"ok": False, "error": "❌ Слот занят"}), 400

@app.route("/api/add_slot", methods=["POST"])
def api_add_slot():
    data = request.json
    add_slot(data['master_id'], data['date'], data['time'])
    return jsonify({"ok": True})

@app.route("/api/add_master", methods=["POST"])
def api_add_master():
    data = request.json
    add_master(data['name'], data['telegram_id'])
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
