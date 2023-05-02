from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table


def generate_pdf(filename: str, user_details: dict) -> str:
    header = ['field_name', 'field_value']
    rows = ([(key, user_details[key]) for key in user_details.keys()])

    data = [header] + rows

    # Create a PDF file
    pdf_file = f"{filename}.pdf"

    doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=30,
                            leftMargin=30, topMargin=30, bottomMargin=18)
    doc.pagesize = landscape(letter)

    # Create a table with the provided fields
    table = Table(data, colWidths=doc.width/len(header), rowHeights=None)

    # Add the table to the PDF file and build it
    doc.build([table])

    print(f"PDF generated: {pdf_file}")
