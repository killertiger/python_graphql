from graphene import ObjectType

from app.gql.employer.mutations import AddEmployer
from app.gql.job.mutations import AddJob, UpdateJob, DeleteJob


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
