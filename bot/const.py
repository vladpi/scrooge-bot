from aiogram.utils.callback_data import CallbackData

CATEGORIES = [
    '🏠 Жилье',
    '🛒 Продукты и быт',
    '🚘 Транспорт',
    '👖 Одежда, обувь, аксессуары',
    '📚 Образование',
    '🎪 Развлечения',
    '🧑‍🍳 Кафе и рестораны',
    '💻 Сервисы и подписки',
    '🎁 Подарки',
    '🧴 Красота и здоровье',
    '🏦 Кредиты',
    '📦 Прочее'
]

history_cb = CallbackData('history', 'date')
reports_cb = CallbackData('reports', 'period')
