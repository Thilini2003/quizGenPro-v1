# MCQ Generator

A powerful web application that generates Multiple Choice Questions (MCQs) from PDF documents or topics using the Groq API and FastAPI. The generated questions can be downloaded as professionally formatted PDF files.

## Features

- 📄 **PDF Upload**: Extract text from PDF documents and generate MCQs
- 🎯 **Topic-Based Generation**: Generate MCQs from any topic with optional subtopics
- 🎚️ **Difficulty Levels**: Choose from Easy, Medium, or Hard difficulty levels
- 📊 **Customizable**: Set the number of questions (1-50)
- 📁 **PDF Export**: Download generated MCQs as formatted PDF files
- 🎨 **Modern UI**: Clean, responsive web interface
- 🚀 **Fast Processing**: Powered by Groq's high-speed AI models

## Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Model**: Groq API (Llama 3 70B)
- **PDF Processing**: PyPDF2, ReportLab
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Uvicorn ASGI server

## Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (get it from [Groq Console](https://console.groq.com/))

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd mcq-generator
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Step 5: Create Required Directories

```bash
mkdir uploads outputs static
```

### Step 6: Create Directory Structure

Your project structure should look like this:

```
mcq-generator/
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── README.md
├── models/
│   ├── __init__.py
│   └── schemas.py
├── services/
│   ├── __init__.py
│   ├── pdf_processor.py
│   ├── mcq_generator.py
│   └── pdf_creator.py
├── static/
│   └── index.html
├── uploads/
└── outputs/
```

## Usage

### Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

### Using the Web Interface

#### Method 1: Upload PDF
1. Click on the "Upload PDF" tab
2. Select or drag-and-drop a PDF file
3. Set the number of questions (1-50)
4. Choose difficulty level (Easy/Medium/Hard)
5. Click "Generate MCQs from PDF"
6. Download the generated PDF

#### Method 2: Enter Topic
1. Click on the "Enter Topic" tab
2. Enter your main topic (e.g., "World War II", "Photosynthesis")
3. Optionally add subtopics for more focused questions
4. Set the number of questions and difficulty level
5. Click "Generate MCQs from Topic"
6. Download the generated PDF

### API Endpoints

#### Generate MCQs from PDF
```bash
POST /generate-from-pdf
Content-Type: multipart/form-data

Parameters:
- file: PDF file
- num_questions: integer (1-50)
- difficulty: string (easy|medium|hard)
```

#### Generate MCQs from Topic
```bash
POST /generate-from-topic
Content-Type: application/json

Body:
{
  "topic": "Machine Learning",
  "num_questions": 10,
  "difficulty": "medium",
  "subtopics": ["Neural Networks", "Deep Learning"]
}
```

#### Download Generated PDF
```bash
GET /download/{filename}
```

#### Health Check
```bash
GET /health
```

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_MODEL`: AI model to use (default: "llama3-70b-8192")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)

### Supported Models

The application supports various Groq models:
- `llama3-70b-8192` (default)
- `llama3-8b-8192`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

## Customization

### Adding New Difficulty Levels

Edit `services/mcq_generator.py` and update the difficulty guidelines in the prompt templates.

### Changing PDF Layout

Modify `services/pdf_creator.py` to customize the PDF output format, colors, and styling.

### Adding New Features

- Add new endpoints in `main.py`
- Create new service classes in the `services/` directory
- Update the UI in `static/index.html`

## Troubleshooting

### Common Issues

1. **"Error generating MCQs"**
   - Check your Groq API key is valid
   - Ensure you have internet connection
   - Verify the API key has sufficient credits

2. **"Could not extract text from PDF"**
   - Ensure the PDF contains extractable text (not just images)
   - Try with a different PDF file
   - Check if the PDF is not password-protected

3. **"File not found" when downloading**
   - Ensure the `outputs/` directory exists
   - Check file permissions
   - Try generating MCQs again

### Performance Tips

- Use smaller PDF files for faster processing
- Limit the number of questions for quicker generation
- Consider using lighter models for faster responses

## Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

1. **Using Uvicorn directly:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. **Using Docker:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Using cloud platforms:**
   - Deploy to Heroku, Railway, or any cloud platform that supports Python
   - Set environment variables in your deployment platform
   - Ensure all dependencies are included

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Groq](https://groq.com/) for providing fast AI inference
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [ReportLab](https://www.reportlab.com/) for PDF generation capabilities

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Look at existing issues in the repository
3. Create a new issue with detailed information

## Changelog

### Version 1.0.0
- Initial release
- PDF upload and text extraction
- Topic-based MCQ generation
- PDF export functionality
- Web interface with responsive design
- Support for multiple difficulty levels
- Customizable question count