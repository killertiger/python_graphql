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


class Query(ObjectType):
    hello = String(name=String(default_value="graphql"))

    @staticmethod
    def resolve_hello(root, info, name):
        return f"Hello {name}"


schema = Schema(query=Query)

app = FastAPI()

app.mount('/graphql-p', GraphQLApp(schema=schema, on_get=make_playground_handler()))

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
