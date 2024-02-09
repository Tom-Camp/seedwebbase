from datetime import datetime

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from seedweb import schemas
from seedweb.models import Profile, Project, ProjectData, ProjectNotes


def get_profile(db: Session, profile_id: int):
    return db.query(Profile).filter(Profile.id == profile_id).first()


def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Profile).offset(skip).limit(limit).all()


def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = Profile(name=profile.name, colors=profile.colors)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile: schemas.ProfileCreate):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    db_profile.name = profile.name
    db_profile.colors = profile.colors
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: int):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    db.delete(db_profile)
    db.commit()
    return JSONResponse(content={"profile": [f"Profile: {db_profile.name} deleted"]})


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_status(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    current_time = datetime.now().time()
    if project.profile_id:
        profile = db.query(Profile).filter(Profile.id == project.profile_id).first()
        colors = profile.colors
    status = True if current_time >= project.start <= project.end else False
    content = {"status": status, "profile": colors}
    return content


def update_project(db: Session, project_id: int, project: schemas.ProjectCreate):
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


def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db.delete(db_project)
    db.commit()
    return JSONResponse(content={"project": [f"Project: {db_project.name} deleted"]})


def get_project_data(db: Session, project_data_id: int):
    return db.query(ProjectData).filter(ProjectData.id == project_data_id).first()


def get_projects_data(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(ProjectData)
        .filter(ProjectData.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_project_data(
    db: Session, project_data: schemas.ProjectDataCreate, project_id: int
):
    db_project_data = Profile(**project_data.dict(), project_id=project_id)
    db.add(db_project_data)
    db.commit()
    db.refresh(db_project_data)
    return db_project_data


def update_project_data(db: Session, project_data: schemas.ProjectDataCreate):
    db_project_data = (
        db.query(ProjectData).filter(ProjectData.id == project_data.id).first()
    )
    db_project_data.data = project_data.data
    db.commit()
    db.refresh(db_project_data)
    return db_project_data


def delete_project_data(db: Session, project_data_id: int):
    db_project_data = (
        db.query(ProjectData).filter(ProjectData.id == project_data_id).first()
    )
    db.delete(db_project_data)
    db.commit()
    return JSONResponse(content={"data": [f"Project Data: {project_data_id} deleted"]})


def get_project_note(db: Session, project_note_id: int):
    return db.query(ProjectNotes).filter(ProjectNotes.id == project_note_id).first()


def get_projects_notes(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(ProjectNotes)
        .filter(ProjectNotes.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_project_note(
    db: Session, project_note: schemas.ProjectNotesCreate, project_id: int
):
    db_project_notes = Profile(**project_note.dict(), project_id=project_id)
    db.add(db_project_notes)
    db.commit()
    db.refresh(db_project_notes)
    return db_project_notes


def update_project_note(db: Session, project_note: schemas.ProjectNotesCreate):
    db_project_note = (
        db.query(ProjectNotes).filter(ProjectNotes.id == project_note.id).first()
    )
    db_project_note.note = project_note.note
    db.commit()
    db.refresh(db_project_note)
    return db_project_note


def delete_project_note(db: Session, project_note_id: int):
    db_project_note = (
        db.query(ProjectNotes).filter(ProjectNotes.id == project_note_id).first()
    )
    db.delete(db_project_note)
    db.commit()
    return JSONResponse(content={"note": [f"Project Note: {project_note_id} deleted"]})
