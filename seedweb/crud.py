from datetime import datetime
from typing import Type

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from seedweb import schemas
from seedweb.models import Profile, Project, ProjectData, ProjectNotes


def get_profile(db: Session, profile_id: int) -> Type[Profile] | None:
    """
    Given a Profile ID, return a Profile record.
    :param db: SQLAlchemy sessionmaker
    :param profile_id: The ID of the Profile to return
    :return: a Profile object
    """
    return db.query(Profile).filter(Profile.id == profile_id).first()


def get_profiles(
    db: Session, skip: int = 0, limit: int = 100
) -> list[Type[Profile]] | None:
    """
    Return a list of Profiles
    :param skip: int - the number of Profiles to skip
    :param limit: int - the total number of Profiles to return
    :param db: SQLAlchemy sessionmaker
    :return: a list of database Profile objects.
    """
    return db.query(Profile).offset(skip).limit(limit).all()


def create_profile(db: Session, profile: schemas.ProfileCreate) -> Profile:
    """
    Create a Profile and write it to the DB.
    :param db: SQLAlchemy sessionmaker
    :param profile: Pydantic schema for the Profile model
    :return: a Profile object
    """
    db_profile = Profile(name=profile.name, colors=profile.colors)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(
    db: Session, profile_id: int, profile: schemas.ProfileCreate
) -> Type[Profile]:
    """
    Given a Profile ID, update a Profile record.
    :param profile_id: int - the Profile ID
    :param profile: dict - the Profile object
    :param db: SQLAlchemy sessionmaker
    :return: a Profile object
    """
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    db_profile.name = profile.name
    db_profile.colors = profile.colors
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: int) -> JSONResponse:
    """
    Given a Profile ID, return a Profile record.
    :param db: SQLAlchemy sessionmaker
    :param profile_id: The Profile ID
    :return: JSONResponse object with deletion confirmation
    """
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    db.delete(db_profile)
    db.commit()
    return JSONResponse(content={"profile": f"Profile: {db_profile.name} deleted"})


