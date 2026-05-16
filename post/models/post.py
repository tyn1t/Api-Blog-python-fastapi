from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database.database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    title = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String, unique=True, index=True)
    user = relationship("User", back_populates="posts")
    sections = relationship(
        "PostSection",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="PostSection.order"
    )


class PostSection(Base):
    __tablename__ = "post_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    img_url = Column(String, nullable=False)
    order = Column(Integer, default=0)
    
    post = relationship("Post", back_populates="sections")