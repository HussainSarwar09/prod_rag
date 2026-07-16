"""
Generate PDF fixtures for testing.
"""

from pathlib import Path

from reportlab.pdfgen import canvas

FIXTURE_DIR = Path("tests/fixtures/pdf")
FIXTURE_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf(name: str, pages: int) -> None:
    pdf = canvas.Canvas(str(FIXTURE_DIR / name))

    for page in range(pages):
        pdf.drawString(
            100,
            750,
            f"This is page {page + 1}",
        )
        pdf.showPage()

    pdf.save()


create_pdf("single_page.pdf", 1)

create_pdf("multi_page.pdf", 3)
