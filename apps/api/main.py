from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import insights, retrieve, mentor, generate, auth, chat # Added chat

app = FastAPI()

# Configure CORS
origins = [

    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(insights.router, prefix="/insights", tags=["insights"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])
app.include_router(retrieve.router, prefix="/retrieve", tags=["retrieve"])
app.include_router(mentor.router, prefix="/mentor", tags=["mentor"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"]) # Added chat router

@app.get("/")
def read_root():
    return {"message": "Artisan Mentor API"}
