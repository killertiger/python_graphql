from graphene import Field, Mutation, String
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject
from app.utils import generate_token, hash_password, verify_password


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


class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if user:
            raise GraphQLError("A user with that email already exists")

        password_hash = hash_password(password)

        user = User(
            username=username, email=email, password_hash=password_hash, role=role
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return AddUser(user=user)
