from fastapi import FastAPI
from routers import jwt_tokens, users, customers

tags_metadata = [
    {
        "name": "auth",
        "description": "Create JWT based access tokens that use SHA256 enterprise level security.",
    },
    {
        "name": "users",
        "description": "Create, read, update and manage all users.",
    },
    {
        "name": "customers",
        "description": "Create, read, update and manage all customers.",
    },
]

app = FastAPI(
    title="Smart Energy Meter API",
    description="Python FastAPI based server and backend",
    openapi_tags=tags_metadata,
    redoc_url=None,
)
app.include_router(jwt_tokens.router)
app.include_router(users.router)
app.include_router(customers.router)
