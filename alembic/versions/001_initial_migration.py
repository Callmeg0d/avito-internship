"""Initial migration - create tables

Revision ID: 001
Revises: 
Create Date: 2025-11-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'teams',
        sa.Column('team_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('team_name')
    )

    op.create_table(
        'users',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('team_name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['team_name'], ['teams.team_name'], ),
        sa.PrimaryKeyConstraint('user_id')
    )

    op.create_table(
        'pull_requests',
        sa.Column('pull_request_id', sa.String(), nullable=False),
        sa.Column('pull_request_name', sa.String(), nullable=False),
        sa.Column('author_id', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('OPEN', 'MERGED', name='prstatus', create_type=False), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('merged_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('pull_request_id')
    )

    op.create_table(
        'pull_request_reviewers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('pull_request_id', sa.String(), nullable=False),
        sa.Column('reviewer_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['pull_request_id'], ['pull_requests.pull_request_id'], ),
        sa.ForeignKeyConstraint(['reviewer_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('pull_request_reviewers')
    op.drop_table('pull_requests')
    op.drop_table('users')
    op.drop_table('teams')

