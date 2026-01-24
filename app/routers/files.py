from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.file import FileMetadata
from app.models.user import User
from app.services.storage import StorageService
from app.config import settings
from app.auth import get_current_user
import os

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file (requires authentication)"""
    
    # Check file size
    content = await file.read()
    file_size = len(content)
    await file.seek(0)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Save file
    file_path, file_size = await StorageService.save_file(file)
    unique_filename = file_path.split("\\")[-1]
    
    # Create thumbnail for images
    thumbnail_path = None
    if StorageService.is_image(file.content_type):
        thumbnail_path = StorageService.create_thumbnail(file_path, unique_filename)
    
    # Save metadata to database (linked to current user)
    file_metadata = FileMetadata(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        thumbnail_path=thumbnail_path,
        file_size=file_size,
        content_type=file.content_type,
        user_id=current_user.id  # Link to user
    )
    
    db.add(file_metadata)
    db.commit()
    db.refresh(file_metadata)
    
    return {
        "id": file_metadata.id,
        "filename": file_metadata.filename,
        "original_filename": file_metadata.original_filename,
        "file_size": file_metadata.file_size,
        "content_type": file_metadata.content_type,
        "uploaded_at": file_metadata.uploaded_at,
        "has_thumbnail": thumbnail_path is not None
    }

@router.get("/")
async def list_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all files uploaded by current user"""
    files = db.query(FileMetadata).filter(FileMetadata.user_id == current_user.id).all()
    return files

@router.get("/{file_id}")
async def get_file_info(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file information (only your own files)"""
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.user_id == current_user.id
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    return file_metadata

@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a file (only your own files)"""
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.user_id == current_user.id
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(file_metadata.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=file_metadata.file_path,
        filename=file_metadata.original_filename,
        media_type=file_metadata.content_type
    )

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file (only your own files)"""
    file_metadata = db.query(FileMetadata).filter(
        FileMetadata.id == file_id,
        FileMetadata.user_id == current_user.id
    ).first()
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from disk
    StorageService.delete_file(file_metadata.file_path)
    if file_metadata.thumbnail_path:
        StorageService.delete_file(file_metadata.thumbnail_path)
    
    # Delete from database
    db.delete(file_metadata)
    db.commit()
    
    return {"message": "File deleted successfully"}