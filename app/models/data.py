from sqlalchemy import Column, ForeignKey, Integer, Date, Float

from app.models import Base


class Data(Base):
    date = Column(Date)
    plan = Column(Float, nullable=True)
    factual = Column(Float, nullable=True)
    project_id = Column(Integer, ForeignKey('project.id'))
