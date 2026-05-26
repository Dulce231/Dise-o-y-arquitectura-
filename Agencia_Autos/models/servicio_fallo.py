from collections import Counter

from models.base_repository import BaseRepository
from models.fallo import Fallo


class ServicioFallo(BaseRepository):
    def __init__(self):
        super().__init__()
        self.fallo_model = Fallo()

    def replace_for_service(self, folio, fallo_ids):
        for fallo_id in set(fallo_ids or []):
            fallo = self.fallo_model.get_by_id(fallo_id)
            if not fallo:
                raise ValueError("El fallo seleccionado no existe.")

        self.clear_for_service(folio)

        for fallo_id, cantidad in Counter(fallo_ids or []).items():
            self.execute(
                "INSERT INTO servicio_fallos (servicio_folio, fallo_id, cantidad) VALUES (%s, %s, %s)",
                (folio, fallo_id, cantidad),
            )

    def clear_for_service(self, folio):
        self.execute("DELETE FROM servicio_fallos WHERE servicio_folio=%s", (folio,))

    def get_by_service(self, folio):
        query = """SELECT sf.id, sf.servicio_folio, sf.fallo_id, sf.cantidad,
                          f.nombre, f.costo, f.descripcion
                   FROM servicio_fallos sf
                   JOIN fallos f ON sf.fallo_id = f.id
                   WHERE sf.servicio_folio = %s
                   ORDER BY f.nombre"""
        return self.fetch_all(query, (folio,))

    def get_total_by_service(self, folio):
        query = """SELECT COALESCE(SUM(f.costo * sf.cantidad), 0) AS total
                   FROM servicio_fallos sf
                   JOIN fallos f ON sf.fallo_id = f.id
                   WHERE sf.servicio_folio = %s"""
        result = self.fetch_one(query, (folio,))
        return float(result.get("total", 0) or 0) if result else 0.0