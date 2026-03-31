import json
import os
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
    # On réduit légèrement le leading (interligne) pour gagner de la place
    style_left = ParagraphStyle('Left', parent=styles['Normal'], fontName=font_name_left, fontSize=10, leading=11)
    style_right = ParagraphStyle('Right', parent=styles['Normal'], fontName=font_name_right, fontSize=10, leading=11, alignment=TA_RIGHT)
    
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

    # --- ACTION 1 : Marges réduites de 36 à 24 pour gagner beaucoup de hauteur ---
    doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=24, leftMargin=24, topMargin=24, bottomMargin=24)
    story = []
    styles = getSampleStyleSheet()

    # --- ACTION 2 : Styles resserrés (leading réduit) ---
    style_name = ParagraphStyle('Name', parent=styles['Normal'], fontName='Times-Roman', fontSize=16, leading=18, alignment=TA_CENTER, spaceAfter=2)
    style_contact = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=12, alignment=TA_CENTER)
    
    # Section resserrée
    style_section = ParagraphStyle('Section', parent=styles['Normal'], fontName='Times-Bold', fontSize=10, leading=11, spaceBefore=6, spaceAfter=1)
    
    style_summary = ParagraphStyle('Summary', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=12, alignment=TA_JUSTIFY, spaceAfter=4)
    style_bullet = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=12, leftIndent=12, firstLineIndent=-12, spaceAfter=1)
    style_sub_bullet = ParagraphStyle('SubBullet', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=12, leftIndent=30, firstLineIndent=-12, spaceAfter=1)
    style_skill = ParagraphStyle('Skill', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=12, spaceAfter=1)

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
    story.append(Spacer(1, 10))
    # --- SUMMARY ---
    if "summary" in data:
        story.append(Paragraph(clean_text(data["summary"]), style_summary))

    # --- EDUCATION ---
    if "education" in data:
        story.append(Paragraph("<b>EDUCATION</b>", style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=3))
        
        for edu in data["education"]:
            add_split_row(story, edu.get('university', ''), edu.get('location', ''))
            add_split_row(story, f"<i>{edu.get('degree', '')}</i>", edu.get('date', ''), 'Times-Roman', 'Times-Roman')
            
            for bullet in edu.get('bullets', []):
                story.append(Paragraph(f"&bull; {clean_text(bullet)}", style_bullet))
            story.append(Spacer(1, 3)) # Espace réduit

    # --- EXPERIENCE ---
    if "experience" in data:
        story.append(Paragraph("<b>WORK & LEADERSHIP EXPERIENCE</b>", style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=3))
        
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
            story.append(Spacer(1, 4)) # Espace réduit entre expériences

    # --- SKILLS & INTERESTS ---
    if "skills" in data:
        story.append(Paragraph("<b>SKILLS, ACTIVITIES & INTERESTS</b>", style_section))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=3))
        
        skills = data["skills"]
        for key, value in skills.items():
            story.append(Paragraph(f"<b>{clean_text(key)}:</b> {clean_text(value)}", style_skill))

    doc.build(story)
    print(f"\nSuccès ! Le fichier compact sur une page a été généré : {pdf_file}")

if __name__ == "__main__":
    json_input = input("Entrez le nom du fichier JSON en entrée : ")
    pdf_output = input("Entrez le nom du fichier PDF à générer : ")
    
    if not json_input.endswith('.json'): json_input += '.json'
    if not pdf_output.endswith('.pdf'): pdf_output += '.pdf'
    
    generate_pdf(json_input, pdf_output)