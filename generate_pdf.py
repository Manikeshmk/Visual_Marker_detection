#!/usr/bin/env python3
"""
Convert TECHNICAL_APPROACH.md to PDF
Requires: pip install reportlab markdown pypdf2
"""

import os
import sys
import subprocess
from pathlib import Path

def generate_pdf_with_pandoc(md_file, pdf_file):
    """Generate PDF using Pandoc (recommended)"""
    try:
        cmd = [
            'pandoc',
            md_file,
            '-f', 'markdown',
            '-t', 'pdf',
            '-o', pdf_file,
            '--pdf-engine=xelatex',  # For better font support
            '-V', 'mainfont:Arial',
            '-V', 'geometry:margin=1in',
            '-V', 'pagestyle:headings',
            '--table-of-contents',
            '--number-sections'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ PDF generated successfully: {pdf_file}")
            return True
        else:
            print(f"✗ Pandoc error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("✗ Pandoc not found. Install with: pip install pandoc")
        return False

def generate_pdf_with_reportlab(md_file, pdf_file):
    """Generate PDF using ReportLab (fallback)"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib import colors
        import markdown
        from html.parser import HTMLParser
        
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content)
        
        # Create PDF
        pdf = SimpleDocTemplate(pdf_file, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Parse markdown structure
        lines = md_content.split('\n')
        
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                story.append(Paragraph(title, title_style))
                story.append(Spacer(1, 0.3*inch))
            elif line.startswith('## '):
                heading = line[3:].strip()
                story.append(Paragraph(heading, heading_style))
                story.append(Spacer(1, 0.1*inch))
            elif line.startswith('### '):
                subheading = line[4:].strip()
                story.append(Paragraph(f"<b>{subheading}</b>", styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
            elif line.strip() and not line.startswith('|') and not line.startswith('-'):
                story.append(Paragraph(line.strip(), styles['BodyText']))
                story.append(Spacer(1, 0.05*inch))
            elif line.strip() == '':
                story.append(Spacer(1, 0.1*inch))
        
        pdf.build(story)
        print(f"✓ PDF generated with ReportLab: {pdf_file}")
        return True
        
    except ImportError as e:
        print(f"✗ ReportLab not available: {e}")
        return False
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        return False

def generate_html_version(md_file, html_file):
    """Generate HTML version as fallback"""
    try:
        import markdown
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
        
        html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Visual Marker Detection - Technical Approach</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f5f5f5;
        }}
        h1, h2, h3, h4 {{
            color: #1a1a1a;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }}
        h1 {{
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        pre {{
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 12px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Courier New', monospace;
            background-color: #f0f0f0;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .checkmark {{
            color: green;
            font-weight: bold;
        }}
        @media print {{
            body {{
                max-width: 100%;
                background-color: white;
            }}
            page {{
                margin: 0.5in;
            }}
        }}
    </style>
</head>
<body>
{html_content}
<hr>
<footer>
    <p><em>Generated on: May 2026</em></p>
    <p>Print or save this HTML to PDF from your browser using Ctrl+P (Cmd+P on Mac)</p>
</footer>
</body>
</html>"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        
        print(f"✓ HTML version generated: {html_file}")
        print(f"  Open in browser and use File→Print→Save as PDF")
        return True
        
    except ImportError:
        print("✗ Markdown module not found: pip install markdown")
        return False
    except Exception as e:
        print(f"✗ Error generating HTML: {e}")
        return False

def main():
    """Main conversion function"""
    md_file = "TECHNICAL_APPROACH.md"
    pdf_file = "TECHNICAL_APPROACH.pdf"
    html_file = "TECHNICAL_APPROACH.html"
    
    if not Path(md_file).exists():
        print(f"✗ File not found: {md_file}")
        sys.exit(1)
    
    print("Converting TECHNICAL_APPROACH.md to PDF...")
    print()
    
    # Try Pandoc first (best quality)
    if generate_pdf_with_pandoc(md_file, pdf_file):
        sys.exit(0)
    
    print()
    print("Pandoc not available, trying ReportLab...")
    print()
    
    # Try ReportLab
    if generate_pdf_with_reportlab(md_file, pdf_file):
        sys.exit(0)
    
    print()
    print("ReportLab not available, generating HTML version instead...")
    print()
    
    # Generate HTML version
    if generate_html_version(md_file, html_file):
        print()
        print("━" * 60)
        print("PDF Generation Instructions:")
        print("━" * 60)
        print(f"1. Open '{html_file}' in your web browser")
        print(f"2. Press Ctrl+P (or Cmd+P on Mac) to open Print dialog")
        print(f"3. Select 'Save as PDF' as printer")
        print(f"4. Click 'Save' to generate PDF")
        print()
        print("This will create a professional PDF version of the")
        print("technical documentation.")
        print("━" * 60)
        sys.exit(0)
    
    print("✗ Could not generate PDF or HTML version")
    sys.exit(1)

if __name__ == "__main__":
    main()
