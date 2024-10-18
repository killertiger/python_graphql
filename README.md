# first commit
Based on: [Building GraphQL APIs with Python: Beginner To Pro](https://bairesdev.udemy.com/course/building-graphql-apis-with-python/learn/lecture/37422472#overview)

# apps

## introduction_app

# Install

```bash
python3 -m venv venv
pip install -r requirements.txt
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
uvicorn app.main:app --reload
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