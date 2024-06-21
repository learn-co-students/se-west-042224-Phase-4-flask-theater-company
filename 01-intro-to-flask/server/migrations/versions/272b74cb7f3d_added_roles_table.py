"""added roles table

Revision ID: 272b74cb7f3d
Revises: 16c9b9df8d01
Create Date: 2024-06-21 14:46:03.513516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '272b74cb7f3d'
down_revision = '16c9b9df8d01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['productions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    # ### end Alembic commands ###
