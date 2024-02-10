class TestProfile:
    @staticmethod
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

    @staticmethod
    def test_get_profiles(test_app):
        response = test_app.get(
            "/profiles/",
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1

    @staticmethod
    def test_get_profile(test_app):
        response = test_app.get("/profiles/1")
        assert response.status_code == 200
        content = response.json()
        assert content.get("name") == "Test Profile One"
        assert content.get("colors") == "[[0, 0, 255], [255, 0, 0], [255, 255, 255]]"

    @staticmethod
    def test_update_profile(test_app):
        response = test_app.patch(
            "/profiles/1",
            json={
                "name": "PATCHED Test Profile One",
                "colors": "[[255, 0, 255], [255, 0, 0], [255, 255, 255]]",
            },
        )
        assert response.status_code == 200
        assert response.json().get("name") == "PATCHED Test Profile One"
        assert (
            response.json().get("colors")
            == "[[255, 0, 255], [255, 0, 0], [255, 255, 255]]"
        )

    @staticmethod
    def test_delete_profile(test_app):
        response = test_app.delete(
            "/profiles/1",
        )
        assert response.status_code == 200
        assert (
            response.json().get("profile")
            == "Profile: PATCHED Test Profile One deleted"
        )
