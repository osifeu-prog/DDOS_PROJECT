# קובץ server.py
# שרת Flask מאוחד: מטפל ב-Frontend, Backend, Admin, DB ו-Telegram Alerts

from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
import psycopg2
from psycopg2 import extras
import os
import json
import requests
from dotenv import load_dotenv

# טעינת משתני סביבה מקובץ .env מקומי לפיתוח, ב-Railway נטענים אוטומטית
load_dotenv() 

app = Flask(__name__, static_folder='../src')

# --- תצורה ---
app.secret_key = os.urandom(24) 
# Railway מספקת DATABASE_URL באופן אוטומטי.
DATABASE_URL = os.getenv("DATABASE_URL")

# הגדרות Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# פרטי אדמין
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "ddos_admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
# ------------------

# --- פונקציות בסיס ---

def get_db_connection():
    # חיבור באמצעות DATABASE_URL שמספקת Railway
    if not DATABASE_URL:
        raise ConnectionError("DATABASE_URL is not set. Cannot connect to PostgreSQL.")
    return psycopg2.connect(DATABASE_URL)

def send_telegram_alert(message):
    try:
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': f"🔔 DDOS ALERT:\n{message}",
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"Telegram failed. Status: {response.status_code}, Response: {response.text}")
        else:
            print("Telegram credentials missing. Alert skipped.")
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")

# --- ניתוב קבצים סטטיים ---
# (נותר זהה: מגיש index.html, assets, וכו')
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(os.getcwd(), 'assets'), path)

@app.route('/src/<path:path>')
def serve_src(path):
    return send_from_directory(app.static_folder, path)

# --- נקודות קצה (API) ---

