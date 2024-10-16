from graphene import Schema, ObjectType, String
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp


class Query(ObjectType):
    hello = String(name=String(default_value="graphql"))

    @staticmethod
    def resolve_hello(root, info, name):
        return f"Hello {name}"


schema = Schema(query=Query)

app = FastAPI()

app.mount("/graphql", GraphQLApp(schema=schema))
