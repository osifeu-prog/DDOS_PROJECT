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
    version="0.2.0",
)


@app.get("/", tags=["meta"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "public_base_url": settings.PUBLIC_BASE_URL,
        "docs_url": settings.DOCS_URL,
        "message": "DDOS Enterprise Pack backend is running.",
    }


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}


@app.get("/ddos/summary", tags=["ddos"])
async def ddos_summary():
    return {
        "vision": "Digital Democratic Operating System למדינה וקהילות, עם ZKP, Escalation ו-NDFS.",
        "layers": [
            "Layer 1 – DDOS Main Chain (Permissioned Consortium, PoS/DPoS)",
            "Layer 2 – Micro-Democracy & Sub-Chains (ועדי בתים/שכונות/קהילות)",
            "Layer 3 – ZK-Rollups / Aggregation Layer לאיגום הצבעות וטרנזקציות",
        ],
        "modules": [
            "ID & ZKP Management – זהות ריבונית ואנונימית",
            "Escalation Engine – מנגנון מדרג וניטוב נושאים אוטומטי",
            "Micro-Democracy – ניהול ועדי בתים/רחובות/שכונות",
            "NDFS – National Digital Fiduciary System (כסף מתוכנת)",
        ],
    }


@app.get("/ddos/investor_flow", tags=["ddos"])
async def ddos_investor_flow():
    return {
        "steps": [
            "1. משקיע נכנס לבוט BOT_FACTORY ומבצע /start.",
            "2. המשקיע מקשר כתובת BNB באמצעות /link_wallet.",
            "3. אדמין מקצה SLH Off-Chain (לדוגמה, /admin_credit).",
            "4. /balance ו-/summary מציגים On-Chain + Off-Chain.",
            "5. בעתיד, DDOS יציג את השפעת המדיניות/הצבעות על הארנק (NDFS).",
        ],
        "note": "API זה מדמה את הזרימה, וניתן להרחיבו כדי למשוך נתונים אמיתיים מבוט BOT_FACTORY והשרת הקיים.",
    }


@app.get("/integrations/bot_factory/status", tags=["integrations"])
async def bot_factory_status():
    if not settings.BOT_FACTORY_BASE_URL:
        raise HTTPException(status_code=503, detail="BOT_FACTORY_BASE_URL is not configured")

    url = f"{settings.BOT_FACTORY_BASE_URL.rstrip('/')}/health"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(url)
        try:
            body = r.json()
        except Exception:
            body = r.text
        return {
            "integration": "bot_factory",
            "target": url,
            "status_code": r.status_code,
            "body": body,
        }
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=f"Error calling BOT_FACTORY health: {exc!r}")
