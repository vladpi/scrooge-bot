"""Transactions table

Revision ID: cb567e4e0856
Revises: 3ef2024fb715
Create Date: 2021-03-03 18:39:37.432190

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cb567e4e0856'
down_revision = '3ef2024fb715'
branch_labels = None
depends_on = None

transaction_type = sa.Enum('EXPENSE', 'INCOME', name='transaction_type')


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('type', transaction_type, nullable=False),
        sa.Column('amount', sa.Numeric(scale=2), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('on_date', sa.Date(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk__transactions__user_id__users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__transactions')),
    )


def downgrade():
    op.drop_table('transactions')
    transaction_type.drop(op.get_bind())
