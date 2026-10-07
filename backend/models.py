from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    issue_type = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(30), default="Open")
    project_id = Column(Integer, ForeignKey("projects.id"))
