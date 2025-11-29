# SLH DDOS × BOT_FACTORY – Enterprise Pack v2

זו חבילה ברמת Enterprise שמחברת בין החזון המלא של DDOS לבין BOT_FACTORY –
שער המשקיעים והארנק הקהילתי על רשת BNB Smart Chain.

## מבנה

- `backend/` – שירות FastAPI:
  - `/health`, `/ddos/summary`, `/ddos/investor_flow`
  - `/integrations/bot_factory/status` – בדיקת חיבור לשער BOT_FACTORY קיים.

- `docs/` – מסמכי DDOS:
  - `executive_summary.md` – סיכום מנהלים.
  - `ddos_architecture.md` – ארכיטקטורה מסוכמת (ניתן להרחיב ל-Whitepaper מלא).

- `site/` – אתר משקיעים סטטי:
  - `index.html` – דף נחיתה יפה למשקיעים.
  - `style.css` – עיצוב כהה ומודרני.

## שימוש מהיר

### 1. Backend – הפעלה מקומית

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # ב-Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

בדיקה:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/ddos/summary
- http://127.0.0.1:8000/docs

### 2. פריסה ל-Railway

1. צור שירות חדש מתוך ריפו זה.
2. בחר Dockerfile: `backend/Dockerfile` (או העתק לשורש).
3. ודא שפורט היעד הוא 8080.
4. הגדר ENV, לדוגמה:

- `BOT_FACTORY_BASE_URL=https://tease-production.up.railway.app`

בדוק:

- `https://<your-ddos-service>.up.railway.app/health`
- `https://<your-ddos-service>.up.railway.app/integrations/bot_factory/status`

### 3. GitHub Pages – אתר משקיעים

1. דחוף ריפו לגיטהאב.
2. ב-Settings → Pages:
   - Source: Deploy from a branch
   - Branch: main
   - Folder: /site
3. קבל URL ושלח למשקיעים.

---

החבילה הזו נועדה להיות בסיס לפרזנטציה למשקיעים, המשך פיתוח DDOS מלא,
והעמקת הקשר בין הארכיטקטורה הגדולה לבין הבוט החי BOT_FACTORY.
