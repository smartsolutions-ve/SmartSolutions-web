import io
from fpdf import FPDF
from django.utils import timezone
from apps.core.models import ConfiguracionSitio

class PDFReport(FPDF):
    def header(self):
        config = ConfiguracionSitio.get_config()
        # Logo o Nombre de la empresa
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(15, 23, 42) # Brand Navy
        self.cell(0, 10, config.nombre_empresa, border=False, align='L')
        
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100)
        self.cell(0, 10, f"Generado el: {timezone.now().strftime('%d/%m/%Y %H:%M')}", border=False, align='R')
        self.ln(15)
        
        # Línea decorativa
        self.set_draw_color(37, 99, 235) # Brand Blue
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')

def generar_pdf_sesion(sesion):
    """
    Genera un archivo PDF con el resumen de respuestas de una sesión.
    Retorna un objeto BytesIO con el contenido del PDF.
    """
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título del Formulario
    pdf.set_font('helvetica', 'B', 18)
    pdf.set_text_color(0)
    pdf.multi_cell(0, 10, f"Reporte de Levantamiento: {sesion.formulario.nombre}")
    pdf.ln(5)

    # Información del Lead
    pdf.set_fill_color(248, 250, 252) # Light Gray
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 8, " INFORMACIÓN DEL CLIENTE", ln=True, fill=True)
    pdf.set_font('helvetica', '', 10)
    
    lead_name = sesion.lead.nombre if sesion.lead else "Desconocido"
    lead_email = sesion.lead.email if sesion.lead else "No proporcionado"
    
    pdf.cell(40, 7, "Nombre:", border='B')
    pdf.cell(0, 7, lead_name, border='B', ln=True)
    pdf.cell(40, 7, "Email:", border='B')
    pdf.cell(0, 7, lead_email, border='B', ln=True)
    pdf.cell(40, 7, "ID Sesión:", border='B')
    pdf.cell(0, 7, str(sesion.pk), border='B', ln=True)
    pdf.ln(10)

    # Respuestas agrupadas por fase
    respuestas_por_fase = sesion.get_respuestas_agrupadas()
    
    for fase, items in respuestas_por_fase.items():
        # Encabezado de la fase
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(37, 99, 235) # Blue
        pdf.cell(0, 10, f"Módulo: {fase.titulo}", ln=True)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(pdf.get_x(), pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

        for item in items:
            # Pregunta
            pdf.set_font('helvetica', 'B', 10)
            pdf.set_text_color(51, 65, 85) # Slate 700
            pdf.multi_cell(0, 6, item['pregunta'])
            
            # Respuesta
            pdf.set_font('helvetica', '', 10)
            pdf.set_text_color(0)
            valor = item['respuesta']
            
            # Manejar listas (checks)
            if isinstance(valor, list):
                valor = ", ".join(valor)
            elif not valor:
                valor = "(Sin respuesta)"
                
            pdf.set_fill_color(255, 255, 255)
            pdf.multi_cell(0, 6, valor)
            pdf.ln(3)
        
        pdf.ln(5)

    # Output buffer
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