# 1. רישום משתמשים (טלפון)
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    phone_number = data.get('phone')
    if not phone_number: return jsonify({"error": "נדרש מספר טלפון"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # הקוד משתמש ב-ON CONFLICT כדי למנוע כפילויות
        cur.execute("INSERT INTO registered_users (phone_number) VALUES (%s) ON CONFLICT (phone_number) DO NOTHING RETURNING id;", (phone_number,))
        new_id = cur.fetchone()
        conn.commit()
        
        if new_id:
            send_telegram_alert(f"New User Registered! Phone: {phone_number} (ID: {new_id[0]})")
            return jsonify({"message": "רישום בוצע בהצלחה", "id": new_id[0]}), 201
        else:
            return jsonify({"message": "המספר כבר רשום"}), 200
    except Exception as e:
        print(f"Registration Error: {e}")
        conn.rollback()
        return jsonify({"error": "שגיאת שרת פנימית"}), 500
    finally:
        cur.close()
        conn.close()

# 2. קבלת פנייה לאדמין
@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.json
    name = data.get('name', 'Anon')
    email = data.get('email', 'N/A')
    message_body = data.get('message')
    
    if not message_body: return jsonify({"error": "חסר תוכן הודעה"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO messages (sender_name, sender_email, content, ip_address) VALUES (%s, %s, %s, %s) RETURNING id;", 
                    (name, email, message_body, request.remote_addr))
        message_id = cur.fetchone()[0]
        conn.commit()
        
        # התראת טלגרם על הודעה חדשה
        alert_msg = (f"New Admin Message (ID: {message_id})\n"
                     f"Sender: {name} ({email})\n"
                     f"Content: {message_body[:50]}...")
        send_telegram_alert(alert_msg)
        
        return jsonify({"message": "הודעה נשלחה בהצלחה לאדמין"}), 201
    except Exception as e:
        print(f"Message Error: {e}")
        conn.rollback()
        return jsonify({"error": "שגיאת שרת פנימית"}), 500
    finally:
        cur.close()
        conn.close()

# 3. לוג כניסה וצפייה (חוק 13)
@app.route('/api/log_entry', methods=['POST'])
def log_entry():
    ip_address = request.remote_addr
    # ... (שאר לוגיקת הלוגינג נותרה זהה) ...
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO access_logs (ip_address, user_agent, page_viewed, session_data)
            VALUES (%s, %s, %s, %s)
        """, (ip_address, request.headers.get('User-Agent'), request.path, json.dumps(dict(request.headers))))
        
        conn.commit()
        return jsonify({"message": "Entry logged"}), 200
    except Exception as e:
        print(f"Logging Error: {e}")
        conn.rollback()
        return jsonify({"error": "שגיאת לוגינג"}), 500
    finally:
        cur.close()
        conn.close()

# 4. סטטיסטיקות האתר
@app.route('/api/stats', methods=['GET'])
def get_stats():
    # ... (הקוד נותר זהה) ...
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM registered_users;")
        registered_users = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM access_logs;")
        total_views = cur.fetchone()[0]
        
        return jsonify({"registered_users": registered_users, "total_views": total_views}), 200
    except Exception as e:
        print(f"Stats Error: {e}")
        return jsonify({"registered_users": 0, "total_views": 0}), 500
    finally:
        cur.close()
        conn.close()


# --- ממשק אדמין (נשאר זהה) ---
# ... (ניתובים admin, admin_login, admin_logout, ופונקציות העזר נשארים זהים לגרסה הקודמת) ...
@app.route('/admin')
def admin_page():
    if 'logged_in' not in session:
        return serve_admin_login()
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM messages ORDER BY access_time DESC;")
        messages = cur.fetchall()
        cur.execute("SELECT * FROM registered_users ORDER BY registration_date DESC;")
        users = cur.fetchall()
        
        return generate_admin_html(messages, users)
    except Exception as e:
        print(f"Admin DB Error: {e}")
        return "שגיאה בטעינת נתונים.", 500
    finally:
        cur.close()
        conn.close()

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('admin_page'))
    else:
        return serve_admin_login("שם משתמש או סיסמה שגויים.")

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('serve_index'))


def serve_admin_login(error=None):
    # הצגת טופס לוגין פשוט
    html = f"""
    <!DOCTYPE html><html lang="he" dir="rtl"><head><title>Admin Login</title><link rel="stylesheet" href="/assets/style.css"></head>
    <body style="text-align: center; padding-top: 50px; background-color: #121212; color: white;">
    <div style="max-width: 400px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 10px; border: 1px solid #673ab7;">
    <h2>כניסת מנהל DDOS</h2>
    {f'<p style="color: red;">{error}</p>' if error else ''}
    <form method="POST" action="/admin/login">
        <input type="text" name="username" placeholder="שם משתמש" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #00bcd4; background: #333; color: white; border-radius: 5px;"><br>
        <input type="password" name="password" placeholder="סיסמה" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #00bcd4; background: #333; color: white; border-radius: 5px;"><br>
        <button type="submit" style="padding: 10px 20px; background-color: #00bcd4; color: black; border: none; border-radius: 5px; cursor: pointer;">התחבר</button>
    </form>
    </div></body></html>
    """
    return html

def generate_admin_html(messages, users):
    # יצירת ממשק אדמין בסיסי
    message_rows = "".join([f"<tr><td>{m['id']}</td><td>{m['sender_name']} ({m['sender_email']})</td><td>{m['content']}</td><td>{m['access_time'].strftime('%Y-%m-%d %H:%M')}</td><td>{m['ip_address']}</td></tr>" for m in messages])
    user_rows = "".join([f"<tr><td>{u['id']}</td><td>{u['phone_number']}</td><td>{u['registration_date'].strftime('%Y-%m-%d %H:%M')}</td></tr>" for u in users])

    html = f"""
    <!DOCTYPE html><html lang="he" dir="rtl"><head><title>DDOS Admin Panel</title><link rel="stylesheet" href="/assets/style.css"></head>
    <body style="padding: 20px; background-color: #121212; color: white;">
    <h1 style="color: #00bcd4; border-bottom: 2px solid #673ab7; padding-bottom: 10px;">DDOS | לוח בקרה למנהל</h1>
    <a href="/admin/logout" style="float: left; color: red;">התנתק</a>
    
    <h2>1. פניות חדשות ({len(messages)})</h2>
    <table border="1" style="width: 100%; text-align: right; border-collapse: collapse; margin-bottom: 40px; background-color: #1e1e1e;">
        <tr><th>ID</th><th>שולח</th><th>תוכן</th><th>זמן קבלה</th><th>IP</th></tr>
        {message_rows}
    </table>

    <h2>2. משתמשים רשומים ({len(users)})</h2>
    <table border="1" style="width: 100%; text-align: right; border-collapse: collapse; background-color: #1e1e1e;">
        <tr><th>ID</th><th>מספר טלפון</th><th>תאריך רישום</th></tr>
        {user_rows}
    </table>
    
    <footer><p style="text-align: center; margin-top: 50px;">זכור: הפרויקט מופעל על Railway ומחובר אוטומטית ל-PostgreSQL.</p></footer>
    </body></html>
    """
    return html


# הוספנו תנאי הרצה מקומי שימושי לפיתוח (לא קריטי ל-Railway)
if __name__ == '__main__':
    @app.route('/assets/<path:path>')
    def serve_assets_dev(path):
        return send_from_directory(os.path.join(os.getcwd(), 'assets'), path)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
