"""
Generate tangible sample assets for the 15 Multimodal Test Cases
Creates sample PDF documents, diagrams using PIL, and sample audio transcripts.
Student: Reshma Anandhan
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ASSETS_DIR = Path(__file__).resolve().parent / "sample_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_sample_images():
    """Generates sample PNG test images for image test cases."""
    # 1. Logic Gate Diagram
    img1 = Image.new('RGB', (800, 450), color='#0f172a')
    draw1 = ImageDraw.Draw(img1)
    # Draw logic gate schematic
    draw1.rectangle([(20, 20), (780, 430)], outline='#38bdf8', width=2)
    draw1.text((40, 40), "TEST CASE TC-IMG-01: DIGITAL LOGIC CIRCUIT", fill='#38bdf8')
    draw1.text((40, 80), "Inputs: A, B, C", fill='#94a3b8')
    draw1.text((40, 110), "Gate 1: AND(A, B) -> Node W1", fill='#f8fafc')
    draw1.text((40, 140), "Gate 2: XOR(B, C) -> Node W2", fill='#f8fafc')
    draw1.text((40, 170), "Gate 3: OR(W1, W2) -> Output Y", fill='#34d399')
    draw1.text((40, 220), "Target Expression: Y = (A AND B) OR (B XOR C)", fill='#f59e0b')
    # Draw simple visual boxes representing gates
    draw1.rectangle([(400, 90), (520, 140)], outline='#38bdf8', width=2)
    draw1.text((430, 105), "AND GATE", fill='#38bdf8')
    draw1.rectangle([(400, 180), (520, 230)], outline='#818cf8', width=2)
    draw1.text((430, 195), "XOR GATE", fill='#818cf8')
    draw1.rectangle([(620, 135), (740, 185)], outline='#34d399', width=2)
    draw1.text((650, 150), "OR GATE", fill='#34d399')
    # Lines
    draw1.line([(520, 115), (620, 150)], fill='#94a3b8', width=2)
    draw1.line([(520, 205), (620, 170)], fill='#94a3b8', width=2)
    draw1.line([(740, 160), (770, 160)], fill='#34d399', width=3)
    img1.save(ASSETS_DIR / "logic_gate_circuit.png")

    # 2. Handwritten notes mock
    img2 = Image.new('RGB', (800, 500), color='#fef3c7')
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([(15, 15), (785, 485)], outline='#b45309', width=2)
    draw2.text((30, 30), "TC-IMG-02: Advanced Calculus Lecture Notes (Student Notebook)", fill='#1e293b')
    draw2.text((30, 70), "Topic: Indefinite Integrals & Polynomial Integration", fill='#1e293b')
    draw2.text((30, 110), "Formula: ∫ (3x^2 + 2x) dx = x^3 + x^2 + C", fill='#0369a1')
    draw2.text((30, 160), "Key Notes from Prof: Remember constant of integration C!", fill='#b91c1c')
    draw2.text((30, 200), "Example 2: ∫ (6x^5 - 4x^3 + 7) dx = x^6 - x^4 + 7x + C", fill='#1e293b')
    draw2.text((30, 250), "Margin Note: Exam question guaranteed on this technique.", fill='#4b5563')
    draw2.text((30, 300), "Verify by differentiating answer: d/dx(x^3 + x^2 + C) = 3x^2 + 2x. (Matches integrand)", fill='#1e293b')
    img2.save(ASSETS_DIR / "handwritten_lecture_notes.png")

    # 3. Chart mock
    img3 = Image.new('RGB', (800, 450), color='#0f172a')
    draw3 = ImageDraw.Draw(img3)
    draw3.text((40, 30), "TC-IMG-05: Macroeconomic Indicators (2018 - 2024)", fill='#38bdf8')
    draw3.text((40, 60), "Blue Bars: GDP Growth (%) | Amber Line: Inflation Rate (%)", fill='#94a3b8')
    # Draw coordinate box
    draw3.rectangle([(100, 100), (720, 380)], outline='#334155', width=2)
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
    gdp = [2.9, 2.3, -2.1, 5.8, 1.2, 2.5, 2.8]
    inf = [2.4, 1.8, 1.2, 4.7, 8.6, 4.1, 3.1]
    
    for i, yr in enumerate(years):
        x = 140 + i * 85
        # Bar for GDP
        bar_h = int(gdp[i] * 20)
        base_y = 280
        if bar_h >= 0:
            draw3.rectangle([(x, base_y - bar_h), (x + 35, base_y)], fill='#0284c7')
        else:
            draw3.rectangle([(x, base_y), (x + 35, base_y - bar_h)], fill='#ef4444')
        draw3.text((x, 390), yr, fill='#f8fafc')
        draw3.text((x, base_y - bar_h - 15 if bar_h >= 0 else base_y - bar_h + 5), f"{gdp[i]}%", fill='#38bdf8')
    draw3.text((40, 415), "Peak Stagflation: 2022 (GDP: 1.2%, Inflation: 8.6%)", fill='#f59e0b')
    img3.save(ASSETS_DIR / "economic_gdp_inflation_chart.png")

def create_sample_pdfs():
    """Generates sample PDF study files using ReportLab."""
    pdf_path = ASSETS_DIR / "tcp_congestion_research.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=12, textColor='#1e293b')
    h2_style = ParagraphStyle('DocH2', parent=styles['Heading2'], fontSize=13, spaceAfter=8, textColor='#0369a1')
    body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=8)
    
    story = [
        Paragraph("Capstone 57 Research Paper: Modern TCP Congestion Control", title_style),
        Paragraph("Abstract", h2_style),
        Paragraph("Transmission Control Protocol (TCP) governs reliable data delivery across the modern Internet. Traditional loss-based algorithms like TCP Reno interpret packet loss as the sole indicator of network congestion. However, in modern high-speed broadband networks with large buffers (bufferbloat), loss-based algorithms induce excessive queuing delays and throughput degradation.", body_style),
        Spacer(1, 10),
        Paragraph("Section 1: Comparative Analysis of Reno vs BBR", h2_style),
        Paragraph("Google's BBR (Bottleneck Bandwidth and Round-trip propagation time) adopts a model-based paradigm. Rather than reacting blindly to packet loss, BBR dynamically probes and estimates the maximum bottleneck bandwidth and minimum round-trip time. In experimental 10 Gbps transatlantic testbeds, BBR achieves up to 4x higher throughput with 50% lower queue latencies compared to TCP Reno and CUBIC.", body_style),
        Spacer(1, 10),
        Paragraph("Section 2: Experimental Findings and Summary", h2_style),
        Paragraph("In conclusion, model-based congestion control demonstrates superior fairness and efficiency across heterogeneous networks. For college computer networking students, understanding the mathematical trade-off between throughput and queuing delay remains a foundational concept.", body_style)
    ]
    doc.build(story)

    # Flawed document for error detection
    flawed_path = ASSETS_DIR / "software_engineering_flawed.pdf"
    doc2 = SimpleDocTemplate(str(flawed_path), pagesize=letter)
    story2 = [
        Paragraph("Review Document: Principles of Software Engineering (Agile vs Waterfall)", title_style),
        Paragraph("Section 1: The Waterfall Lifecycle Model", h2_style),
        Paragraph("The Waterfall lifecycle is a sequential design process. A notable benefit is that the Waterfall model allows changing requirements freely during the implementation phase whenever clients request modifications. [PLANTED ERROR 1]", body_style),
        Paragraph("Section 2: Agile Scrum Framework", h2_style),
        Paragraph("Scrum is an iterative framework widely used in software development. In standard Scrum methodology, the typical Sprint duration is 6 to 12 months, allowing teams to deliver large monolithic releases. [PLANTED ERROR 2]", body_style),
        Paragraph("Section 3: Software Testing Hierarchy", h2_style),
        Paragraph("Testing ensures product reliability. According to standard software engineering practice, Unit testing is executed after User Acceptance Testing (UAT) is finalized in production. [PLANTED ERROR 3]", body_style)
    ]
    doc2.build(story2)

def create_sample_audio_transcripts():
    """Generates sample audio transcripts as text references for audio test cases."""
    transcript_path = ASSETS_DIR / "acoustics_doppler_lecture.txt"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("""[00:00] Prof. Adams: Good morning, class. Today we explore acoustic waves, the Doppler frequency shift, and the geometry of supersonic Mach cones.
[00:18] When a sound source moves toward an observer at velocity v_source, the observed frequency f' is higher than the emitted frequency f because the wavefronts are compressed.
[00:45] The formula is f' = f * (v_sound / (v_sound - v_source)).
[01:10] Now, what happens when the source exceeds the speed of sound? That is, when the Mach number M = v_source / v_sound is greater than 1?
[01:30] At supersonic speeds, the spherical wavefronts form a conical shockwave envelope known as the Mach cone.
[01:50] The half-angle theta of this Mach cone is given by: theta = arcsin(v_sound / v_source) = arcsin(1 / M).
[02:15] Notice that as the speed of the supersonic aircraft increases, the Mach cone becomes narrower and sharper. This explains why sonic booms are perceived along the hyperbolic ground track. Thank you.""")

if __name__ == "__main__":
    create_sample_images()
    create_sample_pdfs()
    create_sample_audio_transcripts()
    print("Tangible sample assets generated successfully in data/sample_assets/")
