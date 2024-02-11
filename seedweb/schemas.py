import datetime

from pydantic import BaseModel


class ProfileBase(BaseModel):
    """ProfileBase model"""

    name: str
    colors: str | None = None


class ProfileCreate(ProfileBase):
    """ProfileCreate passthrough model"""

    pass


class Profile(ProfileBase):
    """Profile model"""

    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

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

    pass


class ProjectData(ProjectDataBase):
    """ProjectData model"""

    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

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


class ProjectCreate(ProjectBase):
    """ProjectCreate passthrough model"""

    pass


class Project(ProjectBase):
    """Project model"""

    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class ConfigDict:
        """
        Configuration dictionary to determine whether to build models and look up discriminators of tagged
        unions using python object attributes
        """

        from_attributes = True
