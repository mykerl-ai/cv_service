"""
CV analyzer for the smart CV writer service
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from openai import OpenAI

from ..models.cv_data import CVData, ContactInfo, EmploymentDetail, Education, Skill, Project
from ..utils.file_processor import FileProcessor

logger = logging.getLogger(__name__)


class CVAnalyzer:
    """Analyzes and parses CV documents to extract structured information"""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo", temperature: float = 0.1):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)
        self.file_processor = FileProcessor()
    
    def parse_cv(self, file_path: str) -> CVData:
        """Parse CV file and extract structured information"""
        try:
            # Validate file
            is_valid, error_message = self.file_processor.validate_file(file_path)
            if not is_valid:
                raise ValueError(f"Invalid file: {error_message}")
            
            # Extract text from file
            cv_text = self.file_processor.extract_text_from_file(file_path)
            if not cv_text:
                raise ValueError("Could not extract text from CV file")
            
            # Parse CV using AI
            cv_data = self._parse_cv_with_ai(cv_text)
            
            # Set metadata
            cv_data.original_file_path = file_path
            
            return cv_data
            
        except Exception as e:
            logger.error(f"Error parsing CV {file_path}: {str(e)}")
            raise
    
    def _parse_cv_with_ai(self, cv_text: str) -> CVData:
        """Parse CV text using AI to extract structured information"""
        system_prompt = """
        You are an expert CV parser. Extract structured information from the provided CV text.
        
        Return the analysis as a JSON object with the following structure:
        {
          "contact_info": {
            "full_name": "Full name",
            "email": "Email address",
            "phone": "Phone number",
            "location": "Location/City, State",
            "linkedin": "LinkedIn URL",
            "github": "GitHub URL",
            "portfolio": "Portfolio URL",
            "website": "Personal website"
          },
          "summary": "Professional summary",
          "employment_history": [
            {
              "company": "Company name",
              "position": "Job title",
              "start_date": "Start date",
              "end_date": "End date (or 'Present')",
              "location": "Job location",
              "description": ["Responsibility 1", "Responsibility 2"],
              "achievements": ["Achievement 1", "Achievement 2"],
              "technologies": ["Tech 1", "Tech 2"]
            }
          ],
          "education": [
            {
              "institution": "Institution name",
              "degree": "Degree type",
              "field_of_study": "Field of study",
              "graduation_date": "Graduation date",
              "gpa": "GPA if available",
              "honors": "Honors if any",
              "relevant_courses": ["Course 1", "Course 2"],
              "thesis": "Thesis topic if applicable"
            }
          ],
          "technical_skills": [
            {
              "name": "Skill name",
              "category": "technical",
              "proficiency": "beginner/intermediate/advanced/expert",
              "years_experience": 0,
              "relevance_score": 0.0,
              "keywords": ["keyword1", "keyword2"]
            }
          ],
          "soft_skills": [
            {
              "name": "Skill name",
              "category": "soft",
              "proficiency": "beginner/intermediate/advanced/expert",
              "years_experience": 0,
              "relevance_score": 0.0,
              "keywords": ["keyword1", "keyword2"]
            }
          ],
          "languages": [
            {
              "name": "Language name",
              "category": "language",
              "proficiency": "beginner/intermediate/advanced/expert",
              "years_experience": 0,
              "relevance_score": 0.0,
              "keywords": ["keyword1", "keyword2"]
            }
          ],
          "certifications": ["Certification 1", "Certification 2"],
          "projects": [
            {
              "name": "Project name",
              "description": "Project description",
              "technologies": ["Tech 1", "Tech 2"],
              "url": "Project URL",
              "github_url": "GitHub URL",
              "impact": "Project impact",
              "role": "Role in project",
              "duration": "Project duration",
              "team_size": 1
            }
          ]
        }
        
        Be precise and extract only what is explicitly stated in the CV. Use empty strings or empty arrays for missing information.
        Ensure the output is valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": cv_text}
                ],
                temperature=self.temperature,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
            
            data = json.loads(content)
            
            # Build CVData object
            return self._build_cv_data(data)
            
        except Exception as e:
            logger.error(f"Error parsing CV with AI: {str(e)}")
            raise
    
    def _build_cv_data(self, data: Dict[str, Any]) -> CVData:
        """Build CVData object from parsed data"""
        cv_data = CVData()
        
        # Contact info
        if "contact_info" in data:
            contact = data["contact_info"]
            cv_data.contact_info = ContactInfo(
                full_name=contact.get("full_name", ""),
                email=contact.get("email", ""),
                phone=contact.get("phone", ""),
                location=contact.get("location", ""),
                linkedin=contact.get("linkedin", ""),
                github=contact.get("github", ""),
                portfolio=contact.get("portfolio", ""),
                website=contact.get("website", "")
            )
        
        # Summary
        cv_data.summary = data.get("summary", "")
        
        # Employment history
        if "employment_history" in data:
            for job_data in data["employment_history"]:
                employment = EmploymentDetail(
                    company=job_data.get("company", ""),
                    position=job_data.get("position", ""),
                    start_date=job_data.get("start_date", ""),
                    end_date=job_data.get("end_date", ""),
                    location=job_data.get("location", ""),
                    description=job_data.get("description", []),
                    achievements=job_data.get("achievements", []),
                    technologies=job_data.get("technologies", [])
                )
                cv_data.employment_history.append(employment)
        
        # Education
        if "education" in data:
            for edu_data in data["education"]:
                education = Education(
                    institution=edu_data.get("institution", ""),
                    degree=edu_data.get("degree", ""),
                    field_of_study=edu_data.get("field_of_study", ""),
                    graduation_date=edu_data.get("graduation_date", ""),
                    gpa=edu_data.get("gpa", ""),
                    honors=edu_data.get("honors", ""),
                    relevant_courses=edu_data.get("relevant_courses", []),
                    thesis=edu_data.get("thesis", "")
                )
                cv_data.education.append(education)
        
        # Technical skills
        if "technical_skills" in data:
            for skill_data in data["technical_skills"]:
                skill = Skill(
                    name=skill_data.get("name", ""),
                    category="technical",
                    proficiency=skill_data.get("proficiency", "intermediate"),
                    years_experience=skill_data.get("years_experience", 0),
                    relevance_score=skill_data.get("relevance_score", 0.0),
                    keywords=skill_data.get("keywords", [])
                )
                cv_data.technical_skills.append(skill)
        
        # Soft skills
        if "soft_skills" in data:
            for skill_data in data["soft_skills"]:
                skill = Skill(
                    name=skill_data.get("name", ""),
                    category="soft",
                    proficiency=skill_data.get("proficiency", "intermediate"),
                    years_experience=skill_data.get("years_experience", 0),
                    relevance_score=skill_data.get("relevance_score", 0.0),
                    keywords=skill_data.get("keywords", [])
                )
                cv_data.soft_skills.append(skill)
        
        # Languages
        if "languages" in data:
            for skill_data in data["languages"]:
                skill = Skill(
                    name=skill_data.get("name", ""),
                    category="language",
                    proficiency=skill_data.get("proficiency", "intermediate"),
                    years_experience=skill_data.get("years_experience", 0),
                    relevance_score=skill_data.get("relevance_score", 0.0),
                    keywords=skill_data.get("keywords", [])
                )
                cv_data.languages.append(skill)
        
        # Certifications
        cv_data.certifications = data.get("certifications", [])
        
        # Projects
        if "projects" in data:
            for project_data in data["projects"]:
                project = Project(
                    name=project_data.get("name", ""),
                    description=project_data.get("description", ""),
                    technologies=project_data.get("technologies", []),
                    url=project_data.get("url", ""),
                    github_url=project_data.get("github_url", ""),
                    impact=project_data.get("impact", ""),
                    role=project_data.get("role", ""),
                    duration=project_data.get("duration", ""),
                    team_size=project_data.get("team_size", 1)
                )
                cv_data.projects.append(project)
        
        return cv_data
    
    def analyze_cv_strengths(self, cv_data: CVData) -> Dict[str, Any]:
        """Analyze CV strengths and areas for improvement"""
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Analyze contact information
        if not cv_data.contact_info.email:
            weaknesses.append("Missing email address")
        if not cv_data.contact_info.phone:
            weaknesses.append("Missing phone number")
        if not cv_data.contact_info.linkedin:
            suggestions.append("Consider adding LinkedIn profile")
        
        # Analyze summary
        if not cv_data.summary:
            weaknesses.append("Missing professional summary")
        elif len(cv_data.summary) < 50:
            weaknesses.append("Professional summary is too short")
        elif len(cv_data.summary) > 300:
            weaknesses.append("Professional summary is too long")
        
        # Analyze experience
        if not cv_data.employment_history:
            weaknesses.append("No work experience listed")
        else:
            strengths.append(f"Has {len(cv_data.employment_history)} work experiences")
            
            # Check for quantified achievements
            quantified_achievements = 0
            for job in cv_data.employment_history:
                for achievement in job.achievements:
                    if any(word in achievement.lower() for word in ["%", "percent", "increased", "decreased", "improved", "reduced"]):
                        quantified_achievements += 1
            
            if quantified_achievements > 0:
                strengths.append(f"Has {quantified_achievements} quantified achievements")
            else:
                suggestions.append("Consider adding quantified achievements")
        
        # Analyze skills
        if not cv_data.technical_skills:
            weaknesses.append("No technical skills listed")
        else:
            strengths.append(f"Has {len(cv_data.technical_skills)} technical skills")
        
        if not cv_data.soft_skills:
            suggestions.append("Consider adding soft skills")
        else:
            strengths.append(f"Has {len(cv_data.soft_skills)} soft skills")
        
        # Analyze education
        if not cv_data.education:
            weaknesses.append("No education information")
        else:
            strengths.append(f"Has {len(cv_data.education)} education entries")
        
        # Analyze projects
        if cv_data.projects:
            strengths.append(f"Has {len(cv_data.projects)} projects")
        else:
            suggestions.append("Consider adding relevant projects")
        
        # Calculate overall score
        total_items = len(strengths) + len(weaknesses)
        score = (len(strengths) / total_items * 100) if total_items > 0 else 0
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "overall_score": round(score, 1),
            "total_experience_years": cv_data.calculate_total_experience_years()
        }
    
    def extract_keywords(self, cv_data: CVData) -> List[str]:
        """Extract keywords from CV"""
        keywords = []
        
        # Extract from summary
        if cv_data.summary:
            keywords.extend(self._extract_keywords_from_text(cv_data.summary))
        
        # Extract from job descriptions
        for job in cv_data.employment_history:
            for desc in job.description:
                keywords.extend(self._extract_keywords_from_text(desc))
            for achievement in job.achievements:
                keywords.extend(self._extract_keywords_from_text(achievement))
        
        # Extract from skills
        for skill in cv_data.technical_skills + cv_data.soft_skills:
            keywords.append(skill.name.lower())
        
        # Extract from projects
        for project in cv_data.projects:
            keywords.extend(self._extract_keywords_from_text(project.description))
            keywords.extend(project.technologies)
        
        # Remove duplicates and common words
        unique_keywords = list(set(keywords))
        filtered_keywords = [kw for kw in unique_keywords if len(kw) > 2 and kw not in self._get_common_words()]
        
        return filtered_keywords[:50]  # Limit to top 50 keywords
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from text"""
        import re
        
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Split into words
        words = text.split()
        
        # Filter out common words and short words
        common_words = self._get_common_words()
        keywords = [word for word in words if word not in common_words and len(word) > 2]
        
        return keywords
    
    def _get_common_words(self) -> List[str]:
        """Get list of common words to filter out"""
        return [
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
            "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those",
            "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
            "my", "your", "his", "her", "its", "our", "their", "mine", "yours", "hers", "ours", "theirs"
        ]
    
    def get_cv_statistics(self, cv_data: CVData) -> Dict[str, Any]:
        """Get CV statistics and metrics"""
        stats = {
            "total_words": 0,
            "total_experience_years": cv_data.calculate_total_experience_years(),
            "number_of_jobs": len(cv_data.employment_history),
            "number_of_skills": len(cv_data.technical_skills) + len(cv_data.soft_skills),
            "number_of_projects": len(cv_data.projects),
            "number_of_education": len(cv_data.education),
            "has_linkedin": bool(cv_data.contact_info.linkedin),
            "has_github": bool(cv_data.contact_info.github),
            "has_portfolio": bool(cv_data.contact_info.portfolio),
            "has_summary": bool(cv_data.summary),
            "summary_length": len(cv_data.summary) if cv_data.summary else 0
        }
        
        # Calculate total words
        if cv_data.summary:
            stats["total_words"] += len(cv_data.summary.split())
        
        for job in cv_data.employment_history:
            for desc in job.description:
                stats["total_words"] += len(desc.split())
            for achievement in job.achievements:
                stats["total_words"] += len(achievement.split())
        
        for project in cv_data.projects:
            if project.description:
                stats["total_words"] += len(project.description.split())
        
        return stats 