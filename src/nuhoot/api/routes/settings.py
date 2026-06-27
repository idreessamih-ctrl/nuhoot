"""API routes for Settings page — credential management + Meta OAuth."""

from __future__ import annotations

from typing import Annotated
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from nuhoot.config import settings as app_settings
from nuhoot.database import get_db
from nuhoot.models.settings import AppSetting
from nuhoot.translations import DEFAULT_LANG, SUPPORTED_LANGS, t
from nuhoot.utils.crypto import encrypt, decrypt, mask

router = APIRouter(tags=["settings"])

DbDep = Annotated[Session, Depends(get_db)]

_TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
templates.env.globals["t"] = t


def _valid_lang(lang: str) -> str:
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def _get_setting(db: Session, key: str) -> str:
    row = db.get(AppSetting, key) if False else db.execute(
        select(AppSetting).where(AppSetting.key == key)
    ).scalar_one_or_none()
    if row is None:
        return ""
    return decrypt(row.value) if row.is_secret else row.value


def _get_all_settings(db: Session) -> dict:
    rows = db.execute(select(AppSetting)).scalars().all()
    result = {}
    for row in rows:
        val = decrypt(row.value) if row.is_secret else row.value
        result[row.key] = val
    return result


@router.get("/settings", response_model=None)
def settings_page(request: Request, db: DbDep, lang: str = "ar", msg: str = "") -> object:
    lang = _valid_lang(lang)
    stored = _get_all_settings(db)

    # Build display values (mask secrets)
    display = {}
    for key, meta in AppSetting.KEYS.items():
        val = stored.get(key, "")
        if val and meta["secret"]:
            display[key] = mask(val)
        elif val:
            display[key] = val
        else:
            display[key] = ""

    # Connection status
    whatsapp_connected = bool(stored.get("whatsapp_access_token"))
    ai_connected = bool(stored.get("umans_api_key"))
    maps_connected = bool(stored.get("google_maps_api_key"))

    result = templates.TemplateResponse(
        request,
        "settings.html",
        {
            "lang": lang,
            "active": "settings",
            "display": display,
            "whatsapp_connected": whatsapp_connected,
            "ai_connected": ai_connected,
            "maps_connected": maps_connected,
            "meta_app_id": app_settings.meta_app_id,
            "msg": msg,
        },
    )
    result.set_cookie("lang", lang, max_age=2592000)
    return result


@router.post("/settings/api-keys", response_model=None)
def save_api_keys(
    db: DbDep,
    lang: str = Form("ar"),
    umans_api_key: str = Form(""),
    google_maps_api_key: str = Form(""),
) -> RedirectResponse:
    """Save API keys (encrypted)."""
    for key, value, is_secret in [
        ("umans_api_key", umans_api_key, True),
        ("google_maps_api_key", google_maps_api_key, True),
    ]:
        if not value:
            continue
        existing = db.execute(
            select(AppSetting).where(AppSetting.key == key)
        ).scalar_one_or_none()
        encrypted = encrypt(value) if is_secret else value
        if existing:
            existing.value = encrypted
        else:
            db.add(AppSetting(key=key, value=encrypted, is_secret=1 if is_secret else 0))
    db.commit()
    return RedirectResponse(url=f"/settings?lang={lang}&msg=saved", status_code=303)


@router.post("/settings/whatsapp/connect", response_model=None)
def whatsapp_connect(
    db: DbDep,
    lang: str = Form("ar"),
    code: str = Form(...),
    phone_number_id: str = Form(""),
) -> RedirectResponse | JSONResponse:
    """Exchange Meta Embedded Signup code for permanent access token."""
    if not app_settings.meta_app_id or not app_settings.meta_app_secret:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Meta App ID/Secret not configured"},
        )

    # Exchange code for long-lived token
    token_url = "https://graph.facebook.com/v21.0/oauth/access_token"
    params = {
        "client_id": app_settings.meta_app_id,
        "client_secret": app_settings.meta_app_secret,
        "code": code,
    }
    try:
        resp = httpx.post(token_url, params=params, timeout=30)
        data = resp.json()
    except Exception as exc:
        return JSONResponse(
            status_code=502,
            content={"success": False, "error": f"Meta API error: {exc}"},
        )

    access_token = data.get("access_token", "")
    if not access_token:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": f"No token in response: {data}"},
        )

    # Store credentials
    for key, value in [
        ("whatsapp_access_token", access_token),
        ("whatsapp_phone_number_id", phone_number_id),
    ]:
        existing = db.execute(
            select(AppSetting).where(AppSetting.key == key)
        ).scalar_one_or_none()
        encrypted = encrypt(value)
        if existing:
            existing.value = encrypted
        else:
            db.add(AppSetting(key=key, value=encrypted, is_secret=1))

    db.commit()
    return RedirectResponse(url=f"/settings?lang={lang}&msg=whatsapp_connected", status_code=303)


@router.post("/settings/whatsapp/disconnect", response_model=None)
def whatsapp_disconnect(db: DbDep, lang: str = Form("ar")) -> RedirectResponse:
    """Remove WhatsApp credentials."""
    for key in ["whatsapp_access_token", "whatsapp_phone_number_id"]:
        existing = db.execute(
            select(AppSetting).where(AppSetting.key == key)
        ).scalar_one_or_none()
        if existing:
            db.delete(existing)
    db.commit()
    return RedirectResponse(url=f"/settings?lang={lang}&msg=disconnected", status_code=303)
