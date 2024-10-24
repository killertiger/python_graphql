from graphene import Field, Int, List, ObjectType, String
from app.db.models import Employer, Job, JobApplication, User


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
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(root: Job, info):
        return root.employer
    
    @staticmethod
    def resolve_applications(root: Job, info):
        return root.job_applications


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    applications = List(lambda: JobApplicationObject)

    def resolve_applications(root: User, info):
        return root.job_applications


class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(root: JobApplication, info):
        return root.user

    def resolve_job(root: JobApplication, info):
        return root.job
