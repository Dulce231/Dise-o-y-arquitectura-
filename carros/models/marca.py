from models.base_repository import BaseRepository


class Marca(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, nombre):
        query = "INSERT INTO marcas (nombre) VALUES (%s)"
        return self.db.execute_query(query, (nombre,))

    def get_all(self):
        return self.db.fetch_all("SELECT * FROM marcas ORDER BY nombre")

    def update(self, id, nombre):
        query = "UPDATE marcas SET nombre=%s WHERE id=%s"
        return self.db.execute_query(query, (nombre, id))

    def delete(self, id):
        query = "DELETE FROM marcas WHERE id=%s"
        return self.db.execute_query(query, (id,))