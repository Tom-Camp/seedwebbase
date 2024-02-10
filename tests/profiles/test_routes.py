def test_create_profile(test_app):
    response = test_app.post(
        "/profiles",
        json={
            "name": "Test Profile One",
            "colors": "[[0, 0, 255], [255, 0, 0], [255, 255, 255]]",
        },
    )
    assert response.status_code == 200
    content = response.json()
    assert content.get("id") == 1
    assert content.get("name") == "Test Profile One"
