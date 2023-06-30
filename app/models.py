from sqlalchemy import Column, Integer, Float, Boolean, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class PostServerData(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    owner = relationship('User')


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    phone_number = Column(String, unique=True, nullable=True)


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False)