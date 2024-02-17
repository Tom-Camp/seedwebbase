from typing import Type

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from seedweb import crud, schemas
from seedweb.database import SessionLocal, engine
from seedweb.models import Base, Profile, Project, ProjectData, ProjectNotes

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> SessionLocal:
    """
    Create a new local database session.
    :return: SQLAlchemy sessionmaker
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Health check endpoint. This endpoint checks the database connection and returns true if
    the database connection is active.
    :param db: SQLAlchemy sessionmaker
    :return: JSONResponse
    """
    status = db.is_active
    return JSONResponse({"database": status})


@app.post("/profiles/", response_model=schemas.Profile)
def create_profile(
    profile: schemas.ProfileCreate, db: Session = Depends(get_db)
) -> Profile:
    """
    Endpoint for creating a Profile
    :param profile: Pydantic schema for the Profile model
    :param db: SQLAlchemy sessionmaker
    :return: json response
    """
    return crud.create_profile(db=db, profile=profile)


@app.get("/profiles/", response_model=list[schemas.Profile])
def get_profiles(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[Profile]] | None:
    """
    Endpoint to return a list of Profiles
    :param skip: int - the number of Profiles to skip
    :param limit: int - the total number of Profiles to return
    :param db: SQLAlchemy sessionmaker
    :return: json response
    """
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles


@app.get("/profiles/{profile_id}", response_model=schemas.Profile)
def get_profile(profile_id: int, db: Session = Depends(get_db)) -> Type[Profile]:
    """
    An endpoint to return a Profile given a Profile ID.
    :param profile_id: int - the Profile ID
    :param db: SQLAlchemy sessionmaker
    :return: json response
    """
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.patch("/profiles/{profile_id}", response_model=schemas.Profile)
def update_profile(
    profile_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)
) -> Type[Profile]:
    """
    An endpoint to update a Profile
    :param profile_id: int - the Profile ID
    :param profile: dict - the Profile object
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_profile = crud.update_profile(db, profile_id=profile_id, profile=profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    An endpoint to delete a given Profile.
    :param profile_id: int - the Profile ID
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_profile = crud.delete_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.post("/projects/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate, db: Session = Depends(get_db)
) -> Project:
    """
    Endpoint for creating a Project
    :param project: Pydantic schema for the Profile model
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    return crud.create_project(db=db, project=project)


