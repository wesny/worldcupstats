"""empty message

Revision ID: 75a2a4a0edb1
Revises: d2f8ce46101c
Create Date: 2017-11-05 15:55:35.779159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75a2a4a0edb1'
down_revision = 'd2f8ce46101c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country_soccer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_name', sa.String(), nullable=True),
    sa.Column('world_cup_wins', sa.Integer(), nullable=True),
    sa.Column('match_wins', sa.Integer(), nullable=True),
    sa.Column('match_ties', sa.Integer(), nullable=True),
    sa.Column('match_losses', sa.Integer(), nullable=True),
    sa.Column('tournament_appearances', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('team')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'team_pkey')
    )
    op.drop_table('country_soccer')
    # ### end Alembic commands ###