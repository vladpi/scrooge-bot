import sqlalchemy as sa

from app.db import metadata

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('username', sa.Text, nullable=True),
    sa.Column('first_name', sa.Text, nullable=True),
    sa.Column('last_name', sa.Text, nullable=True),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
)
