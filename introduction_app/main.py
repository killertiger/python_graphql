from graphene import Field, Int, List, ObjectType, Schema, String, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)


class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break

        if not user:
            return None

        if name is not None:
            user["name"] = name

        if age is not None:
            user["age"] = age

        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id):
        user = None
        for idx, u in enumerate(Query.users):
            if u["id"] == user_id:
                user = u
                del Query.users[idx]
                break

        if not user:
            return None
        
        return DeleteUser(user=user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    users = [
        {"id": 1, "name": "Andy Doe", "age": 33},
        {"id": 2, "name": "Andia Doe", "age": 34},
        {"id": 3, "name": "Julie Sullivan", "age": 31},
        {"id": 4, "name": "John Barber", "age": 29},
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


schema = Schema(query=Query, mutation=Mutation)

gql_query_user_1 = '''
query {
    user(userId: 1) {
        id
        name
        age
    }
}'''

# gql = '''
# query {
#     usersByMinAge(minAge: 30) {
#         id
#         name
#         age
#     }
# }'''

# gql = '''
# mutation {
#     createUser(name: "New User", age: 25) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''

# gql_update = '''
# mutation {
#     updateUser(userId: 1, name: "Update User", age: 49) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''

gql_delete = '''
mutation {
    deleteUser(userId: 1) {
        user {
             id
             name
             age
         }
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql_delete)
    print(result)
    result = schema.execute(gql_query_user_1)
    print(result)
