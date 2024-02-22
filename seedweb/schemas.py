import datetime
import json
from typing import Any, List

from pydantic import BaseModel, field_validator


class ProfileBase(BaseModel):
    """ProfileBase model"""

    name: str
    colors: str | None = None


class ProfileCreate(ProfileBase):
    """ProfileCreate passthrough model"""

    @field_validator("colors")
    @classmethod
    def validate_json(cls, v: Any):
        if not json.loads(v):
            raise ValueError("Colors are not valid JSON")
        return v


class Profile(ProfileBase):
    """Profile model"""

    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    @field_validator("created_date")
    def format_created_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    @field_validator("updated_date")
    def format_updated_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    @field_validator("colors")
    def format_colors(cls, v):
        return json.loads(v)

    class ConfigDict:
        """
        Configuration dictionary to determine whether to build models and look up discriminators of tagged
        unions using python object attributes
        """

        from_attributes = True


class ProjectDataBase(BaseModel):
    """ProjectDataBase model"""

    sensor_data: str
    project_id: int


class ProjectDataCreate(ProjectDataBase):
    """ProjectDataCreate passthrough model"""

    @field_validator("sensor_data")
    @classmethod
    def validate_json(cls, v: Any):
        if not json.loads(v):
            raise ValueError("Sensor Data is not valid JSON")
        return v


class ProjectData(ProjectDataBase):
    """ProjectData model"""

    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    @field_validator("created_date")
    def format_created_date(cls, v):
        return v.strftime("%m-%d-%Y %H:%M")

    @field_validator("updated_date")
    def format_updated_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    @field_validator("sensor_data")
    def format_sensor_data(cls, v):
        return json.loads(v)

    class ConfigDict:
        """
        Configuration dictionary to determine whether to build models and look up discriminators of tagged
        unions using python object attributes
        """

        from_attributes = True


class ProjectNotesBase(BaseModel):
    """ProjectNotesBase model"""

    note: str
    project_id: int


class ProjectNotesCreate(ProjectNotesBase):
    """ProjectNotesCreate passthrough model"""

    pass


class ProjectNotes(ProjectNotesBase):
    """ProjectNotes model"""

    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    @field_validator("created_date")
    def format_created_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    @field_validator("updated_date")
    def format_updated_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    class ConfigDict:
        """
        Configuration dictionary to determine whether to build models and look up discriminators of tagged
        unions using python object attributes
        """

        from_attributes = True


class ProjectBase(BaseModel):
    """ProjectBase model"""

    name: str
    bed_id: str
    description: str
    profile_id: int
    start: datetime.time
    end: datetime.time


class ProjectList(ProjectBase):
    """List view for Projects"""

    id: int


class ProjectCreate(ProjectBase):
    """ProjectCreate passthrough model"""

    pass


class ProjectUpdate(ProjectBase):
    """ProjectUpdate passthrough model"""

    pass


class Project(ProjectBase):
    """Project model"""

    data: List[ProjectData] = []
    notes: List[ProjectNotes] = []
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    @field_validator("created_date")
    def format_created_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    @field_validator("updated_date")
    def format_updated_date(cls, v):
        return v.strftime("%b %d %Y %H:%M")

    class ConfigDict:
        """
        Configuration dictionary to determine whether to build models and look up discriminators of tagged
        unions using python object attributes
        """

        from_attributes = True
