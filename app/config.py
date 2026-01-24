from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    UPLOAD_DIR: str = "./uploads/files"
    THUMBNAIL_DIR: str = "./uploads/thumbnails"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    class Config:
        env_file = ".env"

settings = Settings()