from graphene import Field, Int, List, Schema, ObjectType, String
from fastapi import FastAPI
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)


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


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data
    
    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)

app = FastAPI()

app.mount('/graphql-p', GraphQLApp(schema=schema, on_get=make_playground_handler()))

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
