import json
from datetime import datetime

from seedweb.schemas import Profile


class TestProfileSchema:
    @staticmethod
    def test_profile_base():
        profile = Profile(
            id=1,
            name="Test Profile",
            colors="[[255, 0, 0], [0, 0, 255]]",
            created_date=datetime.now(),
            updated_date=datetime.now(),
        )
        assert isinstance(profile.id, int)
        assert profile.name == "Test Profile"
        assert profile.colors == "[[255, 0, 0], [0, 0, 255]]"
        assert isinstance(json.loads(profile.colors), list)
        assert isinstance(profile.created_date, datetime)
