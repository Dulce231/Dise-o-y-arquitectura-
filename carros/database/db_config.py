import sqlite3
from pathlib import Path

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except Exception:
    mysql = None

    class MySQLError(Exception):
        pass


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.backend = None
            cls._instance.connect()
        return cls._instance

    def connect(self):
        if self.connection is not None:
            return

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="sistema_servicios",
                user="root",
                password="",
            ) if 'mysql' in globals() and mysql else None

            if self.connection and self.connection.is_connected():
                self.backend = "mysql"
                self._ensure_schema_mysql()
                print("Conexión a MySQL exitosa")
                return
        except Exception:
            self.connection = None

        self._connect_sqlite()

    def _connect_sqlite(self):
        db_path = Path(__file__).resolve().parent / "sistema_servicios.db"
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.backend = "sqlite"
        self._ensure_schema_sqlite()
        print(f"Usando base local SQLite: {db_path.name}")

    def get_connection(self):
        if self.connection is None:
            self.connect()
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def _prepare_query(self, query):
        if self.backend == "sqlite":
            return query.replace("%s", "?")
        return query

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        params = params or ()

        try:
            if self.backend == "mysql":
                cursor = connection.cursor(dictionary=True, buffered=True)
                cursor.execute(query, params)
            else:
                cursor = connection.cursor()
                cursor.execute(self._prepare_query(query), params)

            connection.commit()
            return cursor
        except (sqlite3.Error, MySQLError, Exception) as e:
            print(f"Error en consulta: {e}")
            try:
                connection.rollback()
            except Exception:
                pass
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if not cursor:
            return []

        rows = cursor.fetchall()
        cursor.close()

        if self.backend == "sqlite":
            return [dict(row) for row in rows]
        return rows

    def _ensure_schema_sqlite(self):
        schema = """
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        );

        CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS modelos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca_id INTEGER NOT NULL,
            FOREIGN KEY (marca_id) REFERENCES marcas(id)
        );

        CREATE TABLE IF NOT EXISTS anos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            año INTEGER NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            marca_id INTEGER NOT NULL,
            modelo_id INTEGER NOT NULL,
            año_id INTEGER NOT NULL,
            placas TEXT NOT NULL UNIQUE,
            color TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (marca_id) REFERENCES marcas(id),
            FOREIGN KEY (modelo_id) REFERENCES modelos(id),
            FOREIGN KEY (año_id) REFERENCES anos(id)
        );

        CREATE TABLE IF NOT EXISTS servicios (
            folio TEXT PRIMARY KEY,
            vehiculo_id INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL,
            fecha_registro TEXT NOT NULL,
            fecha_proximo_servicio TEXT,
            estatus TEXT NOT NULL,
            quien_llevo TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS refacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL DEFAULT 0,
            stock INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS servicio_refacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servicio_folio TEXT NOT NULL,
            refaccion_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (servicio_folio) REFERENCES servicios(folio) ON DELETE CASCADE,
            FOREIGN KEY (refaccion_id) REFERENCES refacciones(id)
        );
        """

        self.connection.executescript(schema)
        self._seed_sqlite_data()
        self.connection.commit()

    def _seed_sqlite_data(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO administradores (id, nombre, usuario, contrasena) VALUES (1, ?, ?, ?)",
            ("Administrador", "admin", "admin123"),
        )

        marcas = ["Nissan", "Toyota", "Honda", "Ford", "Mazda"]
        for marca in marcas:
            cursor.execute("INSERT OR IGNORE INTO marcas (nombre) VALUES (?)", (marca,))

        modelos = [
            ("Versa", 1),
            ("Sentra", 1),
            ("Corolla", 2),
            ("Hilux", 2),
            ("Civic", 3),
            ("Accord", 3),
            ("Focus", 4),
            ("Ranger", 4),
            ("Mazda 3", 5),
        ]
        for nombre, marca_id in modelos:
            cursor.execute(
                "INSERT OR IGNORE INTO modelos (id, nombre, marca_id) VALUES ((SELECT id FROM modelos WHERE nombre = ? AND marca_id = ?), ?, ?)",
                (nombre, marca_id, nombre, marca_id),
            )

        for year in range(2026, 2014, -1):
            cursor.execute("INSERT OR IGNORE INTO anos (año) VALUES (?)", (year,))

        refacciones = [
            ("Filtro de aceite", 180.0, 12),
            ("Balatas", 950.0, 8),
            ("Bujías", 420.0, 20),
        ]
        for nombre, precio, stock in refacciones:
            cursor.execute(
                "INSERT OR IGNORE INTO refacciones (id, nombre, precio, stock) VALUES ((SELECT id FROM refacciones WHERE nombre = ?), ?, ?, ?)",
                (nombre, nombre, precio, stock),
            )

    def _ensure_schema_mysql(self):
        statements = [
            """CREATE TABLE IF NOT EXISTS administradores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                usuario VARCHAR(50) NOT NULL UNIQUE,
                contrasena VARCHAR(100) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(120) NOT NULL,
                telefono VARCHAR(30),
                direccion VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS marcas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(80) NOT NULL UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS modelos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(80) NOT NULL,
                marca_id INT NOT NULL,
                FOREIGN KEY (marca_id) REFERENCES marcas(id)
            )""",
            """CREATE TABLE IF NOT EXISTS anos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                año INT NOT NULL UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS vehiculos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_id INT NOT NULL,
                marca_id INT NOT NULL,
                modelo_id INT NOT NULL,
                año_id INT NOT NULL,
                placas VARCHAR(20) NOT NULL UNIQUE,
                color VARCHAR(40),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (marca_id) REFERENCES marcas(id),
                FOREIGN KEY (modelo_id) REFERENCES modelos(id),
                FOREIGN KEY (año_id) REFERENCES anos(id)
            )""",
            """CREATE TABLE IF NOT EXISTS servicios (
                folio VARCHAR(30) PRIMARY KEY,
                vehiculo_id INT NOT NULL,
                cliente_id INT NOT NULL,
                fecha_registro DATE NOT NULL,
                fecha_proximo_servicio DATE,
                estatus VARCHAR(30) NOT NULL,
                quien_llevo VARCHAR(120) NOT NULL,
                observaciones TEXT,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )""",
            """CREATE TABLE IF NOT EXISTS refacciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(120) NOT NULL,
                precio DECIMAL(10,2) NOT NULL DEFAULT 0,
                stock INT NOT NULL DEFAULT 0
            )""",
            """CREATE TABLE IF NOT EXISTS servicio_refacciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                servicio_folio VARCHAR(30) NOT NULL,
                refaccion_id INT NOT NULL,
                cantidad INT NOT NULL DEFAULT 1,
                FOREIGN KEY (servicio_folio) REFERENCES servicios(folio) ON DELETE CASCADE,
                FOREIGN KEY (refaccion_id) REFERENCES refacciones(id)
            )""",
        ]

        for statement in statements:
            self.execute_query(statement)

        self.execute_query(
            "INSERT IGNORE INTO administradores (id, nombre, usuario, contrasena) VALUES (%s, %s, %s, %s)",
            (1, "Administrador", "admin", "admin123"),
        )

        for marca in ["Nissan", "Toyota", "Honda", "Ford", "Mazda"]:
            self.execute_query("INSERT IGNORE INTO marcas (nombre) VALUES (%s)", (marca,))

        for nombre, marca_nombre in [
            ("Versa", "Nissan"),
            ("Sentra", "Nissan"),
            ("Corolla", "Toyota"),
            ("Hilux", "Toyota"),
            ("Civic", "Honda"),
            ("Accord", "Honda"),
            ("Focus", "Ford"),
            ("Ranger", "Ford"),
            ("Mazda 3", "Mazda"),
        ]:
            self.execute_query(
                """INSERT INTO modelos (nombre, marca_id)
                   SELECT %s, id FROM marcas
                   WHERE nombre=%s
                     AND NOT EXISTS (
                         SELECT 1 FROM modelos mo
                         JOIN marcas ma ON mo.marca_id = ma.id
                         WHERE mo.nombre=%s AND ma.nombre=%s
                     )
                   LIMIT 1""",
                (nombre, marca_nombre, nombre, marca_nombre),
            )

        for year in range(2026, 2014, -1):
            self.execute_query("INSERT IGNORE INTO anos (año) VALUES (%s)", (year,))

        for nombre, precio, stock in [("Filtro de aceite", 180.0, 12), ("Balatas", 950.0, 8), ("Bujías", 420.0, 20)]:
            self.execute_query(
                """INSERT INTO refacciones (nombre, precio, stock)
                   SELECT %s, %s, %s
                   WHERE NOT EXISTS (
                       SELECT 1 FROM refacciones WHERE nombre=%s
                   )""",
                (nombre, precio, stock, nombre),
            )