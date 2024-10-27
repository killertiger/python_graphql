from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings.config import DB_URL
from app.db.models import Base, Employer, Job, JobApplication, User
from app.db.data import employers_data, jobs_data, users_data, job_applications_data

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)

# conn = engine.connect()


def prepare_database():
    from app.utils import hash_password

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        session.add(Job(**job))

    for user in users_data:
        user["password_hash"] = hash_password(user["password"])
        del user["password"]
        session.add(User(**user))

    for job_application in job_applications_data:
        session.add(JobApplication(**job_application))

    session.commit()
    session.close()
