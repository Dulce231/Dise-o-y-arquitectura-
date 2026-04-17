from database.db_config import DatabaseConnection


class BaseRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def execute(self, query, params=None):
        return self.db.execute_query(query, params)

    def fetch_all(self, query, params=None):
        return self.db.fetch_all(query, params)

    def fetch_one(self, query, params=None):
        rows = self.fetch_all(query, params)
        return rows[0] if rows else None