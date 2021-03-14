from databases import Database

from config import settings

database = Database(settings.DB_URL)
