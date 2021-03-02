import sqlalchemy as sa

from ..metadata import metadata

expenses = sa.Table(
    'expenses',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('amount', sa.Numeric(scale=2), nullable=False),
    sa.Column('comment', sa.Text, nullable=True),
    sa.Column('on_date', sa.Date, nullable=False),
    sa.Column('category', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
)
