from app import app


def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'


def test_empty_claim():
    client = app.test_client()
    response = client.post('/verify', data={})
    assert response.status_code == 400


if __name__ == '__main__':
    print('Smoke tests:')
    test_health()
    print('PASS health')
    test_empty_claim()
    print('PASS empty claim')
