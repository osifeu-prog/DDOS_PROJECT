# deployment/server.py
import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import logging
from threading import Thread

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# --- הגדרות ---
# קריאת משתנים מתוך .env
WEBHOOK_PATH = os.environ.get("TELEGRAM_WEBHOOK_PATH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

# הגדרת Flask App (שימו לב לנתיבים לתיקיות templates ו-assets)
app = Flask(__name__, template_folder='../templates', static_folder='../assets')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app, name='לוח בקרה DDOS', template_mode='bootstrap4', url='/admin')

# --- מודלים של DB (SQLAlchemy) ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def __repr__(self): return f'<User {self.username}>'

class UploadedData(db.Model):
    __tablename__ = 'uploaded_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)
    data_content = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class TelegramConnection(db.Model):
    __tablename__ = 'telegram_connections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

# --- הגדרות Admin Panel ---
class SecureModelView(ModelView):
    # כאן נדרש יישום של מערכת Login אמיתית
    def is_accessible(self):
        # בפרויקט אמיתי: יש להשתמש ב-Flask-Login/Security
        return True 

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

admin.add_view(SecureModelView(User, db.session, name='משתמשים'))
admin.add_view(SecureModelView(UploadedData, db.session, name='נתונים שהועלו'))
admin.add_view(SecureModelView(TelegramConnection, db.session, name='חיבורי טלגרם'))

# --- לוגיקת בוט טלגרם (מבוסס webhook) ---
# נשתמש בגישת Threading כדי לא לחסום את שרת ה-Flask (בפרודקשן מומלץ Async)
try:
    bot = Bot(BOT_TOKEN)
    dispatcher = Dispatcher(bot, None, workers=0)

    # Handlers
    async def start_command(update, context):
        """טיפול בפקודת /start"""
        chat_id = update.message.chat_id
        # דוגמה ללוגיקה: קישור משתמש אדמין חדש
        with app.app_context():
            conn = TelegramConnection.query.filter_by(chat_id=chat_id).first()
            if not conn:
                # מנסים לקשר למשתמש האדמין הראשי
                system_user = User.query.filter_by(username=ADMIN_USER).first() 
                if system_user:
                     new_conn = TelegramConnection(user_id=system_user.id, chat_id=chat_id, is_active=True)
                     db.session.add(new_conn)
                     db.session.commit()
                     await update.message.reply_text(f"ברוך הבא! הצ'אט שלך קושר למשתמש המנהל.")
                     return
            
            if conn:
                 await update.message.reply_text("אתה כבר מחובר למערכת DDOS.")
            else:
                 await update.message.reply_text("ברוך הבא לבוט DDOS! אנא בצע קישור למערכת דרך האתר.")

    async def handle_message(update, context):
        """טיפול בהודעות רגילות ושמירתן ב-DB"""
        text = update.message.text
        with app.app_context():
            conn = TelegramConnection.query.filter_by(chat_id=update.message.chat_id).first()
            if conn:
                # שמירת הנתון בטבלת uploaded_data
                new_data = UploadedData(
                    user_id=conn.user_id,
                    data_type='Telegram Message',
                    data_content=text,
                    status='Review'
                )
                db.session.add(new_data)
                db.session.commit()
                await update.message.reply_text(f"הנתון נשמר לבדיקה בלוח הבקרה! (id: {new_data.id})")
            else:
                 await update.message.reply_text("אנא התחל את הבוט מחדש עם /start ובצע קישור למערכת.")


    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    def run_dispatcher(update_json):
        update = Update.de_json(update_json, bot)
        # הרצת העיבוד ב-Thread נפרד
        Thread(target=lambda: dispatcher.process_update(update)).start()

except Exception as e:
    logging.error(f"Failed to initialize Telegram Bot: {e}")

# --- נתיבי Web/API ---
@app.route('/', methods=['GET'])
def index():
    """דף הבית"""
    return render_template('index.html', project_name='פרויקט DDOS/NDFS')

@app.route(WEBHOOK_PATH, methods=['POST'])
def telegram_webhook():
    """הנקודה אליה טלגרם שולח עדכונים (WebHook)"""
    if request.method == "POST":
        if 'bot' in globals():
            run_dispatcher(request.get_json())
        return 'OK'
    return 'Method Not Allowed', 405

# --- פקודות CLI לאתחול (Flask CLI) ---
@app.cli.command("init-db")
def init_db_command():
    """יוצרת את טבלאות ה-DB ומגדירה משתמש אדמין ראשי."""
    with app.app_context():
        db.create_all()
        if User.query.filter_by(username=ADMIN_USER).first() is None:
            admin_user = User(username=ADMIN_USER, email=ADMIN_EMAIL, is_admin=True)
            admin_user.set_password(ADMIN_PASSWORD)
            db.session.add(admin_user)
            db.session.commit()
            print(f"*** נוצר משתמש אדמין: {ADMIN_USER} עם סיסמה: {ADMIN_PASSWORD} ***")
        print("מסד הנתונים אותחל בהצלחה.")

@app.cli.command("set-webhook")
def set_webhook_command():
    """מגדירה את ה-Webhook בטלגרם. דורש כתובת URL ציבורית HTTPS."""
    if not BOT_TOKEN:
        print("שגיאה: BOT_TOKEN אינו מוגדר.")
        return
    
    SERVER_URL = input("אנא הזן את כתובת ה-URL הציבורית המלאה של השרת (לדוגמה: https://yourdomain.com): ")
    webhook_url = SERVER_URL.rstrip('/') + WEBHOOK_PATH
    
    try:
        import requests
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        response = requests.post(url, json={'url': webhook_url})
        
        if response.json().get('ok'):
            print(f"Webhook הוגדר בהצלחה לכתובת: {webhook_url}")
        else:
            print(f"שגיאה בהגדרת ה-Webhook: {response.json()}")
    except Exception as e:
        print(f"שגיאה כללית בהגדרת Webhook: {e}")


if __name__ == '__main__':
    # הרצה מקומית לצורך בדיקה (לא מתאים לפרודקשן)
    # הערה: Webhook לא יעבוד בסביבה מקומית ללא מנהרת SSL (כגון ngrok).
    app.run(host='0.0.0.0', port=5000)
