from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FolderConfig(Base):
    __tablename__ = 'folder_config'

    id_config = Column(Integer, primary_key=True, autoincrement=True)
    origin_folder = Column(String, nullable=False, default="")
    destination_folder = Column(String, nullable=False, default="")
    active = Column(Integer, default=1)