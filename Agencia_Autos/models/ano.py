from models.base_repository import BaseRepository


class Ano(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, año):
        query = "INSERT INTO anos (año) VALUES (%s)"
        cursor = self.db.execute_query(query, (año,))
        return cursor.lastrowid if cursor else None

    def get_all(self):
        return self.db.fetch_all("SELECT * FROM anos ORDER BY año DESC")

    def update(self, id, año):
        query = "UPDATE anos SET año=%s WHERE id=%s"
        return self.db.execute_query(query, (año, id))

    def delete(self, id):
        query = "DELETE FROM anos WHERE id=%s"
        return self.db.execute_query(query, (id,))