import sqlalchemy as sa

from app.db import metadata

accounts = sa.Table(
    'accounts',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('owner_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('name', sa.Text, nullable=False),
    sa.Column('balance', sa.Numeric, nullable=False),
    sa.Column('currency', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    sa.Column(
        'updated_at',
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    ),
)

accounts_users = sa.Table(
    'accounts_users',
    metadata,
    sa.Column('account_id', sa.ForeignKey('accounts.id'), nullable=False),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    sa.Column(
        'updated_at',
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    ),
)
