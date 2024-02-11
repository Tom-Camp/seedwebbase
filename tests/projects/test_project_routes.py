class TestProject:
    """Project testing class"""

    @staticmethod
    def test_create_project(test_app, valid_project):
        """
        Testing the Project creation endpoint
        :param test_app: fastapi TestClient
        :param valid_project: dict representing a valid Project
        """
        response = test_app.post(
            "/projects",
            json=valid_project,
        )
        assert response.status_code == 200
        content = response.json()
        assert content.get("id") == 1
        assert content.get("name") == "Test Project One"

    @staticmethod
    def test_get_projects(test_app):
        """
        Testing the endpoint that returns a list of Projects
        :param test_app: fastapi TestClient
        """
        response = test_app.get(
            "/projects/",
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1

    @staticmethod
    def test_get_project(test_app):
        """
        Testing the endpoint that returns an individual Project
        :param test_app: fastapi TestClient
        """
        response = test_app.get(
            "/projects/1",
        )
        assert response.status_code == 200
        content = response.json()
        assert content.get("id") == 1
        assert content.get("name") == "Test Project One"

    @staticmethod
    def test_update_project(test_app, valid_project):
        """
        Testing the endpoint for updating a Project
        :param test_app: fastapi TestClient
        :param valid_project: dict representing a valid Project
        """
        valid_project["name"] = "PATCHED Project One"
        response = test_app.patch(
            "/projects/1",
            json=valid_project,
        )
        assert response.status_code == 200
        content = response.json()
        assert content.get("id") == 1
        assert content.get("name") == "PATCHED Project One"

    @staticmethod
    def test_delete_project(test_app):
        """
        Testing the endpoint for deleting a Project
        :param test_app: fastapi TestClient
        """
        response = test_app.delete(
            "/projects/1",
        )
        assert response.status_code == 200
        assert response.json().get("project") == "Project: PATCHED Project One deleted"
