from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String)
    jobs = relationship("Job", back_populates="employer", lazy="joined")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs", lazy="joined")
