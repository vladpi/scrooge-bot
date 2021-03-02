"""Expenses table

Revision ID: 0bdd8a2afcba
Revises: 3ef2024fb715
Create Date: 2021-03-02 21:47:54.917828

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0bdd8a2afcba'
down_revision = '3ef2024fb715'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'expenses',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('amount', sa.Numeric(scale=2), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('on_date', sa.Date(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk__expenses__user_id__users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__expenses')),
    )


def downgrade():
    op.drop_table('expenses')
