from graphene import Field, Int, List, Schema, ObjectType, String
from fastapi import FastAPI
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)
from sqlalchemy import Column, Integer, String as saString, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/graphqldb"
engine = create_engine(DB_URL)
conn = engine.connect()

Base = declarative_base()


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(saString)
    contact_email = Column(saString)
    industry = Column(saString)
    jobs = relationship("Job", back_populates="employer")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


employers_data = [
    {
        "id": 1,
        "name": "TechCorp Inc.",
        "contact_email": "contact@techcorp.com",
        "industry": "Technology",
    },
    {
        "id": 2,
        "name": "HealthWorks LLC",
        "contact_email": "info@healthworks.com",
        "industry": "Healthcare",
    },
    {
        "id": 3,
        "name": "EduSmart Solutions",
        "contact_email": "support@edusmart.com",
        "industry": "Education",
    },
    {
        "id": 4,
        "name": "Green Energy Co.",
        "contact_email": "hello@greenenergy.com",
        "industry": "Energy",
    },
    {
        "id": 5,
        "name": "Foodies Hub",
        "contact_email": "careers@foodieshub.com",
        "industry": "Food & Beverage",
    },
]

jobs_data = [
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Responsible for developing and maintaining software solutions.",
        "employer_id": 1,
    },
    {
        "id": 2,
        "title": "Project Manager",
        "description": "Oversees projects from initiation to completion.",
        "employer_id": 1,
    },
    {
        "id": 3,
        "title": "Registered Nurse",
        "description": "Provides healthcare services and patient support.",
        "employer_id": 2,
    },
    {
        "id": 4,
        "title": "Teaching Assistant",
        "description": "Assists lead teachers in classroom activities and supervision.",
        "employer_id": 3,
    },
    {
        "id": 5,
        "title": "Marketing Coordinator",
        "description": "Supports marketing strategy with planning and execution.",
        "employer_id": 4,
    },
]


for employer in employers_data:
    emp = Employer(**employer)
    session.add(emp)


for job in jobs_data:
    session.add(Job(**job))

session.commit()

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next(
            (
                employer
                for employer in employers_data
                if employer["id"] == root["employer_id"]
            ),
            None,
        )


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)

app = FastAPI()

app.mount('/graphql-p', GraphQLApp(schema=schema, on_get=make_playground_handler()))

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
