from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
import enum

from app.database import Base


class PRStatus(str, enum.Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"


pr_status_enum = ENUM(PRStatus, name="prstatus", create_type=False)


class PullRequest(Base):
    __tablename__ = "pull_requests"

    pull_request_id = Column(String, primary_key=True)
    pull_request_name = Column(String, nullable=False)
    author_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    status: PRStatus = Column(pr_status_enum, default=PRStatus.OPEN, nullable=False)  # type: ignore[assignment]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    merged_at = Column(DateTime, nullable=True)

    author = relationship("User", foreign_keys=[author_id])
    reviewers = relationship(
        "PullRequestReviewer",
        back_populates="pull_request",
        cascade="all, delete-orphan"
    )


class PullRequestReviewer(Base):
    __tablename__ = "pull_request_reviewers"

    id = Column(String, primary_key=True)
    pull_request_id = Column(String, ForeignKey("pull_requests.pull_request_id"), nullable=False)
    reviewer_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    pull_request = relationship("PullRequest", back_populates="reviewers")
    reviewer = relationship("User", back_populates="assigned_reviews")

