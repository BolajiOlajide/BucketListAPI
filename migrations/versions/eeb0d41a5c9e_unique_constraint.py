"""unique constraint

Revision ID: eeb0d41a5c9e
Revises: 1dba23ad33fa
Create Date: 2017-04-08 07:48:10.725722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeb0d41a5c9e'
down_revision = '1dba23ad33fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_BucketList', 'bucketlist', ['name', 'created_by'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_BucketList', 'bucketlist', type_='unique')
    # ### end Alembic commands ###