@app.get("/projects/", response_model=list[schemas.ProjectList])
def get_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[Project]] | None:
    """
    Endpoint to return a list of Projects
    :param skip: int - the number of Projects to skip
    :param limit: int - the total number of Profiles to return
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)) -> Type[Project]:
    """
    An endpoint to return a Project given a Profile ID.
    :param project_id: int - the Profile ID
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.get("/projects/{project_id}/status")
def get_project_status(project_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    An endpoint to return a Projects status. The status determines if the lights should be on or off
    based on the start and end values.
    :param project_id: int - the Profile ID
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project = crud.get_project_status(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.patch("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)
) -> Type[Project] | None:
    """
    An endpoint to update a Project
    :param project_id: int - the Project ID
    :param project: dict - the Profile object
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project = crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    An endpoint to delete a given Project.
    :param project_id: int - the Profile ID
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.post("/projects/{project_id}/data/", response_model=schemas.ProjectData)
def create_project_data(
    project_data: schemas.ProjectDataCreate,
    db: Session = Depends(get_db),
) -> ProjectData:
    """
    Endpoint for creating Project Data
    :param project_data: Pydantic schema for the ProjectData model
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    return crud.create_project_data(db=db, project_data=project_data)


@app.get("/projects/{project_id}/data/", response_model=list[schemas.ProjectData])
def get_projects_data(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[ProjectData]] | None:
    """
    Endpoint to return a list of Project Data
    :param project_id: int - The Project ID
    :param skip: int - the number of Projects to skip
    :param limit: int - the total number of Profiles to return
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_data = crud.get_projects_data(db, project_id=project_id, skip=skip, limit=limit)
    return db_data


@app.get(
    "/projects/{project_id}/data/{project_data_id}", response_model=schemas.ProjectData
)
def get_project_data(
    project_data_id: int, db: Session = Depends(get_db)
) -> Type[ProjectData]:
    """
    An endpoint to return Project Data given an ID
    :param project_data_id: int - The ID of the Project Data
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_data = crud.get_project_data(db, project_data_id=project_data_id)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_data


@app.patch(
    "/projects/{project_id}/data/{project_data_id}", response_model=schemas.ProjectData
)
def update_project_data(
    project_data_id: int,
    project_data: schemas.ProjectDataCreate,
    db: Session = Depends(get_db),
) -> Type[ProjectData]:
    """
    An endpoint to update Project Data.
    :param project_data_id: Project Data ID
    :param project_data: A JSON data object of the project data.
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_data = crud.update_project_data(
        db, project_data_id=project_data_id, project_data=project_data
    )
    if db_data is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_data


@app.delete("/projects/{project_id}/data/{project_data_id}")
def delete_project_data(
    project_data_id: int, db: Session = Depends(get_db)
) -> JSONResponse:
    """
    An endpoint to delete a Project Data record.
    :param project_data_id: The Project Data ID
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project_data = crud.delete_project_data(db, project_data_id=project_data_id)
    if db_project_data is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_project_data


@app.post("/projects/{project_id}/notes/", response_model=schemas.ProjectNotes)
def create_project_note(
    project_notes: schemas.ProjectNotesCreate,
    db: Session = Depends(get_db),
) -> ProjectNotes:
    """
    Endpoint for creating Project Notes
    :param project_notes: Pydantic schema for the ProjectNotes model
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    return crud.create_project_note(db=db, project_note=project_notes)


@app.get("/projects/{project_id}/notes/", response_model=list[schemas.ProjectNotes])
def get_projects_notes(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[ProjectNotes]] | None:
    """
    Endpoint to return a list of Project Notes
    :param project_id: int - The Project ID
    :param skip: int - the number of Projects to skip
    :param limit: int - the total number of Profiles to return
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project_note = crud.get_projects_notes(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return db_project_note


@app.get(
    "/projects/{project_id}/notes/{project_note_id}",
    response_model=schemas.ProjectNotes,
)
def get_project_note(
    project_note_id: int, db: Session = Depends(get_db)
) -> Type[ProjectNotes]:
    """
    An endpoint to return a Project Note given an ID.
    :param project_note_id: int - The ID of the Project Note
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project_note = crud.get_project_note(db, project_note_id=project_note_id)
    if db_project_note is None:
        raise HTTPException(status_code=404, detail="Project Note not found")
    return db_project_note


@app.patch(
    "/projects/{project_id}/notes/{project_note_id}", response_model=schemas.ProjectData
)
def update_project_note(
    project_note_id: int,
    project_note: schemas.ProjectNotesCreate,
    db: Session = Depends(get_db),
) -> Type[ProjectNotes]:
    """
    An endpoint to update a Project Notes
    :param project_note_id: Project Note ID
    :param project_note: A JSON data object of the project data.
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project_note = crud.update_project_note(
        db, project_note_id=project_note_id, project_note=project_note
    )
    if db_project_note is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_project_note


@app.delete("/projects/{project_id}/notes/{project_note_id}")
def delete_project_note(
    project_note_id: int, db: Session = Depends(get_db)
) -> JSONResponse:
    """
    An endpoint to delete a Project Note record.
    :param project_note_id: The Project Data ID
    :param db: SQLAlchemy sessionmaker
    :return: JSON response
    """
    db_project_note = crud.delete_project_note(db, project_note_id=project_note_id)
    if db_project_note is None:
        raise HTTPException(status_code=404, detail="Project Note not found")
    return db_project_note
