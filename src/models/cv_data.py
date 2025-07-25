"""
CV data models for the smart CV writer service
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
import json
from datetime import datetime


@dataclass
class ContactInfo:
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    website: str = ""


@dataclass
class EmploymentDetail:
    company: str = ""
    position: str = ""
    start_date: str = ""
    end_date: str = ""
    location: str = ""
    description: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    relevance_score: float = 0.0
    impact_metrics: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dictionary"""
        return asdict(self)


@dataclass
class Education:
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    graduation_date: str = ""
    gpa: str = ""
    honors: str = ""
    relevant_courses: List[str] = field(default_factory=list)
    thesis: str = ""


@dataclass
class Project:
    name: str = ""
    description: str = ""
    technologies: List[str] = field(default_factory=list)
    url: str = ""
    github_url: str = ""
    impact: str = ""
    role: str = ""
    duration: str = ""
    team_size: int = 1
    relevance_score: float = 0.0


@dataclass
class Skill:
    name: str = ""
    category: str = ""  # technical, soft, language, certification
    proficiency: str = ""  # beginner, intermediate, advanced, expert
    years_experience: int = 0
    relevance_score: float = 0.0
    keywords: List[str] = field(default_factory=list)


@dataclass
class CVData:
    """Enhanced CV data structure with optimization fields"""
    contact_info: ContactInfo = field(default_factory=ContactInfo)
    summary: str = ""
    employment_history: List[EmploymentDetail] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    technical_skills: List[Skill] = field(default_factory=list)
    soft_skills: List[Skill] = field(default_factory=list)
    languages: List[Skill] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    
    # Optimization metadata
    original_file_path: str = ""
    optimization_date: Optional[datetime] = None
    target_job_title: str = ""
    target_company: str = ""
    optimization_score: float = 0.0
    keyword_matches: Dict[str, int] = field(default_factory=dict)
    skill_gaps: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dictionary"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def get_all_skills(self) -> List[str]:
        """Get all skills as a flat list"""
        skills = []
        for skill in self.technical_skills + self.soft_skills + self.languages:
            skills.append(skill.name)
        skills.extend(self.certifications)
        return skills

    def get_skill_by_name(self, skill_name: str) -> Optional[Skill]:
        """Get a skill by name"""
        all_skills = self.technical_skills + self.soft_skills + self.languages
        for skill in all_skills:
            if skill.name.lower() == skill_name.lower():
                return skill
        return None

    def add_skill(self, skill: Skill):
        """Add a skill to the appropriate category"""
        if skill.category == "technical":
            self.technical_skills.append(skill)
        elif skill.category == "soft":
            self.soft_skills.append(skill)
        elif skill.category == "language":
            self.languages.append(skill)

    def remove_skill(self, skill_name: str):
        """Remove a skill by name"""
        for skill_list in [self.technical_skills, self.soft_skills, self.languages]:
            skill_list[:] = [s for s in skill_list if s.name.lower() != skill_name.lower()]

    def get_experience_by_company(self, company_name: str) -> Optional[EmploymentDetail]:
        """Get employment experience by company name"""
        for job in self.employment_history:
            if job.company.lower() == company_name.lower():
                return job
        return None

    def sort_experience_by_relevance(self):
        """Sort employment history by relevance score"""
        self.employment_history.sort(key=lambda x: x.relevance_score, reverse=True)

    def get_most_relevant_experience(self, limit: int = 5) -> List[EmploymentDetail]:
        """Get the most relevant work experience"""
        self.sort_experience_by_relevance()
        return self.employment_history[:limit]

    def calculate_total_experience_years(self) -> float:
        """Calculate total years of experience"""
        total_years = 0.0
        for job in self.employment_history:
            try:
                start_year = int(job.start_date.split()[-1]) if job.start_date else 0
                end_year = int(job.end_date.split()[-1]) if job.end_date and job.end_date.lower() != "present" else datetime.now().year
                total_years += end_year - start_year
            except (ValueError, IndexError):
                continue
        return total_years

    def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get skills by category"""
        if category == "technical":
            return self.technical_skills
        elif category == "soft":
            return self.soft_skills
        elif category == "language":
            return self.languages
        return []

    def merge_with_existing_cv(self, existing_cv: 'CVData') -> 'CVData':
        """Merge with existing CV data, preserving important information"""
        merged = CVData()
        
        # Merge contact info (prefer existing if available)
        merged.contact_info = existing_cv.contact_info if existing_cv.contact_info.full_name else self.contact_info
        
        # Merge employment history (combine and deduplicate)
        merged.employment_history = existing_cv.employment_history + self.employment_history
        # TODO: Add deduplication logic
        
        # Merge education
        merged.education = existing_cv.education + self.education
        
        # Merge skills (combine and remove duplicates)
        merged.technical_skills = existing_cv.technical_skills + self.technical_skills
        merged.soft_skills = existing_cv.soft_skills + self.soft_skills
        merged.languages = existing_cv.languages + self.languages
        
        # Merge projects
        merged.projects = existing_cv.projects + self.projects
        
        # Use the optimized summary
        merged.summary = self.summary
        
        return merged


@dataclass
class CVOptimizationResult:
    """Result of CV optimization process"""
    original_cv: CVData
    optimized_cv: CVData
    optimization_score: float
    improvements_made: List[str]
    skill_gaps_identified: List[str]
    keyword_matches: Dict[str, int]
    processing_time: float
    output_file_path: str = ""
    error_message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, default=str)


@dataclass
class CVTemplate:
    """CV template configuration"""
    name: str
    style: str
    font_family: str
    font_size: int
    line_spacing: float
    margin: float
    header_color: str
    section_color: str
    accent_color: str
    sections: List[str] = field(default_factory=list)
    custom_css: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self) 