# Sistema de Servicios Automotrices

Proyecto con interfaz gráfica para administración de servicios de vehículos.

## Funcionalidades implementadas

- Login privado para administradores.
- Menú visual por pestañas para navegación.
- CRUD de marcas, modelos, años y refacciones.
- Registro, consulta, modificación y eliminación de servicios.
- Búsqueda por folio o nombre del dueño.
- Estatus de servicio: En espera, En proceso y Finalizado.
- Registro de próximo servicio.
- Campo de control para saber quién llevó el vehículo.
- Relación de varias refacciones por servicio.
- Generación de comprobante en PDF o TXT.
- Dashboard con gráfica por día o por total.
- Cierre de sesión y salida segura del sistema.

## Patrones de diseño usados

1. Singleton
   - En la conexión de base de datos y la sesión global.
2. Repository
   - En la capa de acceso a datos mediante los modelos y la base común.

## Acceso inicial

- Usuario: admin
- Contraseña: admin123

## Evidencia de GitHub

Para cubrir la participación del equipo:

1. Inicializar repositorio Git.
2. Cada integrante debe usar su propia cuenta y rama.
3. Registrar avances con commits claros.
4. Hacer push y merge mediante pull requests.
5. Entregar el enlace del repositorio con historial visible.

## Ejecución

Ejecutar la aplicación principal desde el proyecto:

python main.py
