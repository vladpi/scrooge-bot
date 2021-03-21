"""Init

Revision ID: 71d77707438c
Revises:
Create Date: 2021-03-20 08:31:05.642981

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '71d77707438c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.Text(), nullable=True),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__users')),
    )
    op.create_table(
        'accounts',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('owner_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['owner_id'], ['users.id'], name=op.f('fk__accounts__owner_id__users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__accounts')),
    )
    op.create_table(
        'accounts_users',
        sa.Column('account_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ['account_id'], ['accounts.id'], name=op.f('fk__accounts_users__account_id__accounts')
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk__accounts_users__user_id__users')
        ),
    )
    op.create_table(
        'transactions',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('account_id', sa.BigInteger(), nullable=False),
        sa.Column('type', sa.Enum('EXPENSE', 'INCOME', name='transactiontype'), nullable=False),
        sa.Column('amount', sa.Numeric(scale=2), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('on_date', sa.Date(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['account_id'], ['accounts.id'], name=op.f('fk__transactions__account_id__accounts')
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk__transactions__user_id__users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__transactions')),
    )


def downgrade():
    op.drop_table('transactions')
    op.drop_table('accounts_users')
    op.drop_table('accounts')
    op.drop_table('users')
