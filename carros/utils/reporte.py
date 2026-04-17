from pathlib import Path
import os


def generar_comprobante(folio, datos_servicio):
    output_dir = Path("reportes")
    output_dir.mkdir(exist_ok=True)

    refacciones = datos_servicio.get("refacciones", [])
    listado_refacciones = ", ".join([r.get("nombre", "") for r in refacciones]) if refacciones else "Sin refacciones registradas"

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch

        filename = output_dir / f"comprobante_{folio}.pdf"
        doc = SimpleDocTemplate(str(filename), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=16,
            textColor=colors.HexColor("#003366"),
            alignment=1,
            spaceAfter=24,
        )
        story.append(Paragraph("COMPROBANTE DE SERVICIO", title_style))

        data = [
            ["FOLIO", folio],
            ["FECHA REGISTRO", datos_servicio.get("fecha_registro", "")],
            ["CLIENTE", datos_servicio.get("cliente_nombre", "")],
            ["TELÉFONO", datos_servicio.get("telefono", "N/A")],
            ["DIRECCIÓN", datos_servicio.get("direccion", "N/A")],
            ["VEHÍCULO", f"{datos_servicio.get('marca_nombre', '')} {datos_servicio.get('modelo_nombre', '')} - {datos_servicio.get('año', '')}"],
            ["PLACAS", datos_servicio.get("placas", "N/A")],
            ["COLOR", datos_servicio.get("color", "N/A")],
            ["QUIÉN LLEVÓ", datos_servicio.get("quien_llevo", "N/A")],
            ["ESTATUS", datos_servicio.get("estatus", "N/A")],
            ["PRÓXIMO SERVICIO", datos_servicio.get("fecha_proximo_servicio", "N/A")],
            ["REFACCIONES", listado_refacciones],
            ["OBSERVACIONES", datos_servicio.get("observaciones", "") or "Sin observaciones"],
        ]

        table = Table(data, colWidths=[2.1 * inch, 4.2 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dbeafe")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        story.append(table)
        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph("Este comprobante respalda el ingreso del vehículo a servicio.", styles["Normal"]))
        doc.build(story)
        if os.name == "nt":
            try:
                os.startfile(str(filename))
            except Exception:
                pass
        return str(filename)
    except Exception:
        filename = output_dir / f"comprobante_{folio}.txt"
        contenido = [
            "COMPROBANTE DE SERVICIO",
            f"Folio: {folio}",
            f"Cliente: {datos_servicio.get('cliente_nombre', '')}",
            f"Vehículo: {datos_servicio.get('marca_nombre', '')} {datos_servicio.get('modelo_nombre', '')}",
            f"Placas: {datos_servicio.get('placas', '')}",
            f"Estatus: {datos_servicio.get('estatus', '')}",
            f"Quién llevó: {datos_servicio.get('quien_llevo', '')}",
            f"Próximo servicio: {datos_servicio.get('fecha_proximo_servicio', '')}",
            f"Refacciones: {listado_refacciones}",
            f"Observaciones: {datos_servicio.get('observaciones', '')}",
        ]
        filename.write_text("\n".join(contenido), encoding="utf-8")
        return str(filename)