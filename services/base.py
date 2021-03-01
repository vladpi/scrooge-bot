from db import database


class BaseDBService:
    def __init__(self):
        self.db = database
