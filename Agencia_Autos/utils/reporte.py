from pathlib import Path


def _formatear_monto(valor):
    try:
        return f"${float(valor):,.2f}"
    except Exception:
        return "$0.00"


def construir_texto_comprobante(folio, datos_servicio):
    refacciones = datos_servicio.get("refacciones", [])
    fallos = datos_servicio.get("fallos", [])

    listado_refacciones = []
    for item in refacciones:
        cantidad = int(item.get("cantidad", 1) or 1)
        nombre = item.get("nombre", "")
        precio = _formatear_monto(item.get("precio", 0))
        if cantidad > 1:
            listado_refacciones.append(f"{nombre} x{cantidad} ({precio} c/u)")
        else:
            listado_refacciones.append(f"{nombre} ({precio})")
    listado_refacciones = ", ".join(listado_refacciones) if listado_refacciones else "Sin refacciones registradas"

    listado_fallos = []
    for item in fallos:
        cantidad = int(item.get("cantidad", 1) or 1)
        nombre = item.get("nombre", "")
        costo = _formatear_monto(item.get("costo", 0))
        if cantidad > 1:
            listado_fallos.append(f"{nombre} x{cantidad} ({costo} c/u)")
        else:
            listado_fallos.append(f"{nombre} ({costo})")
    listado_fallos = ", ".join(listado_fallos) if listado_fallos else "Sin fallos registrados"

    total_refacciones = datos_servicio.get("total_refacciones")
    if total_refacciones is None:
        total_refacciones = sum(float(item.get("precio", 0) or 0) * int(item.get("cantidad", 1) or 1) for item in refacciones)

    total_fallos = datos_servicio.get("total_fallos")
    if total_fallos is None:
        total_fallos = sum(float(item.get("costo", 0) or 0) * int(item.get("cantidad", 1) or 1) for item in fallos)

    total_general = datos_servicio.get("total_general")
    if total_general is None:
        total_general = float(total_refacciones) + float(total_fallos)
    lineas = [
        "COMPROBANTE DE SERVICIO",
        "=" * 40,
        f"Folio: {folio}",
        f"Fecha registro: {datos_servicio.get('fecha_registro', '')}",
        "",
        "DATOS DEL CLIENTE",
        f"Cliente: {datos_servicio.get('cliente_nombre', '')}",
        f"Telefono: {datos_servicio.get('telefono', 'N/A')}",
        f"Direccion: {datos_servicio.get('direccion', 'N/A')}",
        "",
        "DATOS DEL VEHICULO",
        f"Vehiculo: {datos_servicio.get('marca_nombre', '')} {datos_servicio.get('modelo_nombre', '')} - {datos_servicio.get('año', '')}",
        f"Placas: {datos_servicio.get('placas', 'N/A')}",
        f"Color: {datos_servicio.get('color', 'N/A')}",
        "",
        "SERVICIO",
        f"Quien llevo: {datos_servicio.get('quien_llevo', 'N/A')}",
        f"Estatus: {datos_servicio.get('estatus', 'N/A')}",
        f"Proximo servicio: {datos_servicio.get('fecha_proximo_servicio', 'N/A')}",
        f"Refacciones: {listado_refacciones}",
        f"Total refacciones: {_formatear_monto(total_refacciones)}",
        f"Fallos: {listado_fallos}",
        f"Total fallos: {_formatear_monto(total_fallos)}",
        f"Total general: {_formatear_monto(total_general)}",
        f"Observaciones: {datos_servicio.get('observaciones', '') or 'Sin observaciones'}",
        "",
        "Este comprobante respalda el ingreso del vehiculo a servicio.",
    ]
    return "\n".join(lineas)


def generar_comprobante(folio, datos_servicio):
    output_dir = Path("reportes")
    output_dir.mkdir(exist_ok=True)

    # Si existia un PDF antiguo del mismo folio, se elimina para evitar confusion.
    pdf_anterior = output_dir / f"comprobante_{folio}.pdf"
    if pdf_anterior.exists():
        pdf_anterior.unlink()

    filename = output_dir / f"comprobante_{folio}.txt"
    contenido = construir_texto_comprobante(folio, datos_servicio)
    filename.write_text(contenido, encoding="utf-8")
    return str(filename)