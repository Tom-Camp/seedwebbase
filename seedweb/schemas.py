import datetime

from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str
    colors: str | None = None


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        from_attributes = True


class ProjectDataBase(BaseModel):
    sensor_data: str
    project_id: int


class ProjectDataCreate(ProjectDataBase):
    pass


class ProjectData(ProjectDataBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime


class ProjectNotesBase(BaseModel):
    note: str
    project_id: int


class ProjectNotesCreate(ProjectNotesBase):
    pass


class ProjectNotes(ProjectNotesBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    bed_id: str
    description: str
    profile_id: int
    start: datetime.time
    end: datetime.time


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        from_attributes = True
