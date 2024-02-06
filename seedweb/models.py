from datetime import datetime
from typing import List, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seedweb.database import Base


class Profile(Base):
    __tablename__ = "profile_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    colors: Mapped[Optional[dict | list]] = mapped_column(JSON)

    def __repr__(self):
        return f"Profile: {self.name}"


class Project(Base):
    __tablename__ = "project_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    bed_id: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profile_table.id"))
    profile: Mapped["Profile"] = relationship()
    start: Mapped[datetime] = mapped_column(Time)
    end: Mapped[datetime] = mapped_column(Time)
    data: Mapped[List["ProjectData"]] = relationship(
        back_populates="project", cascade="all, delete"
    )
    notes: Mapped[List["ProjectNotes"]] = relationship(
        back_populates="project", cascade="all, delete"
    )

    def __repr__(self):
        return f"Project: {self.name}"


class ProjectData(Base):
    __tablename__ = "project_data_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    sensor_data: Mapped[str] = mapped_column(String)
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"))
    project: Mapped["Project"] = relationship(back_populates="data")

    def __repr__(self):
        return f"Project Data: {self.id}"


class ProjectNotes(Base):
    __tablename__ = "project_notes_tables"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    note: Mapped[List[str]] = mapped_column(String)
    project_id: Mapped[int] = mapped_column(ForeignKey("project_table.id"))
    project: Mapped["Project"] = relationship(back_populates="notes")

    def __repr__(self):
        return f"Note: {self.id}"
