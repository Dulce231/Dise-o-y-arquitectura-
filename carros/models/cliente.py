from models.base_repository import BaseRepository


class Cliente(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, nombre, telefono, direccion):
        query = "INSERT INTO clientes (nombre, telefono, direccion) VALUES (%s, %s, %s)"
        cursor = self.db.execute_query(query, (nombre, telefono, direccion))
        return cursor.lastrowid if cursor else None

    def get_all(self):
        return self.db.fetch_all("SELECT * FROM clientes ORDER BY nombre")

    def get_by_id(self, id):
        result = self.db.fetch_all("SELECT * FROM clientes WHERE id = %s", (id,))
        return result[0] if result else None

    def get_by_name(self, nombre):
        return self.db.fetch_all("SELECT * FROM clientes WHERE nombre LIKE %s ORDER BY nombre", (f"%{nombre}%",))

    def update(self, id, nombre, telefono, direccion):
        query = "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s WHERE id=%s"
        return self.db.execute_query(query, (nombre, telefono, direccion, id))

    def delete(self, id):
        query = "DELETE FROM clientes WHERE id=%s"
        return self.db.execute_query(query, (id,))