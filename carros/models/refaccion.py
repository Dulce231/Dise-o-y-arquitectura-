from models.base_repository import BaseRepository


class Refaccion(BaseRepository):
    def __init__(self):
        super().__init__()

    def create(self, nombre, precio, stock):
        query = "INSERT INTO refacciones (nombre, precio, stock) VALUES (%s, %s, %s)"
        cursor = self.db.execute_query(query, (nombre, precio, stock))
        return cursor.lastrowid if cursor else None

    def get_all(self):
        return self.db.fetch_all("SELECT * FROM refacciones ORDER BY nombre")

    def get_by_id(self, id):
        result = self.db.fetch_all("SELECT * FROM refacciones WHERE id=%s", (id,))
        return result[0] if result else None

    def update(self, id, nombre, precio, stock):
        query = "UPDATE refacciones SET nombre=%s, precio=%s, stock=%s WHERE id=%s"
        return self.db.execute_query(query, (nombre, precio, stock, id))

    def adjust_stock(self, id, delta):
        refaccion = self.get_by_id(id)
        if not refaccion:
            raise ValueError("La refacción seleccionada no existe.")

        nuevo_stock = int(refaccion["stock"]) + int(delta)
        if nuevo_stock < 0:
            raise ValueError(f"Stock insuficiente para {refaccion['nombre']}. Disponible: {refaccion['stock']}")

        query = "UPDATE refacciones SET stock=%s WHERE id=%s"
        self.db.execute_query(query, (nuevo_stock, id))
        return nuevo_stock

    def decrease_stock(self, id, cantidad=1):
        return self.adjust_stock(id, -abs(int(cantidad)))

    def increase_stock(self, id, cantidad=1):
        return self.adjust_stock(id, abs(int(cantidad)))

    def delete(self, id):
        query = "DELETE FROM refacciones WHERE id=%s"
        return self.db.execute_query(query, (id,))