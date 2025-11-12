from io import BytesIO
from fastapi import HTTPException
from fastapi.responses import Response

from ...shared.base_auth_handler import BaseAuthHandler
from ....persistence.unit_of_work import UnitOfWork
from .generate_notes_pdf_request import GenerateNotesPdfRequest

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False


class GenerateNotesPdfHandler(BaseAuthHandler[GenerateNotesPdfRequest, Response]):
    async def execute(self, request: GenerateNotesPdfRequest) -> Response:
        if not FPDF_AVAILABLE:
            raise HTTPException(
                status_code=500,
                detail="PDF generation library not available. Please install fpdf2."
            )

        unit_of_work = UnitOfWork(self.session)
        
        # Get student info
        student = await unit_of_work.student_repository.get_by_id(request.student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get student subjects with qualifications
        enrollments = await unit_of_work.classroom_subject_student_repository.get_for_student(
            request.student_id,
            with_relations=True,
            only_active=not request.include_inactive,
        )

        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 10, "Reporte de Notas", ln=1, align="C")
        pdf.ln(10)
        
        # Student info
        student_name = f"{student.names} {student.father_last_name or ''} {student.mother_last_name or ''}".strip()
        student_code = student.code or "N/A"
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"Estudiante: {student_name}", ln=1)
        pdf.cell(0, 8, f"Codigo: {student_code}", ln=1)
        pdf.ln(5)
        
        # Subjects table
        if not enrollments:
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, "No se encontraron asignaturas registradas.", ln=1)
        else:
            # Table header
            pdf.set_font("Arial", "B", 12)
            pdf.set_fill_color(37, 99, 235)  # Blue background
            pdf.set_text_color(255, 255, 255)  # White text
            pdf.cell(120, 10, "Asignatura", border=1, fill=True)
            pdf.cell(60, 10, "Nota Final", border=1, fill=True, ln=1)
            
            # Table rows
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(0, 0, 0)  # Black text
            fill = False
            for enrollment in enrollments:
                classroom_subject = enrollment.classroom_subject
                subject = classroom_subject.subject if classroom_subject else None
                subject_name = subject.name if subject else "Sin nombre"
                final_grade = enrollment.qualification or "Sin calificar"
                
                # Alternate row colors
                if fill:
                    pdf.set_fill_color(249, 250, 251)  # Light gray
                else:
                    pdf.set_fill_color(255, 255, 255)  # White
                fill = not fill
                
                pdf.cell(120, 8, subject_name, border=1, fill=True)
                pdf.cell(60, 8, final_grade, border=1, fill=True, ln=1)
        
        # Get PDF bytes
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        
        # Return PDF response
        filename = f"notas_{student_code}_{student_name.replace(' ', '_')}.pdf"
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
