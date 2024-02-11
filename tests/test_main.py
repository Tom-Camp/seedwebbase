def test_main(test_app):
    """
    Test for the health check endpoint
    :param test_app: fastapi TestClient
    """
    response = test_app.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"database": True}
