"""Update categories names

Revision ID: 556bd3adc3f7
Revises: 71d77707438c
Create Date: 2021-04-05 18:04:41.074778

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '556bd3adc3f7'
down_revision = '71d77707438c'
branch_labels = None
depends_on = None


NEW_CATEGORIES = [
    '🏠 Жилье',
    '🛒 Продукты и быт',
    '🚘 Транспорт',
    '👖 Одежда, обувь, аксессуары',
    '📚 Образование',
    '🎪 Развлечения',
    '🧑‍🍳 Кафе и рестораны',
    '📱 Мобильная связь',
    '🎁 Подарки',
    '💊 Медицина',
    '🏦 Кредиты',
]

OLD_CATEGORIES = [
    'Жилье',
    'Продукты и быт',
    'Транспорт',
    'Одежда, обувь, аксессуары',
    'Образование',
    'Развлечения',
    'Кафе и рестораны',
    'Мобильная связь',
    'Подарки',
    'Медицина',
    'Кредиты',
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
