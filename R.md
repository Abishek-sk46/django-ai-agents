# 🧠 Multi‑Agent Django Backend (Recall & Debug Guide)

> **Purpose of this document**
> This README is written for **future‑me** (and for explaining to others).
> I built this project ~6 months ago. Later, I faced confusion around **permissions, agents, tools, Jupyter testing, and Permit.io**.
> This document explains the **full flow step‑by‑step**, with **mental models + exact Jupyter code**, so I can recall everything quickly.

---

## 1️⃣ What this project is (in simple words)

* Backend‑only project (no frontend)
* Built with **Django**
* Uses **LangChain + LangGraph** for a **multi‑agent AI system**
* Uses **Permit.io** for authorization (permissions)
* Tested entirely using **Jupyter Notebook**

### What problem it demonstrates

> How to safely let an AI system perform **real database actions** using tools, while enforcing **strict permissions**.

---

## 2️⃣ High‑level architecture (mental picture)

```
User → Agent → Tool → Permit.io → Django ORM → Database
                ↑
           Allow / Deny
```

### Responsibilities

* **Django** → stores users & documents (data)
* **Agent (LLM)** → understands intent (create, list, update, delete)
* **Tools** → real Python functions that do DB work
* **Permit.io** → decides whether action is allowed
* **Jupyter** → testing environment

---

## 3️⃣ User creation – where users actually come from

### 🔹 Important truth

❌ Users are **NOT** created by agents
❌ Users are **NOT** created by Permit.io

✅ Users are created **manually in Django**

### How users are created

#### Option A: Django Admin

```bash
python manage.py createsuperuser
```

#### Option B: Django shell / Jupyter

```python
from django.contrib.auth import get_user_model
User = get_user_model()

User.objects.create_user(
    username="abishek",
    password="test123"
)
```

Result:

* Django DB now has a user
* User has an integer ID (e.g. `id = 1`)

---

## 4️⃣ Syncing Django users to Permit.io

Permit does **not** know Django users automatically.
We must **sync** them.

### Jupyter code (used once)

```python
from mypermit import permit_client as permit
from django.contrib.auth import get_user_model

User = get_user_model()

for u in User.objects.all():
    await permit.api.users.sync({
        "key": str(u.id),        # IMPORTANT: string
        "first_name": u.username
    })
```

### Mental model

* Django user: `id = 1`
* Permit user: `key = "1"`

They are linked only by **value**, not database relation.

---

## 5️⃣ Resources – what is being protected

### Resources defined in Permit

```text
document
movie_discovery
```

### Actions on document

```text
read
create
update
delete
```

This only defines **what actions exist**, not who can do them.

---

## 6️⃣ Roles – permission bundles

### Viewer role

```text
- document:read
```

### Manager role

```text
- document:read
- document:create
- document:update
- document:delete
```

Roles are just **permission sets**.
They do nothing until assigned to a user.

---

## 7️⃣ Assigning roles to users (MOST IMPORTANT STEP)

This is where permissions actually change.

### Jupyter code

```python
await permit.api.users.assign_role({
    "user": "1",          # Permit user key
    "role": "manager",   # or "viewer"
    "tenant": "default"
})
```

### Meaning

* `viewer` → can only list documents
* `manager` → can create / update / delete

If create fails → check role first.

---

## 8️⃣ How permission is enforced in code (tools)

Permissions are **NOT** checked in:

* Django admin
* Django models
* Agent prompts

They are checked **inside tools**.

### Example tool (simplified)

```python
@tool
async def create_document(title: str, content: str, config):
    user_id = config["configurable"]["user_id"]

    allowed = await permit.check(
        str(user_id),
        "create",
        "document"
    )

    if not allowed:
        raise Exception("Permission denied")

    Document.objects.create(
        title=title,
        content=content,
        owner_id=int(user_id)
    )
```

### Key rule

> **Agents decide WHAT to do**
> **Tools decide IF it is allowed**

---

## 9️⃣ Testing flow using Jupyter (step‑by‑step)

### Step 1: Start Django

```bash
python manage.py runserver
```

⚠️ Forgetting this caused many earlier issues.

---

### Step 2: Create agent

```python
from ai.agents import get_agent
from langgraph.checkpoint.memory import InMemorySaver
import uuid

checkpointer = InMemorySaver()

config = {
    "configurable": {
        "user_id": "1",
        "thread_id": str(uuid.uuid4())
    }
}

agent = get_agent(None, checkpointer=checkpointer)
```

---

### Step 3: CREATE document

```python
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Create a document with title 'New Doc' and content 'Created now'"
            }
        ]
    },
    config
)

response["messages"][-1].content
```

---

### Step 4: LIST documents

