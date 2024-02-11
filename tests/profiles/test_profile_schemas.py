import json
from datetime import datetime

import pytest
from pydantic import ValidationError

from seedweb.schemas import Profile


class TestProfileSchema:
    """Testing the Pydantic schema models"""

    @staticmethod
    def test_profile_base():
        """
        Testing the ProfileBase schema
        """
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

    @staticmethod
    def test_profile_raises():
        """Testing validation errors"""
        with pytest.raises(ValidationError):
            _ = Profile(
                id=2,
                name=1,
                colors="[[255, 0, 0], [0, 0, 255]]",
                created_date=datetime.now(),
                updated_date=datetime.now(),
            )

        with pytest.raises(ValidationError):
            _ = Profile(
                id=2,
                name="Raises",
                colors=1,
                created_date=datetime.now(),
                updated_date=datetime.now(),
            )
