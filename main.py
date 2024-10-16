from graphene import Field, Int, List, ObjectType, Schema, String


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


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


schema = Schema(query=Query)

# gql = '''
# query {
#     user(userId: 1) {
#         id
#         name
#         age
#     }
# }'''

gql = '''
query {
    usersByMinAge(minAge: 30) {
        id
        name
        age
    }
}'''

if __name__ == "__main__":
    result = schema.execute(gql)
    print(result)
