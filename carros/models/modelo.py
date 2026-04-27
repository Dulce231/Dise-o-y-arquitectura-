from models.base_repository import BaseRepository


class Modelo(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, nombre, marca_id):
        query = "INSERT INTO modelos (nombre, marca_id) VALUES (%s, %s)"
        cursor = self.db.execute_query(query, (nombre, marca_id))
        return cursor.lastrowid if cursor else None

    def get_all(self):
        query = """SELECT m.*, ma.nombre as marca_nombre
                   FROM modelos m
                   JOIN marcas ma ON m.marca_id = ma.id
                   ORDER BY ma.nombre, m.nombre"""
        return self.db.fetch_all(query)

    def update(self, id, nombre, marca_id=None):
        if marca_id is not None:
            query = "UPDATE modelos SET nombre=%s, marca_id=%s WHERE id=%s"
            return self.db.execute_query(query, (nombre, marca_id, id))
        query = "UPDATE modelos SET nombre=%s WHERE id=%s"
        return self.db.execute_query(query, (nombre, id))

    def delete(self, id):
        query = "DELETE FROM modelos WHERE id=%s"
        return self.db.execute_query(query, (id,))