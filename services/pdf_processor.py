import PyPDF2
import re

class PDFProcessor:
    def __init__(self):
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            # Clean up the text
            text = self._clean_text(text)
            return text
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess extracted text"""
        # Remove extra whitespaces and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        # Remove very short lines (likely formatting artifacts)
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return ' '.join(cleaned_lines).strip()
    
    def get_text_summary(self, text: str, max_length: int = 500) -> str:
        """Get a summary of the text for preview purposes"""
        if len(text) <= max_length:
            return text
        
        # Try to break at sentence boundaries
        sentences = text.split('.')
        summary = ""
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + "."
            else:
                break
        
        return summary.strip() + "..." if summary else text[:max_length] + "..."