from graphene import Field, Int, List, ObjectType, String
from app.db.data import jobs_data, employers_data
from app.db.models import Employer, Job


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root: Employer, info):
        return root.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root: Job, info):
        return root.employer
        # return next(
        #     (
        #         employer
        #         for employer in employers_data
        #         if employer["id"] == root["employer_id"]
        #     ),
        #     None,
        # )
