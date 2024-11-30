import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)  
    user_from_id = Column(Integer, ForeignKey('users.id'), nullable=False)  
    user_to_id = Column(Integer, ForeignKey('users.id'), nullable=False)  

    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='followers_from')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followers_to')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  
    username = Column(String(150), unique=True, nullable=False) 
    firstname = Column(String(50), nullable=False)  
    lastname = Column(String(50), nullable=False) 
    email = Column(String(100), unique=True, nullable=False)  

    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True) 
    title = Column(String(100), nullable=False)  
    content = Column(String, nullable=False)  
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 


    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post', cascade='all, delete-orphan')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)  
    comment_text = Column(String, nullable=False)  
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)  

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)  
    type = Column(Enum('image', 'video', 'audio', name='media_types'), nullable=False) 
    url = Column(String, nullable=False)  
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)  

    post = relationship('Post', back_populates='media')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
