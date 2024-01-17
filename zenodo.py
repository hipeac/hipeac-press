from io import BytesIO
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


pdfs = [
    {
        "folder": "00 Introduction and recommendations",
        "section_title": "",
        "articles": [
            ("", "HiPEAC_Vision_2024_Ratinoale_Introduction_v1__EIL.pdf"),
        ],
    },
    {
        "folder": "01 The next computing paradigm (NCP)",
        "section_title": "Next computing paradigm (NCP)",
        "articles": [
            ("Introduction", "The New Computing Paradigm - Intro Definitive__EIL_KDBOK.pdf"),
            ("The Spatial Web", "The New Computing Paradigm - Spatial Web__EIL.pdf"),
            ("Bridging CPS communities", "2024_Bridging_CPS_communities_v0.8_designationUpdate KDBOK.pdf"),
            ("Societal aspects", "New Computing Paradigm, Societal Aspects THG_revMG_updated_231223__EIL_KDBOK.pdf"),
        ],
    },
    {
        "folder": "02 Artificial intelligence",
        "section_title": "Artificial intelligence",
        "articles": [
            ("Introduction", "AI_intro_231219-5 KDB__EIL.pdf"),
            ("AI everywhere", "AI_everywhere in 2023_231215-6 KDBOK_final__EIL.pdf"),
            ("AI assisted software engineering", "NESSI - AISE HIPEAC RC2 KDB final__EIL_KDBOK.pdf"),
            ("AI for EDA", "Challenges in EDA_V2_10Jan2024_LZ__EIL.pdf"),
            ("SWOT", "Vision24_AI_swot_240108-2__EIL_KDBOK.pdf"),
        ],
    },
    {
        "folder": "03 New hardware",
        "section_title": "New hardware",
        "articles": [
            ("Introduction", "HiPEAC-7 Hardware Section Intro__EIL_KDBOK.pdf"),
            (
                "Heterogeneous and domain-specific acceleration",
                "Here to stay specialized and heterogeneous computing__EIL_KDBOK.pdf",
            ),
            ("Quantum computing", "Quantum Qubits and pieces__EIL_KDBOK.pdf"),
            (
                "Open source hardware",
                "Open Source Hardware and RISC-V an exciting opportunity for Europe__EIL_KDBOK.pdf",
            ),
        ],
    },
    {
        "folder": "04 Cybersecurity",
        "section_title": "Cybersecurity",
        "articles": [
            (
                "Introduction",
                "2023-1208_HiPEAC_Vision_2024_NCP_cybersecurity_chapter_introduction_Zendra_Coppens__EIL_KDBOK.pdf",
            ),
            ("NCP cybersecurity", "2023-1205_HiPEAC_Vision_2024_NCP-Cybersecurity_Zendra_Coppens__EIL_KDBOK.pdf"),
            ("NCP privacy", "2023-1129_HiPEAC_Vision_2024_NCP-Privacy_Coppens_Zendra__EIL_KDBOK.pdf"),
            ("Browser tracking", "2023-1207_HiPEAC_Vision_2024_NCP-Browser_Tracking_Rudametkin_Zendra__EIL_KDBOK.pdf"),
            ("DLT and IPFS for the NCP", "2023-1211_HiPEAC_Vision_2024_NCP-DLT_Bertin_v2_revOZ__EIL_KDBOK.pdf"),
            (
                "Integrity of hardware supply chains",
                "2023-1123_HiPEAC_vision_HW-SEC_Integrity-at-Every-Link-Trustworthy-Supply-Chains__EIL_KDBOK.pdf",
            ),
            (
                "Microarchitectures as root of trust",
                "2023-1121_HiPEAC_vision_HW-SEC_Microarchitectures-Root-of-Trust-Formal-Analysis_Kunz-Stoffel_V2__EIL_KDBOK.pdf",
            ),
        ],
    },
    {
        "folder": "05 Sustainability",
        "section_title": "Sustainability",
        "articles": [
            ("Introduction", "Sustainability 01 Introduction__EIL_KDBOK.pdf"),
            ("What does it mean to be sustainable?", "What does it mean to be sustainable_KDB_PB__EIL_KDBOK.pdf"),
            (
                "Sustainable materials and production",
                "Sustainability 03 Sustainable materials and production final version__EIL_KDBOK_Lars.pdf",
            ),
            (
                "Sustainable computer architecture",
                "Sustainability 04 Sustainability Computer Architecture LE__EIL_KDBOK.pdf",
            ),
        ],
    },
]


def get_header(section_title: str, article_title: str, num: int) -> PdfReader:
    b = BytesIO()
    c = canvas.Canvas(b, pagesize=A4)
    pdfmetrics.registerFont(TTFont("Garamond", "./public/fonts/EBGaramond-Regular.ttf"))
    c.setFont("Garamond", 7)
    top_position = A4[1] - (1.25 * cm)
    bottom_position = A4[1] - (28.45 * cm)
    left_margin = 2.56 * cm
    right_margin = A4[0] - (2.56 * cm)

    if num % 2 == 0:
        c.drawRightString(right_margin, top_position, "HiPEAC Vision 2024 rationale")
        c.drawRightString(right_margin, bottom_position, article_title)
        c.drawString(left_margin, bottom_position, str(num))
    else:
        c.drawString(left_margin, bottom_position, section_title)
        c.drawRightString(right_margin, bottom_position, str(num))

    c.save()
    b.seek(0)
    return PdfReader(b)


def add_pages_to_pdfs():
    # gop through the folder alnd make a list of all pdf files, as filename: path

    vision_folder = Path("/Users/eillarra/Nextcloud/hipeac/Vision/2024/HiPEAC_Vision_24/02 Articles/Stage 5 - Print")
    pdf_files = {}

    for pdf_file in vision_folder.glob("**/*.pdf"):
        pdf_files[pdf_file.name] = pdf_file

    for pdf in pdfs:
        for article in pdf["articles"]:
            writer = PdfWriter()
            i = 0
            pdf_file = pdf_files[article[1]]
            pdf_reader = PdfReader(pdf_file)

            print(i + 1, article[0])

            for page in pdf_reader.pages:
                i += 1
                page.merge_page(get_header(pdf["section_title"], article[0], i).pages[0], True)
                writer.add_page(page)
            if len(pdf_reader.pages) % 2 == 1:
                i += 1
                blank_page = PageObject.create_blank_page(pdf_reader)
                blank_page.merge_page(get_header(pdf["section_title"], article[0], i).pages[0], True)
                writer.add_page(blank_page)

            with BytesIO() as bytes_stream:
                writer.remove_links()
                writer.write(bytes_stream)
                bytes_stream.seek(0)

                with open(pdf_file.name, "wb") as f:
                    f.write(bytes_stream.read())


add_pages_to_pdfs()
