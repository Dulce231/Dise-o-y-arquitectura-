import datetime

from models.base_repository import BaseRepository


class Servicio(BaseRepository):
    def __init__(self):
        super().__init__()

    def generate_folio(self):
        return f"SERV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    def create(self, vehiculo_id, cliente_id, quien_llevo, fecha_proximo_servicio, observaciones=""):
        folio = self.generate_folio()
        fecha_registro = datetime.date.today().isoformat()
        query = """INSERT INTO servicios (folio, vehiculo_id, cliente_id, fecha_registro,
                   fecha_proximo_servicio, estatus, quien_llevo, observaciones)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = self.db.execute_query(
            query,
            (folio, vehiculo_id, cliente_id, fecha_registro, fecha_proximo_servicio, "En espera", quien_llevo, observaciones),
        )
        return folio if cursor else None

    def get_all(self):
        query = """SELECT s.*, c.nombre as cliente_nombre, v.placas
                   FROM servicios s
                   JOIN clientes c ON s.cliente_id = c.id
                   JOIN vehiculos v ON s.vehiculo_id = v.id
                   ORDER BY s.fecha_registro DESC, s.folio DESC"""
        return self.db.fetch_all(query)

    def get_by_folio(self, folio):
        query = """SELECT s.*, c.nombre as cliente_nombre, c.telefono, c.direccion,
                          v.placas, v.color, m.nombre as marca_nombre, mo.nombre as modelo_nombre, a.año
                   FROM servicios s
                   JOIN clientes c ON s.cliente_id = c.id
                   JOIN vehiculos v ON s.vehiculo_id = v.id
                   JOIN marcas m ON v.marca_id = m.id
                   JOIN modelos mo ON v.modelo_id = mo.id
                   JOIN anos a ON v.año_id = a.id
                   WHERE s.folio = %s"""
        result = self.db.fetch_all(query, (folio,))
        return result[0] if result else None

    def get_by_cliente_nombre(self, nombre):
        query = """SELECT s.*, c.nombre as cliente_nombre, v.placas
                   FROM servicios s
                   JOIN clientes c ON s.cliente_id = c.id
                   JOIN vehiculos v ON s.vehiculo_id = v.id
                   WHERE c.nombre LIKE %s
                   ORDER BY s.fecha_registro DESC"""
        return self.db.fetch_all(query, (f"%{nombre}%",))

    def update_status(self, folio, estatus):
        query = "UPDATE servicios SET estatus=%s WHERE folio=%s"
        return self.db.execute_query(query, (estatus, folio))

    def update(self, folio, vehiculo_id, cliente_id, fecha_proximo_servicio, quien_llevo, observaciones):
        query = """UPDATE servicios
                   SET vehiculo_id=%s, cliente_id=%s, fecha_proximo_servicio=%s,
                       quien_llevo=%s, observaciones=%s
                   WHERE folio=%s"""
        return self.db.execute_query(query, (vehiculo_id, cliente_id, fecha_proximo_servicio, quien_llevo, observaciones, folio))

    def delete(self, folio):
        query = "DELETE FROM servicios WHERE folio=%s"
        return self.db.execute_query(query, (folio,))

    def get_estadisticas(self):
        query = """SELECT estatus, COUNT(*) as cantidad
                   FROM servicios
                   GROUP BY estatus"""
        return self.db.fetch_all(query)