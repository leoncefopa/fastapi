import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, posts, users, votes


# Creates on server-side the models structures defined in models.py
# Not needed with alembic module
# models.Base.metadata.create_all(bind=engine)

# API Instantiation
app = FastAPI()

# Cross Origin Resource Sharing
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routing requests
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
