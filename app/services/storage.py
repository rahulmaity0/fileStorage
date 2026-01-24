import os
import uuid
from pathlib import Path
from PIL import Image
from fastapi import UploadFile
from app.config import settings

class StorageService:
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """Generate a unique filename using UUID"""
        ext = Path(original_filename).suffix  # Get extension like .jpg
        unique_name = f"{uuid.uuid4()}{ext}"
        return unique_name
    
    @staticmethod
    async def save_file(file: UploadFile) -> tuple[str, int]:
        """
        Save uploaded file to disk
        Returns: (file_path, file_size)
        """
        # Generate unique filename
        unique_filename = StorageService.generate_unique_filename(file.filename)
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Save file
        file_size = 0
        with open(file_path, "wb") as f:
            content = await file.read()
            file_size = len(content)
            f.write(content)
        
        return file_path, file_size
    
    @staticmethod
    def create_thumbnail(image_path: str, filename: str) -> str | None:
        """
        Create thumbnail for image files
        Returns: thumbnail_path or None
        """
        try:
            # Open image
            img = Image.open(image_path)
            
            # Create thumbnail (200x200 max)
            img.thumbnail((200, 200))
            
            # Generate thumbnail path
            thumbnail_filename = f"thumb_{filename}"
            thumbnail_path = os.path.join(settings.THUMBNAIL_DIR, thumbnail_filename)
            
            # Create directory
            os.makedirs(settings.THUMBNAIL_DIR, exist_ok=True)
            
            # Save thumbnail
            img.save(thumbnail_path)
            
            return thumbnail_path
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    @staticmethod
    def delete_file(file_path: str):
        """Delete file from disk"""
        if os.path.exists(file_path):
            os.remove(file_path)
    
    @staticmethod
    def is_image(content_type: str) -> bool:
        """Check if file is an image"""
        return content_type.startswith("image/")