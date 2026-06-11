import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "career.ai.system@gmail.com")

def generate_pdf_report(user_name, career_match_results, resume_analysis, roadmap):
    """
    Generates a structured career recommendation report as a PDF.
    If reportlab is not installed, creates a formatted HTML/Text report as fallback.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.join(base_dir, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    filename = f"career_report_{user_name.lower().replace(' ', '_')}.pdf"
    pdf_path = os.path.join(uploads_dir, filename)
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        story = []
        styles = getSampleStyleSheet()
        
        # Define premium text styles
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'), # Indigo-600
            spaceAfter=15
        )
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'), # Gray-500
            spaceAfter=25
        )
        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1E1B4B'), # Dark Indigo
            spaceBefore=15,
            spaceAfter=10
        )
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            textColor=colors.HexColor('#374151'), # Gray-700
            spaceAfter=10
        )
        
        # Add contents
        story.append(Paragraph("AI Career Development Platform - Report", title_style))
        story.append(Paragraph(f"Generated for: {user_name} | Platform: CareerAI System", subtitle_style))
        story.append(Spacer(1, 10))
        
        # 1. Career Matches
        story.append(Paragraph("1. AI Career Recommendations", heading_style))
        career_text = "Based on our machine learning evaluation, here are your top matching career paths:"
        story.append(Paragraph(career_text, body_style))
        
        table_data = [["Career Path", "Match Percentage"]]
        for res in career_match_results[:5]:
            table_data.append([res.get("career"), f"{res.get('match_percentage')}%"])
            
        t = Table(table_data, colWidths=[300, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0E7FF')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#4F46E5')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # 2. Resume Assessment
        story.append(Paragraph("2. Resume Analysis", heading_style))
        ats_score = resume_analysis.get("ats_score", 0)
        strength = resume_analysis.get("resume_strength", "Weak")
        story.append(Paragraph(f"<b>ATS Compatibility Score:</b> {ats_score}/100", body_style))
        story.append(Paragraph(f"<b>Resume Strength:</b> {strength}", body_style))
        
        extracted_skills = ", ".join(resume_analysis.get("extracted_skills", [])) or "None detected"
        missing_skills = ", ".join(resume_analysis.get("missing_skills", [])) or "None (perfect fit!)"
        
        story.append(Paragraph(f"<b>Extracted Skills:</b> {extracted_skills}", body_style))
        story.append(Paragraph(f"<b>Missing Recommended Skills:</b> {missing_skills}", body_style))
        story.append(Spacer(1, 20))
        
        # 3. Roadmap Summary
        story.append(Paragraph("3. Learning Roadmap Steps", heading_style))
        story.append(Paragraph(f"Target Career: {roadmap.get('career_path', 'General Development')}", body_style))
        story.append(Paragraph(f"Overall Course Progress: {roadmap.get('overall_progress', 0)}%", body_style))
        
        roadmap_data = [["Stage", "Milestone", "Skills to Build"]]
        for step in roadmap.get("steps", []):
            roadmap_data.append([
                step.get("stage"), 
                step.get("title"), 
                ", ".join(step.get("missing_skills", [])) or "Completed"
            ])
            
        t2 = Table(roadmap_data, colWidths=[80, 180, 190])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#374151')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E5E7EB'))
        ]))
        story.append(t2)
        
        doc.build(story)
        print(f"PDF report generated at {pdf_path}")
        return pdf_path, filename
        
    except ImportError:
        print("ReportLab package not found. Generating fallback HTML report file...")
        # Fallback HTML file representing PDF
        fallback_filename = f"career_report_{user_name.lower().replace(' ', '_')}.html"
        fallback_path = os.path.join(uploads_dir, fallback_filename)
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #374151; padding: 30px; }}
                h1 {{ color: #4F46E5; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }}
                h2 {{ color: #1E1B4B; margin-top: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th, td {{ border: 1px solid #E5E7EB; padding: 10px; text-align: left; }}
                th {{ background-color: #F3F4F6; }}
                .highlight {{ font-weight: bold; color: #4F46E5; }}
            </style>
        </head>
        <body>
            <h1>AI Career Recommendation & Development Report</h1>
            <p>Generated for: <strong>{user_name}</strong></p>
            
            <h2>1. Top Recommendations</h2>
            <table>
                <tr><th>Career Path</th><th>Match Percentage</th></tr>
                {"".join(f"<tr><td>{r.get('career')}</td><td class='highlight'>{r.get('match_percentage')}%</td></tr>" for r in career_match_results[:5])}
            </table>
            
            <h2>2. Resume & ATS Evaluation</h2>
            <p><strong>ATS Compatibility Score:</strong> {resume_analysis.get('ats_score')}/100</p>
            <p><strong>Strength:</strong> {resume_analysis.get('resume_strength')}</p>
            <p><strong>Missing Skills identified:</strong> {", ".join(resume_analysis.get('missing_skills', [])) or 'None'}</p>
            
            <h2>3. Targeted Roadmap</h2>
            <p>Recommended Roadmap: {roadmap.get('career_path')}</p>
            <p>Overall Skill Level Progress: {roadmap.get('overall_progress')}%</p>
            <ul>
                {"".join(f"<li><strong>{s.get('stage')}: {s.get('title')}</strong> - Missing: {', '.join(s.get('missing_skills', [])) or 'None'}</li>" for s in roadmap.get('steps', []))}
            </ul>
        </body>
        </html>
        """
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Fallback HTML report file generated at {fallback_path}")
        return fallback_path, fallback_filename

def send_career_email(to_email, subject, body_html, attachment_path=None):
    """
    Sends email containing career analysis.
    Logs email details directly to console if SMTP details are missing.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("\n=== [DEBUG EMAIL SYSTEM] ===")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body_html}")
        if attachment_path:
            print(f"Attachment file attached: {attachment_path}")
        print("============================\n")
        return True
        
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        
        # Attach html body
        msg.attach(MIMEText(body_html, 'html'))
        
        # Attach PDF report if present
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(attach)
                
        # Connect and send
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Email successfully sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"SMTP Email delivery failed ({e}). Logging body instead:")
        print(f"Email content: {body_html}")
        return False
