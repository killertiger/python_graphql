from datetime import datetime, timedelta, timezone
from functools import wraps
import os

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
import jwt

from app.db.models import User
from app.db.database import Session
from dotenv import load_dotenv

load_dotenv()

# DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/graphqldb"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION_TIME_MINUTES = int(os.getenv("TOKEN_EXPIRATION_TIME_MINUTES"))


def generate_token(email: str) -> str:
    expiration_time = datetime.utcnow() + timedelta(
        minutes=TOKEN_EXPIRATION_TIME_MINUTES
    )

    payload = {"sub": email, "exp": expiration_time}

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_authenticated_user(context) -> User:
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')

    header_token = [None]
    if auth_header:
        header_token = auth_header.split(" ")

    if auth_header and header_token[0] == "Bearer" and len(header_token) == 2:
        token = header_token[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if datetime.now(timezone.utc) > datetime.fromtimestamp(
                payload['exp'], tz=timezone.utc
            ):
                raise GraphQLError("Token has expired")

            session = Session()
            user = session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate user")
            return user

        except jwt.exceptions.PyJWKError:
            raise GraphQLError("Invalid authentication token")
        except Exception:
            raise GraphQLError("Could not authenticate user")
    else:
        raise GraphQLError("Missing authentication token")


def hash_password(pwd: str) -> str:
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_password(pwd_hash: str, pwd: str) -> None:
    ph = PasswordHasher()

    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)

        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this action")

        return func(*args, **kwargs)

    return wrapper


def authd_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        get_authenticated_user(info.context)

        return func(*args, **kwargs)

    return wrapper


def authd_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        uid = kwargs.get("user_id")

        if user.id != uid:
            raise GraphQLError("You are not authorized to perform this action")

        return func(*args, **kwargs)

    return wrapper
