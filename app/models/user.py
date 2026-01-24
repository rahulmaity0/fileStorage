# from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
# from app.database import Base

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, nullable=False, index=True)
#     email = Column(String, unique=True, nullable=False, index=True)
#     hashed_password = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
    
#     def __repr__(self):
#         return f"<User {self.username}>"

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users" # This MUST match the ForeignKey in file.py

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship to files (optional but recommended)
    files = relationship("FileMetadata", backref="owner")