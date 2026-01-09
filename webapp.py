from flask import Flask, render_template, request, jsonify
from crm_db import *
app = Flask(__name__)
init_db()

@app.route("/")
def index():
    # Правильный парсинг tgWebAppData
    tg_data = request.args.get('tgWebAppData', '')
    telegram_id = 60973352  # Твой ID по умолчанию
    
    if tg_data:
        try:
            # Парсим query string
            params = {}
            for param in tg_data.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
            
            # Извлекаем user
            if 'user' in params:
                import json, urllib.parse
                user_json = urllib.parse.unquote(params['user'])
                user_data = json.loads(user_json)
                telegram_id = user_data.get('id', 0)
                print(f"User ID: {telegram_id}")  # Лог в Render
        except Exception as e:
            print(f"Parse error: {e}")
    
    ADMIN_IDS = [60973352]  # Твой ID!
    is_admin_user = telegram_id in ADMIN_IDS
    
    slots = get_free_slots()
    bookings = get_bookings()
    masters = get_masters()
    
    return render_template("index.html", 
                         slots=slots, bookings=bookings, masters=masters, 
                         is_admin=is_admin_user, debug_id=telegram_id)


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
