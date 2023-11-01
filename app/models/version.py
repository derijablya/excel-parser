import uuid

from sqlalchemy import Column, UUID
from sqlalchemy.orm import relationship

from app.models import Base


class Version(Base):
    version = Column(UUID(as_uuid=True), default=uuid.uuid4)
    project = relationship("Project")
