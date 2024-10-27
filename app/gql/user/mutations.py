from graphene import Mutation, String
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
from app.utils import generate_token, verify_password


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

        verify_password(user.password_hash, password)

        # token = ''.join(choices(string.ascii_lowercase, k=10))
        token = generate_token(email)

        return LoginUser(token=token)
