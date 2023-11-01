"""create initial tables

Revision ID: e63ffcd534aa
Revises: 
Create Date: 2023-11-01 06:30:12.952247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e63ffcd534aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('version',
    sa.Column('version', sa.UUID(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_version_id'), 'version', ['id'], unique=False)
    op.create_table('project',
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('version_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['version_id'], ['version.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)
    op.create_table('data',
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('plan', sa.Float(), nullable=True),
    sa.Column('factual', sa.Float(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_id'), 'data', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_data_id'), table_name='data')
    op.drop_table('data')
    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')
    op.drop_index(op.f('ix_version_id'), table_name='version')
    op.drop_table('version')
    # ### end Alembic commands ###
