import string
from random import choices
from graphene import Mutation, String
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
ph = PasswordHasher()


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()

        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("A user by that email does not exist")
        
        try:
            ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise GraphQLError("Invalid password")

        token = ''.join(choices(string.ascii_lowercase, k=10))

        return LoginUser(token=token)
