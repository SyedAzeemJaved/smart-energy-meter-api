from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
origins = [
    "*",
]

app = FastAPI(
    title="Smart Energy Meter API",
    description="Python FastAPI based server and backend",
    openapi_tags=tags_metadata,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jwt_tokens.router)
app.include_router(users.router)
app.include_router(customers.router)
