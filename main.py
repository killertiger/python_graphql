from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)
from app.db.database import prepare_database
from app.db.models import Employer, Job, JobApplication
from app.gql.queries import Query
from app.gql.mutations import Mutation
from app.db.database import Session

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    prepare_database()


@app.get("/employers")
def get_employers():
    with Session() as session:
        return session.query(Employer).all()


@app.get("/jobs")
def get_jobs():
    with Session() as session:
        return session.query(Job).all()


@app.get("/apps")
def get_applications():
    with Session() as session:
        return session.query(JobApplication).count()


app.mount("/graphiql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))

app.mount('/', GraphQLApp(schema=schema, on_get=make_playground_handler()))

