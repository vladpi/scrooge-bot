"""Update categories names

Revision ID: 3735ead36f19
Revises: 556bd3adc3f7
Create Date: 2021-04-25 15:03:19.993440

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '3735ead36f19'
down_revision = '556bd3adc3f7'
branch_labels = None
depends_on = None

NEW_CATEGORIES = [
    '🧴 Красота и здоровье',
    '💻 Сервисы и подписки',
]

OLD_CATEGORIES = [
    '💊 Медицина',
    '📱 Мобильная связь',
]


def upgrade():
    for new_category, old_category in zip(NEW_CATEGORIES, OLD_CATEGORIES):
        op.execute(
            f'UPDATE transactions SET category=\'{new_category}\' WHERE category=\'{old_category}\''
        )


def downgrade():
    for new_category, old_category in zip(NEW_CATEGORIES, OLD_CATEGORIES):
        op.execute(
            f'UPDATE transactions SET category=\'{old_category}\' WHERE category=\'{new_category}\''
        )
