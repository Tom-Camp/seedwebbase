from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from seedweb import crud, models, schemas
from seedweb.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)


@app.get("/profiles/", response_model=list[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles


@app.get("/profiles/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.patch("/profiles/{profile_id}", response_model=schemas.Profile)
def update_profile(
    profile_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)
):
    db_profile = crud.update_profile(db, profile_id=profile_id, profile=profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.delete_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)


@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.patch("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    db_project = crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.post("/projects/{project_id}/data/", response_model=schemas.ProjectData)
def create_project_data(
    project_id: int,
    project_data: schemas.ProjectDataCreate,
    db: Session = Depends(get_db),
):
    return crud.create_project_data(
        db=db, project_data=project_data, project_id=project_id
    )


@app.get("/projects/{project_id}/data/", response_model=list[schemas.ProjectData])
def read_projects_data(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    db_data = crud.get_projects_data(db, project_id=project_id, skip=skip, limit=limit)
    return db_data


@app.get(
    "/projects/{project_id}/data/{project_data_id}", response_model=schemas.ProjectData
)
def read_project_data(project_data_id: int, db: Session = Depends(get_db)):
    db_data = crud.get_project_data(db, project_data_id=project_data_id)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_data


@app.patch(
    "/projects/{project_id}/data/{project_data_id}", response_model=schemas.ProjectData
)
def update_project_data(
    project_data: schemas.ProjectDataCreate, db: Session = Depends(get_db)
):
    db_data = crud.update_project_data(db, project_data=project_data)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_data


@app.delete("/projects/{project_id}/data/{project_data_id}")
def delete_project_data(project_data_id: int, db: Session = Depends(get_db)):
    db_project_data = crud.delete_project_data(db, project_data_id=project_data_id)
    if db_project_data is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_project_data


@app.post("/projects/{project_id}/notes/", response_model=schemas.ProjectNotes)
def create_project_note(
    project_id: int,
    project_notes: schemas.ProjectNotesCreate,
    db: Session = Depends(get_db),
):
    return crud.create_project_note(
        db=db, project_note=project_notes, project_id=project_id
    )


@app.get("/projects/{project_id}/notes/", response_model=list[schemas.ProjectNotes])
def read_projects_notes(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    db_project_note = crud.get_projects_notes(
        db, project_id=project_id, skip=skip, limit=limit
    )
    return db_project_note


@app.get(
    "/projects/{project_id}/notes/{project_note_id}",
    response_model=schemas.ProjectNotes,
)
def read_project_note(project_note_id: int, db: Session = Depends(get_db)):
    db_project_note = crud.get_project_note(db, project_note_id=project_note_id)
    if db_project_note is None:
        raise HTTPException(status_code=404, detail="Project Note not found")
    return db_project_note


@app.patch(
    "/projects/{project_id}/notes/{project_note_id}", response_model=schemas.ProjectData
)
def update_project_note(
    project_note: schemas.ProjectNotesCreate, db: Session = Depends(get_db)
):
    db_project_note = crud.update_project_note(db, project_note=project_note)
    if db_project_note is None:
        raise HTTPException(status_code=404, detail="Project Data not found")
    return db_project_note


@app.delete("/projects/{project_id}/notes/{project_note_id}")
def delete_project_note(project_note_id: int, db: Session = Depends(get_db)):
    db_project_note = crud.delete_project_note(db, project_note_id=project_note_id)
    if db_project_note is None:
        raise HTTPException(status_code=404, detail="Project Note not found")
    return db_project_note
