from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)
from app.db.database import prepare_database
from app.db.models import Employer, Job
from app.gql.queries import Query
from app.db.database import Session

schema = Schema(query=Query)

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


app.mount('/graphql-p', GraphQLApp(schema=schema, on_get=make_playground_handler()))

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
