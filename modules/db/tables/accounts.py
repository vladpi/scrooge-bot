import sqlalchemy as sa

from ..metadata import metadata

accounts = sa.Table(
    'accounts',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('owner_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('name', sa.Text, nullable=False),
)

accounts_users = sa.Table(
    'accounts_users',
    metadata,
    sa.Column('account_id', sa.ForeignKey('accounts.id'), nullable=False),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
)
