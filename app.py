import os
import re
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class LeadIn(BaseModel):
    name: str
    phone: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not 1 <= len(v) <= 100:
            raise ValueError("Имя должно быть от 1 до 100 символов")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        v = v.strip()
        if not re.fullmatch(r"[0-9+()\- ]+", v):
            raise ValueError("Телефон содержит недопустимые символы")
        digits = re.sub(r"\D", "", v)
        if not 10 <= len(digits) <= 15:
            raise ValueError("Телефон должен содержать 10–15 цифр")
        return v


async def send_telegram_message(name: str, phone: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Telegram не настроен: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID")

    text = f"📩 Новая заявка\n👤 {name}\n📞 {phone}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
                timeout=10.0,
            )
    except httpx.HTTPError as err:
        raise RuntimeError(f"Telegram недоступен: {err}") from err
    data = resp.json()
    if resp.status_code != 200 or not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {resp.status_code}")


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/lead")
async def create_lead(lead: LeadIn):
    try:
        await send_telegram_message(lead.name, lead.phone)
    except RuntimeError as err:
        raise HTTPException(status_code=502, detail="Не удалось отправить заявку") from err
    return {"ok": True}
