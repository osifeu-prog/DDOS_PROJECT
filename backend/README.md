# SLH DDOS × BOT_FACTORY – Enterprise Backend

שירות FastAPI קטן שמייצג את שכבת ה-Enterprise של DDOS:

## Endpoints

- `/` – מידע כללי על השירות.
- `/health` – בריאות (לריילווי / קוברנטיס).
- `/ddos/summary` – סיכום קצר של שכבות DDOS והמודולים המרכזיים.
- `/ddos/investor_flow` – זרימת משקיע דרך BOT_FACTORY וה-DDOS העתידי.
- `/integrations/bot_factory/status` – בדיקת חיבור ל-BOT_FACTORY (דרך `BOT_FACTORY_BASE_URL`).

## הפעלה מקומית

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # ב-Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

בדיקות:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/ddos/summary
- http://127.0.0.1:8000/docs
