# Smart CV Writer Service

A sophisticated AI-powered CV writer that intelligently modifies existing CVs to match specific job descriptions and requirements. This service analyzes job descriptions, extracts key requirements, and optimizes CV content to maximize match scores.

## Features

### Core Capabilities
- **Job Description Analysis**: Extracts key requirements, skills, and responsibilities from job postings
- **CV Optimization**: Intelligently modifies existing CV content to match job requirements
- **Skill Enhancement**: Suggests and incorporates relevant skills and keywords
- **Experience Tailoring**: Rewrites job descriptions to highlight relevant experience
- **Summary Optimization**: Creates compelling professional summaries tailored to specific roles
- **Multiple Output Formats**: Generates optimized CVs in PDF, DOCX, and plain text formats

### Advanced Features
- **ATS Optimization**: Ensures CVs pass through Applicant Tracking Systems
- **Keyword Matching**: Identifies and incorporates industry-specific keywords
- **Experience Relevance Scoring**: Prioritizes most relevant work experience
- **Skill Gap Analysis**: Identifies missing skills and suggests alternatives
- **Cultural Fit Optimization**: Adapts language and tone to match company culture

## Architecture

```
cv_writer_service/
├── src/
│   ├── core/
│   │   ├── cv_analyzer.py      # Analyzes existing CVs
│   │   ├── job_analyzer.py     # Analyzes job descriptions
│   │   ├── cv_optimizer.py     # Main optimization logic
│   │   └── cv_generator.py     # Generates output files
│   ├── models/
│   │   ├── cv_data.py          # CV data structures
│   │   ├── job_data.py         # Job description structures
│   │   └── optimization.py     # Optimization results
│   ├── utils/
│   │   ├── file_processor.py   # File handling utilities
│   │   ├── text_processor.py   # Text processing utilities
│   │   └── formatter.py        # Output formatting
│   └── api/
│       ├── main.py             # FastAPI application
│       └── routes.py           # API endpoints
├── config/
│   └── config.yaml             # Configuration settings
├── templates/
│   └── cv_templates/           # CV template files
├── tests/
│   └── test_cv_writer.py       # Unit tests
├── requirements.txt            # Python dependencies
└── Dockerfile                  # Container configuration
```

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Docker (optional)

### Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your OpenAI API key in `config/config.yaml`
4. Run the service:
   ```bash
   python src/api/main.py
   ```

## Usage

### API Endpoints

#### Optimize CV
```http
POST /api/v1/optimize-cv
Content-Type: multipart/form-data

{
  "cv_file": "path/to/cv.pdf",
  "job_description": "Software Engineer position...",
  "output_format": "pdf"
}
```

#### Analyze Job Description
```http
POST /api/v1/analyze-job
Content-Type: application/json

{
  "job_description": "Full job description text..."
}
```

#### Get Optimization Suggestions
```http
POST /api/v1/suggestions
Content-Type: application/json

{
  "cv_data": {...},
  "job_analysis": {...}
}
```

### Python SDK Usage

```python
from cv_writer_service import CVWriter

# Initialize the service
writer = CVWriter(api_key="your-openai-key")

# Optimize a CV for a specific job
optimized_cv = writer.optimize_cv(
    cv_file="path/to/cv.pdf",
    job_description="Software Engineer position...",
    output_format="pdf"
)

# Get optimization suggestions
suggestions = writer.get_suggestions(cv_data, job_analysis)
```

## Configuration

### OpenAI Settings
```yaml
openai:
  api_key: "your-api-key"
  model: "gpt-4-turbo"
  temperature: 0.1
  max_tokens: 4000
```

### Optimization Settings
```yaml
optimization:
  skill_weight: 0.4
  experience_weight: 0.3
  education_weight: 0.2
  summary_weight: 0.1
  max_summary_length: 200
  keyword_boost: 1.5
```

### Output Settings
```yaml
output:
  default_format: "pdf"
  include_original: false
  template_style: "modern"
  font_size: 11
  line_spacing: 1.15
```

## Advanced Features

### Custom Templates
Create custom CV templates in `templates/cv_templates/`:
- Modern professional template
- Creative design template
- Minimalist template
- Industry-specific templates

### Skill Mapping
The service includes intelligent skill mapping:
- Technical skill synonyms
- Industry-specific terminology
- Skill hierarchy and relationships
- Emerging technology mapping

### Experience Optimization
- Relevance scoring for each job experience
- Achievement quantification
- Impact measurement
- Keyword integration

## Performance

### Optimization Metrics
- **Match Score**: Overall fit percentage (0-100)
- **Skill Coverage**: Percentage of required skills matched
- **Experience Relevance**: Relevance score for work history
- **Keyword Density**: Optimal keyword distribution
- **ATS Compatibility**: ATS-friendly formatting score

### Processing Time
- **Small CVs** (< 2 pages): 30-60 seconds
- **Medium CVs** (2-4 pages): 60-120 seconds
- **Large CVs** (> 4 pages): 120-300 seconds

## Security

- API key encryption
- Secure file handling
- Input validation
- Rate limiting
- Audit logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the examples in the `examples/` directory 