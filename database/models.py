from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass
class Configurations(Base):
    __tablename__ = 'configurations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    origin_folder: Mapped[str] = mapped_column(String[100], nullable=False)
    destination_folder: Mapped[str] = mapped_column(String[100], nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

class ExistentsFolders(Base):
    __tablename__ = 'existents_folder'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    folder_name: Mapped[str] = mapped_column(String[100], nullable=False)
    folder_location: Mapped[str] = mapped_column(String[100], nullable=False)
    folder_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    folder_files_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

class RemovableTags(Base):
    __tablename__ = 'removable_tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag_name: Mapped[str] = mapped_column(String, nullable=False)
    ignore_tag: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )    
    


