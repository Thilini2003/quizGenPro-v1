from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from typing import List
from models.schemas import MCQQuestion

class PDFCreator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        # Question style
        self.question_style = ParagraphStyle(
            'Question',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Option style
        self.option_style = ParagraphStyle(
            'Option',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=5
        )
        
        # Answer style
        self.answer_style = ParagraphStyle(
            'Answer',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=5,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )
        
        # Explanation style
        self.explanation_style = ParagraphStyle(
            'Explanation',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=15,
            textColor=colors.darkblue
        )
    
    def create_mcq_pdf(self, questions: List[MCQQuestion], output_path: str, source: str = ""):
        """Create a PDF with MCQ questions and answers"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Add title
        title = Paragraph("Multiple Choice Questions", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add metadata
        if source:
            source_para = Paragraph(f"<b>Source:</b> {source}", self.styles['Normal'])
            story.append(source_para)
        
        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_para = Paragraph(f"<b>Generated:</b> {generated_time}", self.styles['Normal'])
        story.append(time_para)
        
        total_questions = len(questions)
        total_para = Paragraph(f"<b>Total Questions:</b> {total_questions}", self.styles['Normal'])
        story.append(total_para)
        story.append(Spacer(1, 20))
        
        # Add questions section
        questions_title = Paragraph("Questions", self.styles['Heading2'])
        story.append(questions_title)
        story.append(Spacer(1, 12))
        
        # Add each question
        for i, mcq in enumerate(questions, 1):
            # Question number and text
            q_text = f"<b>Question {i}:</b> {mcq.question}"
            question_para = Paragraph(q_text, self.question_style)
            story.append(question_para)
            
            # Options
            for option in mcq.options:
                option_para = Paragraph(option, self.option_style)
                story.append(option_para)
            
            story.append(Spacer(1, 10))
        
        # Add page break before answers
        story.append(PageBreak())
        
        # Add answers section
        answers_title = Paragraph("Answer Key", self.styles['Heading2'])
        story.append(answers_title)
        story.append(Spacer(1, 12))
        
        # Add answers
        for i, mcq in enumerate(questions, 1):
            # Question number
            q_ref = Paragraph(f"<b>Question {i}:</b>", self.answer_style)
            story.append(q_ref)
            
            # Correct answer
            answer_text = f"<b>Correct Answer:</b> {mcq.correct_answer}"
            answer_para = Paragraph(answer_text, self.answer_style)
            story.append(answer_para)
            
            # Explanation
            if mcq.explanation:
                explanation_text = f"<b>Explanation:</b> {mcq.explanation}"
                explanation_para = Paragraph(explanation_text, self.explanation_style)
                story.append(explanation_para)
            
            story.append(Spacer(1, 15))
        
        # Build PDF
        doc.build(story)
    
    def create_questions_only_pdf(self, questions: List[MCQQuestion], output_path: str, source: str = ""):
        """Create a PDF with only questions (no answers) for testing purposes"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Add title
        title = Paragraph("Multiple Choice Questions - Test Paper", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add metadata
        if source:
            source_para = Paragraph(f"<b>Source:</b> {source}", self.styles['Normal'])
            story.append(source_para)
        
        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_para = Paragraph(f"<b>Generated:</b> {generated_time}", self.styles['Normal'])
        story.append(time_para)
        
        total_questions = len(questions)
        total_para = Paragraph(f"<b>Total Questions:</b> {total_questions}", self.styles['Normal'])
        story.append(total_para)
        story.append(Spacer(1, 20))
        
        # Instructions
        instructions = Paragraph(
            "<b>Instructions:</b> Choose the best answer for each question. Mark your answer clearly.",
            self.styles['Normal']
        )
        story.append(instructions)
        story.append(Spacer(1, 20))
        
        # Add each question
        for i, mcq in enumerate(questions, 1):
            # Question number and text
            q_text = f"<b>{i}.</b> {mcq.question}"
            question_para = Paragraph(q_text, self.question_style)
            story.append(question_para)
            
            # Options
            for option in mcq.options:
                option_para = Paragraph(option, self.option_style)
                story.append(option_para)
            
            story.append(Spacer(1, 15))
        
        # Build PDF
        doc.build(story)