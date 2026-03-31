import json
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

def clean_text(text):
    if not isinstance(text, str):
        return text
    text = text.replace("M&A;", "M&amp;A").replace("M&A", "M&amp;A")
    text = text.replace("€", "EUR ")
    return text

def add_split_row(story, left_text, right_text, font_name_left='Times-Bold', font_name_right='Times-Bold'):
    styles = getSampleStyleSheet()
    # Interligne plus aéré
    style_left = ParagraphStyle('Left', parent=styles['Normal'], fontName=font_name_left, fontSize=10, leading=13)
    style_right = ParagraphStyle('Right', parent=styles['Normal'], fontName=font_name_right, fontSize=10, leading=13, alignment=TA_RIGHT)
    
    t = Table([
        [Paragraph(clean_text(left_text), style_left), Paragraph(clean_text(right_text), style_right)]
    ], colWidths=['75%', '25%'])
    
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0), # Collé
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t)

def generate_pdf(json_file, pdf_file):
    if not os.path.exists(json_file):
        print(f"Erreur : Le fichier {json_file} n'existe pas.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Charger personal.json si disponible et fusionner avec data
    personal_file = os.path.join(os.path.dirname(json_file), 'personal.json')
    if os.path.exists(personal_file):
        with open(personal_file, 'r', encoding='utf-8') as f:
            personal_data = json.load(f)
            # Fusionner : personal.json comme base, écrasé par data si personal_info existe
            if 'personal_info' not in data and 'personal_info' in personal_data:
                data['personal_info'] = personal_data['personal_info']

    # Marges optimisées pour tenir sur une page
    doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()

    # Styles optimisés : aéré mais compact pour tenir sur une page
    style_name = ParagraphStyle('Name', parent=styles['Normal'], fontName='Times-Roman', fontSize=16, leading=19, alignment=TA_CENTER, spaceAfter=3)
    style_contact = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=13, alignment=TA_CENTER)
    
    # Section équilibrée
    style_section = ParagraphStyle('Section', parent=styles['Normal'], fontName='Times-Bold', fontSize=10, leading=12, spaceBefore=8, spaceAfter=2)
    
    style_summary = ParagraphStyle('Summary', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=13, alignment=TA_JUSTIFY, spaceAfter=5)
    style_bullet = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=13, leftIndent=12, firstLineIndent=-12, spaceAfter=1.5)
    style_sub_bullet = ParagraphStyle('SubBullet', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=13, leftIndent=30, firstLineIndent=-12, spaceAfter=1.5)
    style_skill = ParagraphStyle('Skill', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=13, spaceAfter=1.5)

    # --- EN-TÊTE ---
    personal = data.get("personal_info", {})
    name = personal.get('name', '')
    contact = personal.get('contact', '')
    linkedin_display = personal.get('linkedin_display', '')
    linkedin_url = personal.get('linkedin_url', '')
    
    story.append(Paragraph(f"<b>{name}</b>", style_name))
    
    # Ajouter le lien LinkedIn seulement s'il est fourni
    if linkedin_url:
        contact_paragraph = f"{contact} | <a href='{linkedin_url}'><u>{linkedin_display}</u></a>"
    else:
        contact_paragraph = contact
    
    story.append(Paragraph(contact_paragraph, style_contact))
    story.append(Spacer(1, 8))
    # --- SUMMARY ---
    if "summary" in data:
        story.append(Paragraph(clean_text(data["summary"]), style_summary))

    # --- EDUCATION ---
    if "education" in data:
        story.append(Paragraph("<b>EDUCATION</b>", style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=4))
        
        for edu in data["education"]:
            add_split_row(story, edu.get('university', ''), edu.get('location', ''))
            add_split_row(story, f"<i>{edu.get('degree', '')}</i>", edu.get('date', ''), 'Times-Roman', 'Times-Roman')
            
            for bullet in edu.get('bullets', []):
                story.append(Paragraph(f"&bull; {clean_text(bullet)}", style_bullet))
            story.append(Spacer(1, 4))

    # --- EXPERIENCE ---
    if "experience" in data:
        story.append(Paragraph("<b>WORK & LEADERSHIP EXPERIENCE</b>", style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=4))
        
        for exp in data["experience"]:
            add_split_row(story, exp.get('company', ''), exp.get('location', ''))
            add_split_row(story, f"<i>{exp.get('title', '')}</i>", exp.get('date', ''), 'Times-Roman', 'Times-Roman')
            
            for item in exp.get('bullets', []):
                if isinstance(item, str):
                    story.append(Paragraph(f"&bull; {clean_text(item)}", style_bullet))
                elif isinstance(item, dict):
                    story.append(Paragraph(f"&bull; {clean_text(item.get('main', ''))}", style_bullet))
                    for sub in item.get('sub_bullets', []):
                        story.append(Paragraph(f"&#9702; {clean_text(sub)}", style_sub_bullet))
            story.append(Spacer(1, 5))

    # --- SKILLS & INTERESTS ---
    if "skills" in data:
        story.append(Paragraph("<b>SKILLS, ACTIVITIES & INTERESTS</b>", style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=4))
        
        skills = data["skills"]
        for key, value in skills.items():
            story.append(Paragraph(f"<b>{clean_text(key)}:</b> {clean_text(value)}", style_skill))

    # Vérifier que le CV tient sur une page avant de sauvegarder
    buffer = BytesIO()
    test_doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    
    # Créer une copie du story pour le test (car build() consomme le story)
    from copy import deepcopy
    test_story = deepcopy(story)
    test_doc.build(test_story)
    
    # Compter le nombre de pages générées
    num_pages = test_doc.page
    
    if num_pages > 1:
        print(f"\n❌ ERREUR : Le CV généré fait {num_pages} pages. Il doit tenir sur UNE SEULE page.")
        print("Veuillez réduire le contenu du fichier JSON (moins de bullets, texte plus court, etc.)")
        return False
    
    # Si on tient sur une page, générer le vrai PDF avec le story original
    doc.build(story)
    print(f"\n✓ Succès ! Le CV tient sur une page : {pdf_file}")
    return True

if __name__ == "__main__":
    json_input = input("Entrez le nom du fichier JSON en entrée : ")
    pdf_output = "output/" + input("Entrez le nom du fichier PDF à générer : ")
    
    if not json_input.endswith('.json'): json_input += '.json'
    if not pdf_output.endswith('.pdf'): pdf_output += '.pdf'
    
    generate_pdf(json_input, pdf_output)