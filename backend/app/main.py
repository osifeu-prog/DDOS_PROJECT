from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx

from .settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "שירות Enterprise עבור SLH DDOS × BOT_FACTORY: "
        "API פרזנטטיבי שמרכז את הארכיטקטורה, החזון, ומצב האינטגרציה אל BOT_FACTORY."
    ),
    version=settings.VERSION,
)


@app.get("/health", tags=["system"])
async def health() -> dict:
    """בדיקת חיים בסיסית עבור Railway / ניטור.

    מחזיר:
        dict: אובייקט קטן שמסמן שהשירות חי.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME, "version": settings.VERSION}


@app.get("/ddos/summary", tags=["ddos"])
async def ddos_summary() -> dict:
    """סיכום קצר של DDOS למשקיעים / אינטגרציה.

    זה Endpoint סטטי שמאפשר לאתרים, מצגות וכלי BI לשלוף תיאור
    טקסטואלי ותמציתי של הרעיון.
    """
    return {
        "project": "DDOS – Digital Democratic Operating System",
        "highlights": [
            "Permissioned Consortium Blockchain עם ZKP להצבעות אנונימיות וחד-פעמיות",
            "מנוע Escalation חכם שמעלה נושאים שלא טופלו במדרג הממשלתי",
            "Micro-Democracy – ניהול ועדי בתים/שכונות/ערים בערוצי משנה (Sub-Chains)",
            "שכבת כספים NDFS – כסף מתוכנת לרווחה, יוקר מחיה וקצבאות מותנות",
        ],
        "docs": {
            "executive_summary": str(settings.DOCS_URL).rstrip("/") + "/executive_summary.html",
            "architecture": str(settings.DOCS_URL).rstrip("/") + "/ddos_architecture.html",
        },
    }


@app.get("/ddos/investor_flow", tags=["ddos"])
async def ddos_investor_flow() -> dict:
    """תיאור מסלול משקיע: מהבוט בטלגרם ועד קריאת ה-API.

    זה Endpoint דוקומנטרי בלבד – הוא לא מחזיק מידע אישי, אלא Flow לוגי
    שהאתר / חומרים למשקיעים יכולים להציג.
    """
    return {
        "steps": [
            "המשקיע נכנס לבוט המשקיעים בטלגרם ומבצע /start.",
            "המשקיע מקשר כתובת BNB (BSC) באמצעות /link_wallet.",
            "בצד השרת, BOT_FACTORY מקליט את ההשקעה ומקצה SLH Off-Chain.",
            "שירות ה-DDOS Enterprise יכול לשאוב בעתיד נתוני Aggregation / מדדים ויזואליים.",
            "בדשבורד ה-DDOS / האתר, המשקיע רואה איך החלטות מדיניות מתחברות לזרימת ההון.",
        ],
        "bot_factory_hint": "האינטגרציה בפועל נעשית בבוט וב-DB, כאן זו שכבת תיעוד ו-API read-only.",
    }


@app.get("/integrations/bot_factory/status", tags=["integrations"])
async def bot_factory_status() -> dict:
    """פינג לבריאות שירות BOT_FACTORY (אם הוגדר URL).

    אם BOT_FACTORY_BASE_URL לא מוגדר, מחזירים תשובה אינפורמטיבית
    כדי שה-Frontend ידע להציג הודעה עדינה.
    """
    if not settings.BOT_FACTORY_BASE_URL:
        return {
            "integration": "bot_factory",
            "configured": False,
            "message": "BOT_FACTORY_BASE_URL לא הוגדר ב-Environment – אין בדיקת בריאות חיה.",
        }

    url = str(settings.BOT_FACTORY_BASE_URL).rstrip("/") + "/health"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(url)
        try:
            body = r.json()
        except Exception:
            body = r.text
        return {
            "integration": "bot_factory",
            "configured": True,
            "target": url,
            "status_code": r.status_code,
            "body": body,
        }
    except Exception as exc:  # pragma: no cover
        # שומרים על שגיאה רכה – 502 – כדי ש-Nginx / Railway יבינו שזה בעיית אינטגרציה בלבד.
        raise HTTPException(status_code=502, detail=f"Error calling BOT_FACTORY health: {exc!r}")
