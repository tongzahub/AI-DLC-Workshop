from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _create():
    return client.post("/parcels", json={
        "merchant_id": "M-100", "recipient_name": "Test User", "recipient_phone": "0812345678",
        "address": "1 Test Rd", "district": "Bang Rak", "cod_amount": 150.0,
    }).json()


def test_create_and_get_parcel():
    p = _create()
    assert p["status"] == "CREATED"
    got = client.get(f"/parcels/{p['id']}").json()
    assert got["merchant_id"] == "M-100"
    assert got["history"][0]["status"] == "CREATED"


def test_status_update_appends_history():
    p = _create()
    client.put(f"/parcels/{p['id']}/status", json={"status": "OUT_FOR_DELIVERY", "rider_id": "R-001"})
    got = client.get(f"/parcels/{p['id']}").json()
    assert got["status"] == "OUT_FOR_DELIVERY"
    assert len(got["history"]) == 2


def test_unknown_parcel_404():
    assert client.get("/parcels/TEX-2026-999999").status_code == 404
