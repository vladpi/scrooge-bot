import sqlalchemy as sa

from app.db import metadata

transactions = sa.Table(
    'transactions',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('at_date', sa.Date, nullable=False),
    sa.Column('category_id', sa.ForeignKey('categories.id'), nullable=False),
    sa.Column('comment', sa.Text, nullable=True),
    sa.Column('income_account_id', sa.ForeignKey('accounts.id'), nullable=True),
    sa.Column('income_currency', sa.Text, nullable=True),
    sa.Column('income', sa.Numeric(scale=2), nullable=True),
    sa.Column('outcome_account_id', sa.ForeignKey('accounts.id'), nullable=True),
    sa.Column('outcome_currency', sa.Text, nullable=True),
    sa.Column('outcome', sa.Numeric(scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    sa.Column(
        'updated_at',
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    ),
)
