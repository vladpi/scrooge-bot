import sqlalchemy as sa

from app.db import metadata

categories = sa.Table(
    'categories',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('name', sa.Text, nullable=False),
    sa.Column('is_income', sa.Boolean, server_default=sa.true(), nullable=False),
    sa.Column('is_outcome', sa.Boolean, server_default=sa.true(), nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    sa.Column(
        'updated_at',
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    ),
)
