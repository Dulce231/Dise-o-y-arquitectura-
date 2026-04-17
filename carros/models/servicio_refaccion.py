from collections import Counter

from models.base_repository import BaseRepository
from models.refaccion import Refaccion


class ServicioRefaccion(BaseRepository):
    def __init__(self):
        super().__init__()
        self.refaccion_model = Refaccion()

    def replace_for_service(self, folio, refaccion_ids):
        actuales = self.get_by_service(folio)
        cantidades_actuales = Counter({item["refaccion_id"]: int(item.get("cantidad", 1)) for item in actuales})
        cantidades_nuevas = Counter(refaccion_ids or [])

        for refaccion_id, cantidad in cantidades_nuevas.items():
            refaccion = self.refaccion_model.get_by_id(refaccion_id)
            if not refaccion:
                raise ValueError("La refacción seleccionada no existe.")

            disponible = int(refaccion["stock"]) + int(cantidades_actuales.get(refaccion_id, 0))
            if cantidad > disponible:
                raise ValueError(f"Stock insuficiente para {refaccion['nombre']}. Disponible: {refaccion['stock']}")

        self.clear_for_service(folio, restore_stock=True)

        for refaccion_id, cantidad in cantidades_nuevas.items():
            self.refaccion_model.decrease_stock(refaccion_id, cantidad)
            self.execute(
                "INSERT INTO servicio_refacciones (servicio_folio, refaccion_id, cantidad) VALUES (%s, %s, %s)",
                (folio, refaccion_id, cantidad),
            )

    def clear_for_service(self, folio, restore_stock=True):
        actuales = self.get_by_service(folio)
        if restore_stock:
            for item in actuales:
                self.refaccion_model.increase_stock(item["refaccion_id"], int(item.get("cantidad", 1)))
        self.execute("DELETE FROM servicio_refacciones WHERE servicio_folio=%s", (folio,))

    def get_by_service(self, folio):
        query = """SELECT sr.id, sr.servicio_folio, sr.refaccion_id, sr.cantidad,
                          r.nombre, r.precio, r.stock
                   FROM servicio_refacciones sr
                   JOIN refacciones r ON sr.refaccion_id = r.id
                   WHERE sr.servicio_folio = %s
                   ORDER BY r.nombre"""
        return self.fetch_all(query, (folio,))