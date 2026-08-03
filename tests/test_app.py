from fastapi.testclient import TestClient

from app import _requests_log, app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200


def test_valid_lead_sends_telegram(monkeypatch):
    sent = []

    async def fake_send(name, phone):
        sent.append((name, phone))

    monkeypatch.setattr("app.send_telegram_message", fake_send)

    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
    )
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert sent == [("Иван", "+7 (912) 600-51-61")]


def test_invalid_phone_rejected():
    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "abc"},
    )
    assert response.status_code == 422


def test_missing_fields_rejected():
    response = client.post("/api/lead", json={"name": "Иван"})
    assert response.status_code == 422


def test_telegram_error_returns_502(monkeypatch):
    async def failing_send(name, phone):
        raise RuntimeError("telegram down")

    monkeypatch.setattr("app.send_telegram_message", failing_send)

    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
    )
    assert response.status_code == 502

def test_invalid_name_rejected():
    response = client.post("/api/lead", json={"name": "", "phone": "+7 (912) 600-51-61"})
    assert response.status_code == 422


def test_phone_too_short_rejected():
    response = client.post("/api/lead", json={"name": "Иван", "phone": "+7 (912) 600"})
    assert response.status_code == 422

def test_rate_limit_blocks_after_limit(monkeypatch):
    _requests_log.clear()

    async def fake_send(name, phone):
        pass

    monkeypatch.setattr("app.send_telegram_message", fake_send)

    for _ in range(3):
        response = client.post(
            "/api/lead",
            json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
        )
        assert response.status_code == 200

    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
    )
    assert response.status_code == 429
