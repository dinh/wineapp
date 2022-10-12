from starlette.testclient import TestClient

from app.main import app
from app.project import info


def test_app_info():
    client = TestClient(app)
    response = client.get("/api/info")
    assert response.status_code == 200
    assert response.url == "http://testserver/api/info"
    assert response.json() == {
        "name": info['name'],
        "version": info['version'],
        "description": "Wine review API"
    }


def test_healthcheck():
    client = TestClient(app)
    response = client.get("/api/healthcheck")
    assert response.status_code == 200
    assert response.url == "http://testserver/api/healthcheck"
    assert response.json() == {"detail": "OK"}
