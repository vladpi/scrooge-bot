import sqlalchemy as sa

from app.db import metadata

from .consts import TransactionType

transactions = sa.Table(
    'transactions',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('account_id', sa.ForeignKey('accounts.id'), nullable=False),
    sa.Column('type', sa.Enum(TransactionType), nullable=False),
    sa.Column('amount', sa.Numeric(scale=2), nullable=False),
    sa.Column('comment', sa.Text, nullable=True),
    sa.Column('on_date', sa.Date, nullable=False),
    sa.Column('category', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
)
