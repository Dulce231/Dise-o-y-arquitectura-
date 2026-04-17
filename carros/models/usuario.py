from models.base_repository import BaseRepository


class Usuario(BaseRepository):
    def __init__(self):
        super().__init__()

    def authenticate(self, usuario, contrasena):
        query = "SELECT * FROM administradores WHERE usuario = %s AND contrasena = %s"
        result = self.db.fetch_all(query, (usuario, contrasena))
        return result[0] if result else None