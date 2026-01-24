# from fastapi import FastAPI
# from app.database import engine, Base
# from app.routers import files, auth
# # Import models so SQLAlchemy knows they exist
# from app.models import user, file
# from fastapi.middleware.cors import CORSMiddleware



# # Create database tables
# Base.metadata.create_all(bind=engine)

# # Create FastAPI app
# app = FastAPI(
#     title="File Storage API",
#     description="A secure file storage and processing service with JWT authentication",
#     version="2.0.0"
# )

# # Include routers
# app.include_router(auth.router)
# app.include_router(files.router)

# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to File Storage API",
#         "docs": "/docs",
#         "version": "2.0.0",
#         "features": ["JWT Authentication", "File Upload", "Thumbnail Generation"]
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import files, auth

# We import models here to ensure SQLAlchemy registers them before creating tables
from app.models import user, file

# 1. Initialize Database Tables
# This creates the file_storage.db and the 'users'/'files' tables automatically
Base.metadata.create_all(bind=engine)

# 2. Initialize FastAPI App
app = FastAPI(
    title="VOID // FILE STORAGE",
    description="A secure, monochrome-themed file processing service with JWT authentication",
    version="2.0.0"
)

# 3. Configure CORS (Cross-Origin Resource Sharing)
# This allows your index.html (running on a different port/file) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. In production, use your specific domain.
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows Authorization and Content-Type headers
)

# 4. Include Routers
app.include_router(auth.router)
app.include_router(files.router)

# 5. Root Endpoint
@app.get("/")
async def root():
    return {
        "status": "ONLINE",
        "system": "VOID_FILE_STORAGE",
        "version": "2.0.0",
        "documentation": "/docs",
        "message": "The vault is open."
    }