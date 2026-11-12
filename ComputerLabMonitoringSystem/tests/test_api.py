from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['app'] == 'Computer Lab Monitoring System'


def test_login_endpoint():
    response = client.post('/api/auth/login', json={"username": "admin", "password": "Admin123!"})
    assert response.status_code == 200
    assert 'access_token' in response.json()
