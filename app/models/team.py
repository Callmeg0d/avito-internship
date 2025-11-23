from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    team_name = Column(String, primary_key=True)
    members = relationship("User", back_populates="team", cascade="all, delete-orphan")

