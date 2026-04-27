from pathlib import Path


def construir_texto_comprobante(folio, datos_servicio):
    refacciones = datos_servicio.get("refacciones", [])
    listado_refacciones = ", ".join([r.get("nombre", "") for r in refacciones]) if refacciones else "Sin refacciones registradas"
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