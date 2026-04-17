from models.base_repository import BaseRepository


class Vehiculo(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, cliente_id, marca_id, modelo_id, año_id, placas, color):
        query = """INSERT INTO vehiculos (cliente_id, marca_id, modelo_id, año_id, placas, color)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor = self.db.execute_query(query, (cliente_id, marca_id, modelo_id, año_id, placas, color))
        return cursor.lastrowid if cursor else None

    def get_all(self):
        query = """SELECT v.*, c.nombre as cliente_nombre, m.nombre as marca_nombre,
                          mo.nombre as modelo_nombre, a.año
                   FROM vehiculos v
                   JOIN clientes c ON v.cliente_id = c.id
                   JOIN marcas m ON v.marca_id = m.id
                   JOIN modelos mo ON v.modelo_id = mo.id
                   JOIN anos a ON v.año_id = a.id
                   ORDER BY c.nombre"""
        return self.db.fetch_all(query)

    def get_by_placas(self, placas):
        query = "SELECT * FROM vehiculos WHERE placas = %s"
        return self.db.fetch_all(query, (placas,))

    def update(self, id, cliente_id, marca_id, modelo_id, año_id, placas, color):
        query = """UPDATE vehiculos SET cliente_id=%s, marca_id=%s, modelo_id=%s,
                   año_id=%s, placas=%s, color=%s WHERE id=%s"""
        return self.db.execute_query(query, (cliente_id, marca_id, modelo_id, año_id, placas, color, id))