from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Preformatted,
)
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "report" / "informe_final.md"
REPORT_PDF = ROOT / "report" / "informe_final.pdf"
REPORT_LATEX_DIR = ROOT / "report" / "latex"
REPORT_LATEX = REPORT_LATEX_DIR / "informe_final.tex"
REPORT_LATEX_PDF = REPORT_LATEX_DIR / "informe_final.pdf"
SLIDES_PDF = ROOT / "slides" / "presentacion_final.pdf"

BG = colors.HexColor("#05050a")
FG = colors.HexColor("#f2f2f2")
MUTED = colors.HexColor("#b8b8c8")
CYAN = colors.HexColor("#42e8f5")
MAGENTA = colors.HexColor("#ff2bd6")
GOLD = colors.HexColor("#ffcf33")
GREEN = colors.HexColor("#82ff7a")


def _page_footer(c: canvas.Canvas, doc):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawRightString(letter[0] - 0.55 * inch, 0.35 * inch, f"ChaosLab - {doc.page}")
    c.restoreState()


def _clean_inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", text)
    return text


def build_report_pdf() -> None:
    REPORT_PDF.parent.mkdir(exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleClean",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        alignment=TA_CENTER,
        spaceAfter=16,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        spaceBefore=12,
        spaceAfter=7,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=9,
        spaceAfter=5,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        alignment=TA_LEFT,
        spaceAfter=7,
    )
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, firstLineIndent=-8)
    code = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8,
        leading=10,
        backColor=colors.HexColor("#f4f4f4"),
        borderPadding=5,
        spaceBefore=4,
        spaceAfter=8,
    )

    story = []
    in_code = False
    code_lines: list[str] = []

    for raw in REPORT_MD.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                story.append(Preformatted("\n".join(code_lines), code))
                in_code = False
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line:
            story.append(Spacer(1, 4))
            continue
        if line.startswith("# "):
            story.append(Paragraph(_clean_inline(line[2:]), title))
            continue
        if line.startswith("## "):
            story.append(Paragraph(_clean_inline(line[3:]), h1))
            continue
        if line.startswith("### "):
            story.append(Paragraph(_clean_inline(line[4:]), h2))
            continue
        if line.startswith("!["):
            match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if match:
                caption, rel = match.groups()
                img_path = (REPORT_MD.parent / rel).resolve()
                if img_path.exists():
                    story.append(Image(str(img_path), width=6.1 * inch, height=3.55 * inch, kind="proportional"))
                    story.append(Paragraph(f"<i>{_clean_inline(caption)}</i>", body))
            continue
        if line.startswith("- "):
            story.append(Paragraph("- " + _clean_inline(line[2:]), bullet))
            continue
        if re.match(r"^\d+\. ", line):
            story.append(Paragraph(_clean_inline(line), bullet))
            continue
        story.append(Paragraph(_clean_inline(line), body))

    doc = SimpleDocTemplate(
        str(REPORT_PDF),
        pagesize=letter,
        rightMargin=0.62 * inch,
        leftMargin=0.62 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.55 * inch,
    )
    doc.build(story, onFirstPage=_page_footer, onLaterPages=_page_footer)


def _draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float, size: int = 24, color=FG, leading: float | None = None):
    leading = leading or size * 1.18
    style = ParagraphStyle(
        "SlideText",
        fontName="Helvetica",
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
    )
    p = Paragraph(_clean_inline(text), style)
    _, h = p.wrap(width, 6 * inch)
    p.drawOn(c, x, y - h)
    return y - h


def _draw_image(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float):
    if not path.exists():
        c.setStrokeColor(colors.HexColor("#333344"))
        c.rect(x, y, w, h)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 14)
        c.drawCentredString(x + w / 2, y + h / 2, f"Missing: {path.name}")
        return
    img = ImageReader(str(path))
    iw, ih = img.getSize()
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(img, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, preserveAspectRatio=True, mask="auto")


def _slide_bg(c: canvas.Canvas, title: str, kicker: str | None = None):
    w, h = landscape(letter)
    c.setFillColor(BG)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 15)
    if kicker:
        c.drawString(0.55 * inch, h - 0.42 * inch, kicker)
    c.setFillColor(FG)
    c.setFont("Helvetica-Bold", 27)
    c.drawString(0.55 * inch, h - 0.82 * inch, title)
    c.setStrokeColor(colors.HexColor("#2b2b3d"))
    c.line(0.55 * inch, h - 0.98 * inch, w - 0.55 * inch, h - 0.98 * inch)