def get_project(db: Session, project_id: int) -> Type[Project] | None:
    """
    Given a Project ID, return a Project record.
    :param db: SQLAlchemy sessionmaker
    :param project_id: The Project ID
    :return: a Project object
    """
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(
    db: Session, skip: int = 0, limit: int = 100
) -> list[Type[Project]] | None:
    """
    Return a list of Project records.
    :param db: SQLAlchemy sessionmaker
    :param skip: The number of Projects to skip
    :param limit: The max number of Projects to return.
    :return: a list of Project objects
    """
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate) -> Project:
    """
    Create a Project object and write them to the database.
    :param db: SQLAlchemy sessionmaker
    :param project: the Project object.
    :return: a Project model object.
    """
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_status(db: Session, project_id: int) -> JSONResponse:
    """
    Calculate whether the lights should be on or off as well as the color pattern to use.
    :param db: SQLAlchemy sessionmaker
    :param project_id: The Project ID
    :return: a JSONResponse object
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    current_time = datetime.now().time()
    if project.profile_id:
        profile = db.query(Profile).filter(Profile.id == project.profile_id).first()
        colors = profile.colors
        status = True if current_time >= project.start <= project.end else False
        content = {"status": status, "profile": colors}
        return JSONResponse(content)
    else:
        return JSONResponse({"error": "Project not found"})


def update_project(
    db: Session, project_id: int, project: schemas.ProjectCreate
) -> Type[Project]:
    """
    Given a Project ID, update a Project record.
    :param db: SQLAlchemy sessionmaker
    :param project_id: the Project ID
    :param project: the Project object.
    :return: a Project model object
    """
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db_project.name = project.name
    db_project.bed_id = project.bed_id
    db_project.description = project.description
    db_project.profile_id = project.profile_id
    db_project.start = project.start
    db_project.end = project.end
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> JSONResponse:
    """
    Given a Project ID, delete a Project record.
    :param db: SQLAlchemy sessionmaker
    :param project_id: the Project ID
    :return: JSONResponse object with deletion confirmation
    """
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db.delete(db_project)
    db.commit()
    return JSONResponse(content={"project": f"Project: {db_project.name} deleted"})


def get_project_data(db: Session, project_data_id: int) -> Type[ProjectData] | None:
    """
    Given a ProjectData ID, return a ProjectData record.
    :param db: SQLAlchemy sessionmaker
    :param project_data_id: the Project Data ID
    :return: a ProjectData model object
    """
    return db.query(ProjectData).filter(ProjectData.id == project_data_id).first()


def get_projects_data(
    db: Session, project_id: int, skip: int = 0, limit: int = 100
) -> list[Type[ProjectData]] | None:
    """
    Given a Project ID, return a list of ProjectData associated with the Project.
    :param db: SQLAlchemy sessionmaker
    :param project_id: the Project ID
    :param skip: the number of Project ID to skip
    :param limit: the max number of ProjectData to return
    :return: a list of ProjectData objects.
    """
    return (
        db.query(ProjectData)
        .filter(ProjectData.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_project_data(
    db: Session, project_data: schemas.ProjectDataCreate, project_id: int
) -> ProjectData:
    """
    Create a ProjectData object and write it to the database.
    :param db: SQLAlchemy sessionmaker
    :param project_data: a ProjectDataCreate object
    :param project_id: The id for the project that the data is associated with.
    :return: a ProjectData object
    """
    db_project_data = ProjectData(**project_data.model_dump(), project_id=project_id)
    db.add(db_project_data)
    db.commit()
    db.refresh(db_project_data)
    return db_project_data


def update_project_data(
    db: Session, project_data_id: int, project_data: schemas.ProjectDataCreate
) -> Type[ProjectData]:
    """
    Update a ProjectData record
    :param db: SQLAlchemy sessionmaker
    :param project_data_id: The ProjectData ID
    :param project_data: a ProjectDataCreate object with which to update the data
    :return: a ProjectData object
    """
    db_project_data = (
        db.query(ProjectData).filter(ProjectData.id == project_data_id).first()
    )
    db_project_data.data = project_data.data
    db.commit()
    db.refresh(db_project_data)
    return db_project_data


def delete_project_data(db: Session, project_data_id: int) -> JSONResponse:
    """
    Delete a ProjectData record
    :param db: SQLAlchemy sessionmaker
    :param project_data_id: The ProjectData ID
    :return: JSONResponse object with deletion confirmation
    """
    db_project_data = (
        db.query(Pr100ojectData).filter(ProjectData.id == project_data_id).first()
    )
    db.delete(db_project_data)
    db.commit()
    return JSONResponse(content={"data": f"Project Data: {project_data_id} deleted"})


def get_project_note(db: Session, project_note_id: int) -> Type[ProjectNotes]:
    """
    Given a ProjectNote ID, return a ProjectNote record.
    :param db: SQLAlchemy sessionmaker
    :param project_note_id: the ProjectNote ID
    :return: return a ProjectNotes record object.
    """
    return db.query(ProjectNotes).filter(ProjectNotes.id == project_note_id).first()


def get_projects_notes(
    db: Session, project_id: int, skip: int = 0, limit: int = 100
) -> list[Type[ProjectNotes]] | None:
    """
    Given a Project ID, return a list of ProjectNotes associated with the Project.
    :param db: SQLAlchemy sessionmaker
    :param project_id: the ProjectNote ID
    :param skip: the number of records to skip
    :param limit: the max number of results to return
    :return: a list of ProjectNote objects
    """
    return (
        db.query(ProjectNotes)
        .filter(ProjectNotes.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_project_note(
    db: Session, project_note: schemas.ProjectNotesCreate, project_id: int
) -> ProjectNotes:
    """
    Create a note to associate with a Project with the given Project ID.
    :param db: SQLAlchemy sessionmaker
    :param project_note: The ProjectNote
    :param project_id: The Project ID
    :return: a ProjectNote object
    """
    db_project_notes = Profile(**project_note.model_dump(), project_id=project_id)
    db.add(db_project_notes)
    db.commit()
    db.refresh(db_project_notes)
    return db_project_notes


def update_project_note(
    db: Session, project_note_id: int, project_note: schemas.ProjectNotesCreate
) -> Type[ProjectNotes] | None:
    """
    Given a ProjectNote ID, update the ProjectNote
    :param db: SQLAlchemy sessionmaker
    :param project_note_id: The ProjectNote ID
    :param project_note: The ProjectNote object
    :return: a ProjectNote object
    """
    db_project_note = (
        db.query(ProjectNotes).filter(ProjectNotes.id == project_note_id).first()
    )
    db_project_note.note = project_note.note
    db.commit()
    db.refresh(db_project_note)
    return db_project_note


def delete_project_note(db: Session, project_note_id: int) -> JSONResponse:
    """
    Given a ProjectNote ID, delete the ProjectNote record
    :param db: SQLAlchemy sessionmaker
    :param project_note_id: a ProjectNote ID
    :return: JSONResponse object
    """
    db_project_note = (
        db.query(ProjectNotes).filter(ProjectNotes.id == project_note_id).first()
    )
    db.delete(db_project_note)
    db.commit()
    return JSONResponse(content={"note": f"Project Note: {project_note_id} deleted"})
