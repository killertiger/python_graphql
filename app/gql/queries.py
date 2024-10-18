from graphene import List, ObjectType
from app.db.models import Employer, Job
from app.gql.types import JobObject, EmployerObject
from app.db.database import Session
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return Session().query(Job).all()
        # with Session() as session:
        #     return session.query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).all()
