import uuid
from datetime import datetime

from scrapy.utils.project import get_project_settings
from sqlalchemy import (
    ARRAY,
    VARCHAR,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

settings = get_project_settings()
Base = declarative_base()
engine = create_engine(settings.get("DATABASE_URL"))


def create_tables():
    Base.metadata.create_all(engine)


class Site(Base):
    __tablename__ = "sites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(VARCHAR(50), nullable=False)
    site = Column(VARCHAR(50), nullable=False)
    url = Column(String, nullable=False)
    recipients = Column(ARRAY(String), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Site ({self.name}, {self.site}, {self.recipients})>"


class Ad(Base):
    __tablename__ = "ads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    site_id = Column(
        UUID(as_uuid=True), ForeignKey(Site.id), nullable=False, index=True
    )
    source_id = Column(VARCHAR(50), nullable=False, index=True)
    url = Column(String, nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    price = Column(ARRAY(String), default=list, nullable=False)
    image = Column(String)

    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Ad ({self.source_id}, {self.title})>"