```python
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "list the documents"}
        ]
    },
    config
)

response["messages"][-1].content
```

---

### Step 5: UPDATE document

```python
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Update document 1 and change the title to 'New Doc Updated'"}
        ]
    },
    config
)

response["messages"][-1].content
```

---

### Step 6: VERIFY update

```python
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Show document 1"}
        ]
    },
    config
)

response["messages"][-1].content
```

---

## 🔟 Why UPDATE didn’t appear in list earlier

Because list was ordered by:

```python
.order_by("-created_at")
```

Updating changes `updated_at`, not `created_at`.

This is expected behavior, not a bug.

---

## 1️⃣1️⃣ Debugging permissions (quick checklist)

If an action fails:

1. Is Django running?
2. Does Django user exist?
3. Is user synced to Permit?
4. Does user have `manager` role?
5. Is correct `user_id` passed in config?

### View users + roles

```python
result = await permit.api.users.list()

for u in result.data:
    print(f"User {u.key} roles:", [r.role for r in u.roles])
```

---

## 1️⃣2️⃣ One‑page memory summary

* Django creates users
* Permit assigns roles
* Roles decide permissions
* Tools enforce security
* Agents never bypass rules

> **Problem before:** permissions + environment confusion
> **Reality:** system worked correctly

---

---

## 1️⃣3️⃣ Movie Discovery Agent Testing (step‑by‑step)

Similar to document agent, but for movie search and details.

### Step 1: Start Django (same as before)

```bash
python manage.py runserver
```

⚠️ **Critical**: Django must be running for TMDB tools to work.

---

### Step 2: Create movie discovery agent

```python
from ai.agents import get_movie_discovery_agent
from langgraph.checkpoint.memory import InMemorySaver
import uuid

checkpointer = InMemorySaver()

config = {
    "configurable": {
        "user_id": "2",        # Different user for testing
        "thread_id": str(uuid.uuid4())
    }
}

agent = get_movie_discovery_agent(model="gemini-1.5-flash", checkpointer=checkpointer)
```

---

### Step 3: SEARCH movies

```python
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Tell me about the first Lord of the Rings movie"
            }
        ]
    },
    config
)

response["messages"][-1].content
```

---

### Step 4: DETAILED movie search

```python
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Find action movies from 2023 with high ratings"}
        ]
    },
    config
)

response["messages"][-1].content
```

---

### Step 5: GET movie details

```python
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Give me detailed information about movie ID 120"}
        ]
    },
    config
)

response["messages"][-1].content
```

---

### Step 6: VERIFY tools work directly

```python
# Test tools directly (debugging)
from ai.tools.movie_discovery import search_movies, movies_detail

# Test search
search_result = search_movies.invoke({"query": "Lord of the Rings"})
print(f"Search found: {len(search_result)} movies")

# Test detail (using ID from search)
if search_result:
    movie_id = search_result[0]['id']
    detail_result = movies_detail.invoke({"movie_id": movie_id})
    print(f"Detail: {detail_result['title']}")
```

---

## 1️⃣4️⃣ Movie vs Document agent differences

### Mental model

**Document Agent:**
```
User → Agent → Document Tools → Permit.io → Django DB → Documents
```

**Movie Agent:**
```
User → Agent → Movie Tools → TMDB API → External Data
```

### Key differences

* **Document**: Stores in Django database
* **Movie**: Fetches from external TMDB API
* **Document**: Requires Permit.io permissions
* **Movie**: Uses TMDB API key (simpler auth)

---

## 1️⃣5️⃣ Debugging movie agent (quick checklist)

If movie search fails:

1. Is Django running?
2. Is TMDB API key valid?
3. Is internet connection working?
4. Are movie tools imported correctly?
5. Is correct agent created?

### Test TMDB API directly

```python
from tmdb import client as tmdb_client

# Direct API test
result = tmdb_client.search_movie("Test Movie")
print(result)  # Should return JSON, not error
```

### View available tools

```python
from ai.tools.movie_discovery import movie_discovery_tools
print([tool.name for tool in movie_discovery_tools])
# Should show: ['search_movies', 'movies_detail']
```

---

## 1️⃣6️⃣ One‑page memory summary (updated)

### Document System
* Django creates users
* Permit assigns roles
* Tools enforce security
* Agents never bypass rules

### Movie System
* TMDB provides data
* API key enables access
* Tools fetch external data
* No permission checks (yet)

> **Pattern**: Both agents follow same structure, but different data sources

---

## ✅ Final note (for future me)

If you feel stuck again:

**For Documents:**
* Don't panic
* Check role first
* Check Django running
* Check `user_id`

**For Movies:**
* Check Django running
* Check TMDB API key
* Check internet connection
* Check tool imports

Both systems are **correctly designed** but serve different purposes.
