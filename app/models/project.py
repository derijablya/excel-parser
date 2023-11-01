from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Project(Base):
    code = Column(Integer)
    name = Column(String(100))
    data = relationship('Data')
    version_id = Column(Integer, ForeignKey('version.id'))
