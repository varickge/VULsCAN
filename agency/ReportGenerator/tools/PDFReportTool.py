import os

from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json
import traceback
from markdown2 import markdown

from agency.threadLocal import thread_local_data
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

from dotenv import load_dotenv
load_dotenv()

class PDFReportTool(BaseTool):
    """
    This utility facilitates the creation of PDF documents with alternating text and images.
    """

    title: str = Field(..., description="Title of the PDF document.")
    text: List[str] = Field(..., description="List of text paragraphs to be included in the PDF.")
    output_file: str = Field(..., description="Output file path for the generated PDF with .pdf extension.", examples=["file.pdf", "file123.pdf"])

    def markdown_to_html(self, markdown_text):
        """
        Convert Markdown text to HTML.
        """
        return markdown(markdown_text)
    
    def footer(self, canvas, doc):
        """
        Add a footer to each page.
        """
        canvas.saveState()
        footer_text = "(c) 2024, Authored by VULsCAN"
        canvas.setFont('Times-Roman', 10)
        canvas.setFillColor(colors.grey)
        # Adjust the position to the bottom center of the page
        canvas.drawCentredString(doc.pagesize[0] / 2, 15, footer_text)
        canvas.restoreState()


    def run(self):
        """
        Generate a PDF document with alternating text and images.
        """
        try:
            os.makedirs('./reports', exist_ok=True)
            self.output_file = self.output_file.split('/')[-1]
            print(f"Name: {self.output_file}")
            doc = SimpleDocTemplate(f'./reports/{self.output_file}', pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='IEEE_Title', fontSize=14, leading=18, fontName='Times-Bold', alignment=TA_CENTER, spaceAfter=20))
            styles.add(ParagraphStyle(name='IEEE_Body', fontSize=11, leading=14, fontName='Times-Roman', spaceAfter=12, alignment=TA_JUSTIFY))

            flowables = []

            # Add title
            title_para = Paragraph(self.title, styles['IEEE_Title'])
            flowables.append(title_para)

            # image_paths = get_img_paths()
            for i, paragraph_text in enumerate(self.text):
                html_text = self.markdown_to_html(paragraph_text)
                para = Paragraph(html_text.replace("\n", "<br/>"), styles['IEEE_Body'])
                flowables.append(para)
                flowables.append(Spacer(1, 12))


            doc.build(flowables, onLaterPages=self.footer, onFirstPage=self.footer)
            thread_local_data.report_path = f'./reports/{self.output_file}'
            print(f"PDF generated successfully: {thread_local_data.report_path}")
            return "PDF generated successfully."

        except Exception as e:
            print(f"Error occurred: {traceback.format_exc()}")
            return f"Error occurred: {traceback.format_exc()}"


if __name__ == "__main__":
    tool = PDFReportTool(
        report_content="this is a test via api",
    )
    print(tool.run())