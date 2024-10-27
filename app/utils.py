from datetime import datetime, timedelta, timezone
from functools import wraps

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
import jwt

from app.db.models import User
from app.db.database import Session
from app.settings.config import ALGORITHM, SECRET_KEY, TOKEN_EXPIRATION_TIME_MINUTES


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

    if auth_header:
        token = auth_header.split(" ")[1]

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

        except jwt.exceptions.InvalidSignatureError:
            raise GraphQLError("Invalid authentication token")
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