def build_slides_pdf() -> None:
    SLIDES_PDF.parent.mkdir(exist_ok=True)
    c = canvas.Canvas(str(SLIDES_PDF), pagesize=landscape(letter))
    w, h = landscape(letter)

    slides = [
        (
            "ChaosLab",
            "Mismas leyes, futuros distintos",
            ["Proyecto final de Fisica I", "Pendulo doble, energia y sensibilidad a condiciones iniciales"],
            ROOT / "figures" / "trajectory_mass2.png",
        ),
        (
            "1. El caso ordenado",
            "Pendulo simple",
            ["theta describe la posicion angular.", "omega = d theta / dt.", "Para angulos pequenos: sin(theta) ~= theta."],
            None,
        ),
        (
            "2. Agregar una segunda masa",
            "De una coordenada a cuatro variables de estado",
            ["s(t) = [theta1, omega1, theta2, omega2]", "Las barras quedan acopladas.", "La energia se transfiere entre dos grados de libertad."],
            ROOT / "animations" / "double_pendulum.gif",
        ),
        (
            "3. Simulacion numerica",
            "Resolver las ecuaciones, no dibujar a mano",
            ["El sistema se integra con solve_ivp.", "Metodo usado: DOP853.", "Cada frame sale del modelo fisico."],
            ROOT / "figures" / "trajectory_mass2.png",
        ),
        (
            "4. Energia como control de calidad",
            "Si la energia explota, el resultado no sirve",
            ["La energia cinetica y potencial cambian.", "La energia total permanece casi constante.", "La divergencia no viene de crear energia artificialmente."],
            ROOT / "figures" / "energy_vs_time.png",
        ),
        (
            "5. Sensibilidad inicial",
            "Una diferencia invisible se vuelve visible",
            ["Perturbacion: epsilon = 1e-6 rad.", "Delta(t) mide separacion en espacio de fases.", "La escala logaritmica revela crecimiento temprano."],
            ROOT / "figures" / "divergence_semilog.png",
        ),
        (
            "6. Cada pixel es un experimento",
            "Mapa de condiciones iniciales",
            ["x = theta1(0), y = theta2(0).", "Color = tiempo hasta el primer flip.", "Aparecen regiones ordenadas, caoticas e islas de estabilidad."],
            ROOT / "figures" / "flip_time_fractal_map.png",
        ),
        (
            "Conclusion",
            "Deterministico no significa predecible",
            ["La fisica da reglas locales.", "La computacion revela consecuencias globales.", "ChaosLab combina Fisica I, Calculo I, EDOs y visualizacion."],
            None,
        ),
    ]

    for i, (title, kicker, bullets, img) in enumerate(slides, start=1):
        _slide_bg(c, title, kicker)
        if img:
            _draw_image(c, img, 5.8 * inch, 0.75 * inch, 4.75 * inch, 5.35 * inch)
            text_w = 4.75 * inch
        else:
            text_w = 8.8 * inch
        y = h - 1.55 * inch
        for bullet in bullets:
            c.setFillColor(GOLD if i in (1, 8) else CYAN)
            c.circle(0.78 * inch, y - 0.1 * inch, 0.055 * inch, fill=1, stroke=0)
            y = _draw_wrapped(c, bullet, 0.95 * inch, y, text_w, size=21, color=FG, leading=27) - 0.25 * inch
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawRightString(w - 0.55 * inch, 0.35 * inch, f"{i}/8")
        c.showPage()

    c.save()


def build_report_pdf() -> None:
    REPORT_PDF.parent.mkdir(exist_ok=True)
    if not REPORT_LATEX.exists():
        raise FileNotFoundError(f"Missing LaTeX report source: {REPORT_LATEX}")

    latexmk = shutil.which("latexmk")
    if latexmk is None:
        raise RuntimeError("latexmk is required to build report/informe_final.pdf from LaTeX")

    subprocess.run(
        [
            latexmk,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            REPORT_LATEX.name,
        ],
        cwd=REPORT_LATEX_DIR,
        check=True,
    )
    if not REPORT_LATEX_PDF.exists():
        raise FileNotFoundError(f"LaTeX did not produce {REPORT_LATEX_PDF}")
    shutil.copy2(REPORT_LATEX_PDF, REPORT_PDF)


def main() -> None:
    build_report_pdf()
    build_slides_pdf()
    print(REPORT_PDF)
    print(SLIDES_PDF)


if __name__ == "__main__":
    main()
