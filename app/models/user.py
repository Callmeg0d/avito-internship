from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    team_name = Column(String, ForeignKey("teams.team_name"), nullable=False)

    team = relationship("Team", back_populates="members")
    assigned_reviews = relationship(
        "PullRequestReviewer",
        back_populates="reviewer",
        cascade="all, delete-orphan"
    )

