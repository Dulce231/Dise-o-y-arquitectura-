from models.base_repository import BaseRepository


class Fallo(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, nombre, costo, descripcion=""):
        query = "INSERT INTO fallos (nombre, costo, descripcion) VALUES (%s, %s, %s)"
        cursor = self.db.execute_query(query, (nombre, costo, descripcion))
        return cursor.lastrowid if cursor else None

    def get_all(self):
        return self.db.fetch_all("SELECT * FROM fallos ORDER BY nombre")

    def get_by_id(self, id):
        result = self.db.fetch_all("SELECT * FROM fallos WHERE id=%s", (id,))
        return result[0] if result else None

    def update(self, id, nombre, costo, descripcion=""):
        query = "UPDATE fallos SET nombre=%s, costo=%s, descripcion=%s WHERE id=%s"
        return self.db.execute_query(query, (nombre, costo, descripcion, id))

    def delete(self, id):
        query = "DELETE FROM fallos WHERE id=%s"
        return self.db.execute_query(query, (id,))