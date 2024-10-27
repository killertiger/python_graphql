# first commit
Based on: [Building GraphQL APIs with Python: Beginner To Pro](https://bairesdev.udemy.com/course/building-graphql-apis-with-python/learn/lecture/37422472#overview)

# apps

## introduction_app

# Install

```bash
python3 -m venv venv
pip install -r requirements.txt
```

Create .env file:
```
DB_URL="postgresql://postgres:postgres@localhost:5432/graphqldb"
SECRET_KEY="job_board_app_secret!"
ALGORITHM="HS256"
TOKEN_EXPIRATION_TIME_MINUTES=25
```

# Running

```bash
source venv/bin/activate
```

```bash
python main.py
```

# app

# Running
```bash
uvicorn main:app --reload
```


Query example:
```
{ 
  jobs {
    id
    employerId
    description
    employer {
      id
      industry
    }
  }

  employers {
    industry
    contactEmail
    jobs {
      id
      description
    }
  }
}
```

Mutation example:
```
mutation {
  addJob(title: "Some futuristic role", description: "working with code", employerId: 1) {
    job {
      id
    }
  }
}
```

# Example queries:

Query using Fragment
```
query {
  employer(id: 2) {
    ...employerFields
  }
}

fragment employerFields on EmployerObject {
  id name contactEmail industry jobs {
    ...jobFields
  }
}

fragment jobFields on JobObject { 
	id title description employerId
}
```

Update employer:
```
mutation {
  updateEmployer(employerId: 1, name: "new name", contactEmail: "newemail@domain.code", industry: "Any industry") {
    employer {
      id
      name
      contactEmail
      industry
    }
  }
}
```

Delete employer:
```
mutation {
  deleteEmployer(id: 1) {
    success
  }
}
```

Query Users:
```
query {
  users {
    id
    username
    email
    role
  }
}
```

Query JobApplications:
```
query
 {
  jobApplications {
    id
    jobId
    userId
    user {
      id
      username
    }
    job {
      id
      title
    }
  }
}
```

Mutation LoginUser:
```
mutation {
  loginUser(email: "john.doe@example.com", password: "hashed_password_1"){
    token
  }
}
```

Mutation AddUser:
```
mutation {
  addUser(
    username: "new_user",
    email: "test@example.com",
    password: "new_pass",
    role: "role") {
    user {
      id
      username
      email
      role
    }
  }
}
```

Mutation ApplyToJob:
```
mutation {
  applyToJob(
    jobId: 1,
    userId: 3
  ) {
    jobApplication {
      id
      userId
      jobId
    }
  }
}
```