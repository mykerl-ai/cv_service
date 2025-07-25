# CV Tailoring Service

An AI-powered CV optimization service that uses OpenAI to generate tailored CVs in PDF format. This service analyzes job descriptions and optimizes CVs to match specific job requirements.

## Features

- **CV Parsing**: Extract structured information from existing CV files (PDF, DOCX, TXT)
- **Job Analysis**: Analyze job descriptions to extract requirements and insights
- **CV Optimization**: Tailor CVs to match specific job requirements using AI
- **PDF Generation**: Generate professional PDF CVs with multiple template styles
- **From Scratch**: Create CVs from personal information without existing files
- **Detailed Analysis**: Get optimization scores, improvements, and skill gap analysis

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. **Clone or navigate to the CV writer service directory:**
   ```bash
   cd cv_writer_service
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

## Usage

### Command Line Interface

The main script provides a command-line interface for generating tailored CVs:

#### Basic Usage - Tailor Existing CV

```bash
python generate_tailored_cv.py \
  --cv-file path/to/your/cv.pdf \
  --job-description "Job description text here..." \
  --output tailored_cv.pdf \
  --template modern
```

#### Generate CV from Scratch

```bash
python generate_tailored_cv.py \
  --from-scratch \
  --personal-info sample_personal_info.json \
  --job-description "Job description text here..." \
  --output new_cv.pdf \
  --template professional
```

#### Command Line Options

- `--cv-file`: Path to input CV file (PDF, DOCX, TXT) - required for existing CV mode
- `--job-description`: Job description text - required
- `--output`: Output PDF file path - required
- `--template`: CV template style (modern, professional, creative) - default: modern
- `--api-key`: OpenAI API key (or set OPENAI_API_KEY env var)
- `--include-analysis`: Include detailed analysis in output
- `--from-scratch`: Generate CV from personal info instead of file
- `--personal-info`: JSON file with personal information (for from-scratch mode)

### Python API Usage

You can also use the service programmatically:

```python
import os
from generate_tailored_cv import CVTailoringService

# Initialize the service
api_key = os.getenv("OPENAI_API_KEY")
service = CVTailoringService(api_key)

# Tailor existing CV
results = service.generate_tailored_cv(
    cv_file_path="path/to/cv.pdf",
    job_description="Job description text...",
    output_path="tailored_cv.pdf",
    template_style="modern",
    include_analysis=True
)

# Generate CV from scratch
personal_info = {
    "full_name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1 (555) 123-4567",
    "location": "San Francisco, CA",
    "summary": "Experienced software engineer...",
    "technical_skills": ["Python", "JavaScript", "React"],
    "soft_skills": ["Leadership", "Communication"],
    "experience": [...],
    "education": [...]
}

results = service.generate_cv_from_scratch(
    personal_info=personal_info,
    job_description="Job description text...",
    output_path="new_cv.pdf",
    template_style="professional"
)
```

## Examples

### Example 1: Tailor Existing CV

```bash
# Using the sample job description
python generate_tailored_cv.py \
  --cv-file your_cv.pdf \
  --job-description "$(cat sample_job_description.txt)" \
  --output my_tailored_cv.pdf \
  --template modern \
  --include-analysis
```

### Example 2: Generate CV from Scratch

```bash
# Using the sample personal information
python generate_tailored_cv.py \
  --from-scratch \
  --personal-info sample_personal_info.json \
  --job-description "$(cat sample_job_description.txt)" \
  --output john_doe_cv.pdf \
  --template professional
```

### Example 3: Run Example Script

```bash
# Run the example usage script
python example_usage.py
```

## Input Formats

### Supported CV File Formats

- **PDF**: Portable Document Format
- **DOCX**: Microsoft Word Document
- **TXT**: Plain Text File

### Personal Information JSON Format (for from-scratch mode)

```json
{
  "full_name": "John Doe",
  "email": "john.doe@email.com",
  "phone": "+1 (555) 123-4567",
  "location": "San Francisco, CA",
  "linkedin": "linkedin.com/in/johndoe",
  "github": "github.com/johndoe",
  "portfolio": "johndoe.dev",
  "summary": "Professional summary...",
  "technical_skills": ["Python", "JavaScript", "React"],
  "soft_skills": ["Leadership", "Communication"],
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "start_date": "January 2022",
      "end_date": "Present",
      "description": ["Responsibility 1", "Responsibility 2"],
      "achievements": ["Achievement 1", "Achievement 2"]
    }
  ],
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Science",
      "field_of_study": "Computer Science",
      "graduation_date": "May 2020",
      "gpa": "3.8/4.0"
    }
  ]
}
```

## Output

The service generates:

1. **PDF CV**: A professionally formatted CV tailored to the job description
2. **Optimization Score**: Percentage match between CV and job requirements
3. **Improvements Made**: List of optimizations applied to the CV
4. **Skill Gaps**: Identified missing skills or experience
5. **Detailed Analysis**: (Optional) Comprehensive analysis of CV and job requirements

### Sample Output

```
✅ CV generated successfully!
📄 Output file: tailored_cv.pdf
📊 Optimization score: 87.5%
🎯 Job: Senior Software Engineer at TechInnovate Solutions
⏱️  Processing time: 45.23 seconds

🔧 Improvements made:
   • Professional summary optimized for job requirements
   • Added missing technical skills
   • Job descriptions enhanced with relevant keywords and achievements
   • Improved keyword distribution for ATS optimization

⚠️  Skill gaps identified:
   • Kubernetes
   • GraphQL

📋 Detailed Analysis:
   Required skills: Python, JavaScript, React, Node.js, AWS, Docker
   Preferred skills: GraphQL, Kubernetes, Machine Learning
   Experience level: Senior
```

## Template Styles

The service offers three CV template styles:

1. **Modern**: Clean and contemporary design with blue accent colors
   - Suitable for: Technology, startups, creative industries
   - Font: Helvetica

2. **Professional**: Traditional professional design with conservative styling
   - Suitable for: Finance, consulting, corporate
   - Font: Times-Roman

3. **Creative**: Bold and creative design with purple accent colors
   - Suitable for: Design, marketing, advertising
   - Font: Helvetica

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### File Size Limits

- Maximum CV file size: 10MB
- Supported formats: PDF, DOCX, DOC, TXT

## Error Handling

The service includes comprehensive error handling for:

- Invalid file formats
- Missing API keys
- File size limits
- Network connectivity issues
- OpenAI API errors

## Troubleshooting

### Common Issues

1. **"OpenAI API key not configured"**
   - Set your API key: `export OPENAI_API_KEY="your-key"`
   - Or use the `--api-key` parameter

2. **"Invalid file format"**
   - Ensure your CV is in PDF, DOCX, or TXT format
   - Check file size (max 10MB)

3. **"File not found"**
   - Verify the file path is correct
   - Use absolute paths if needed

4. **"Processing timeout"**
   - Large files or complex job descriptions may take longer
   - Consider breaking down large job descriptions

### Performance Tips

- Use concise job descriptions for faster processing
- Ensure CV files are well-formatted and readable
- Use modern template for faster PDF generation

## API Integration

The service can be integrated into web applications using the FastAPI server:

```bash
# Start the API server
cd src/api
python main.py
```

Then access the API at `http://localhost:8000/docs`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the example files
3. Open an issue on the repository

## Changelog

### Version 1.0.0
- Initial release
- CV parsing and optimization
- PDF generation with multiple templates
- Job description analysis
- Command-line interface
- Python API 