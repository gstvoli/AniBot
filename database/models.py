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

class Medias(Base):
    __tablename__ = 'medias'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_name: Mapped[str] = mapped_column(String[150], nullable=False)
    media_description: Mapped[Optional[str]] = mapped_column(String[500], nullable=True)
    media_category: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    media_author: Mapped[Optional[str]] = mapped_column(String[100], nullable=True)
    media_magazine: Mapped[Optional[str]] = mapped_column(String[60], nullable=True)
    media_episodes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    media_ovas: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    media_movies: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    media_novels: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    media_seasons: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    media_status: Mapped[Optional[str]] = mapped_column(String[20], nullable=True)
    media_released_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    media_ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    media_nsfw: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
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

    genres: Mapped[List["Genre"]] = relationship(
        secondary="media_genre", back_populates="medias"
    )
    episodes: Mapped[List["MediaEpisodes"]] = relationship(
        back_populates="medias", cascade="all, delete-orphan"
    )
    

class MediaEpisodes(Base):
    __tablename__ = 'media_episodes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("medias.id"), nullable=False)
    episode_title: Mapped[str] = mapped_column(String[80], nullable=False)
    episode_synopsis: Mapped[str] = mapped_column(String[100], nullable=True)
    episode_duration: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )    

    media: Mapped["Medias"] = relationship(back_populates="episodes")

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String[50], unique=True, nullable=False)

class MediaGenre(Base):
    __tablename__ = "media_genre"

    media_id: Mapped[int] = mapped_column(ForeignKey("medias.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)

class MediaHistory(Base):
    __tablename__ = 'media_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    original_name: Mapped[str] = mapped_column(String[255], nullable=False)
    clean_name: Mapped[str] = mapped_column(String[255], nullable=False)
    removed_tags: Mapped[str] = mapped_column(String[150], nullable=False)
    movement_date: Mapped[DateTime] = mapped_column(
        DateTime,  
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
        server_onupdate=func.now(),
    )    