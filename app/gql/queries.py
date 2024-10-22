from graphene import Field, Int, List, ObjectType
from app.db.models import Employer, Job
from app.gql.types import JobObject, EmployerObject
from app.db.database import Session


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))

    @staticmethod
    def resolve_jobs(root, info):
        return Session().query(Job).all()

    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).all()

    @staticmethod
    def resolve_job(root, info, id):
        return Session().query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_employer(root, info, id):
        return Session().query(Employer).filter(Employer.id == id).first()