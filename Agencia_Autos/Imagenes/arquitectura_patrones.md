# Arquitectura y patrones del sistema

Este diagrama resume dónde están los patrones de diseño que usa el proyecto.

```mermaid
classDiagram
    direction LR

    class AutoTallerApp {
        +show_login()
        +show_main_screen()
        +save_service()
        +refresh_all()
    }

    class Session {
        <<Singleton>>
        -_instance
        +login(user_data)
        +logout()
        +is_logged_in()
        +get_user()
    }

    class DatabaseConnection {
        <<Singleton>>
        -_instance
        +connect()
        +execute_query()
        +fetch_all()
    }

    class BaseRepository {
        <<Repository base>>
        +execute()
        +fetch_all()
        +fetch_one()
    }

    class Cliente
    class Vehiculo
    class Servicio
    class Refaccion
    class Fallo
    class ServicioRefaccion
    class ServicioFallo

    AutoTallerApp --> Session : usa sesión global
    AutoTallerApp --> DatabaseConnection : usa conexión compartida
    AutoTallerApp --> Cliente : administra datos
    AutoTallerApp --> Vehiculo : administra datos
    AutoTallerApp --> Servicio : administra datos
    AutoTallerApp --> Refaccion : administra datos
    AutoTallerApp --> Fallo : administra datos
    AutoTallerApp --> ServicioRefaccion : vincula refacciones
    AutoTallerApp --> ServicioFallo : vincula fallos

    BaseRepository --> DatabaseConnection : depende de la conexión
    Cliente --|> BaseRepository
    Vehiculo --|> BaseRepository
    Servicio --|> BaseRepository
    Refaccion --|> BaseRepository
    Fallo --|> BaseRepository
    ServicioRefaccion --|> BaseRepository
    ServicioFallo --|> BaseRepository
```

## Cómo leerlo

- `Session` y `DatabaseConnection` son Singleton porque el sistema necesita una sola instancia compartida.
- Los modelos heredan de `BaseRepository`, que centraliza el acceso a la base de datos.
- `AutoTallerApp` solo orquesta la interfaz; no guarda la lógica de datos.