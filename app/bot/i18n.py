from __future__ import annotations

from typing import Dict
from app.core.config import settings


def _parse_supported() -> list[str]:
    raw = settings.SUPPORTED_LANGUAGES or "he,en,ru,es"
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.split(",")]
    else:
        # אם בעתיד נגדיר כ-list ב-Settings – נדע להתמודד
        try:
            parts = [str(p).strip() for p in raw]
        except TypeError:
            parts = []
    return [p for p in parts if p]


SUPPORTED_LANGS: list[str] = _parse_supported()
DEFAULT_LANG: str = settings.DEFAULT_LANGUAGE or "he"


def detect_lang(update) -> str:
    """קובע שפת עבודה לבוט לפי שפת המשתמש בטלגרם והגדרות ENV."""
    code = None
    try:
        if update.effective_user and update.effective_user.language_code:
            code = update.effective_user.language_code.split("-")[0]
    except Exception:
        code = None

    if code in SUPPORTED_LANGS:
        return code
    if DEFAULT_LANG in SUPPORTED_LANGS:
        return DEFAULT_LANG
    # fallback אחרון
    return "en"


MESSAGES: Dict[str, Dict[str, str]] = {
    "start_title": {
        "he": "ברוך הבא לשער המשקיעים של SLH",
        "en": "Welcome to the SLH Investor Gateway.",
        "ru": "Добро пожаловать в шлюз инвесторов SLH.",
        "es": "Bienvenido al portal de inversores de SLH.",
    },
    "start_subtitle": {
        "he": "כאן מנהלים את ההשקעה, הארנק הקהילתי והחיבור לאקו־סיסטם SLH.",
        "en": "Here you manage your investment, the community wallet and your link to the SLH ecosystem.",
        "ru": "Здесь вы управляете своей инвестицией, общим кошельком и связью с экосистемой SLH.",
        "es": "Aquí gestionas tu inversión, la wallet comunitaria y tu conexión al ecosistema SLH.",
    },
    "menu_title": {
        "he": "תפריט המשקיע של SLH – בחר פעולה:",
        "en": "SLH Investor Menu – choose an action:",
        "ru": "Меню инвестора SLH – выберите действие:",
        "es": "Menú de inversor SLH – elige una acción:",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """פונקציית תרגום פשוטה – עם fallback ל-en ואז לשם המפתח עצמו."""
    by_lang = MESSAGES.get(key, {})
    text = by_lang.get(lang) or by_lang.get("en") or key
    try:
        return text.format(**kwargs)
    except Exception:
        return text
