"""
Job description data models for the smart CV writer service
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
import json


@dataclass
class JobRequirement:
    """Individual job requirement with metadata"""
    text: str
    category: str  # required, preferred, bonus, nice_to_have
    importance: float  # 0.0 to 1.0
    keywords: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    industry_context: str = ""


@dataclass
class SkillRequirement:
    """Detailed skill requirement"""
    skill_name: str
    category: str  # technical, soft, tool, certification
    level: str  # beginner, intermediate, advanced, expert
    years_experience: Optional[int] = None
    required: bool = True
    alternatives: List[str] = field(default_factory=list)
    industry_specific: bool = False


@dataclass
class ExperienceRequirement:
    """Experience requirement details"""
    years_required: int
    role_type: str  # specific role, general field, industry
    relevant_positions: List[str] = field(default_factory=list)
    industry_preference: List[str] = field(default_factory=list)
    project_scale: str = ""  # small, medium, large, enterprise


@dataclass
class EducationRequirement:
    """Education requirement details"""
    degree_level: str  # high_school, associate, bachelor, master, phd
    field_of_study: List[str] = field(default_factory=list)
    required: bool = True
    equivalent_experience: bool = False
    certifications_accepted: List[str] = field(default_factory=list)


@dataclass
class CompanyInfo:
    """Company information extracted from job description"""
    name: str = ""
    industry: str = ""
    size: str = ""  # startup, small, medium, large, enterprise
    location: str = ""
    remote_policy: str = ""  # remote, hybrid, on-site
    culture_keywords: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)


@dataclass
class JobDescription:
    """Comprehensive job description data structure"""
    title: str = ""
    company: CompanyInfo = field(default_factory=CompanyInfo)
    location: str = ""
    employment_type: str = ""  # full-time, part-time, contract, internship
    experience_level: str = ""  # entry, junior, mid, senior, lead, executive
    salary_range: str = ""
    description: str = ""
    
    # Structured requirements
    required_skills: List[SkillRequirement] = field(default_factory=list)
    preferred_skills: List[SkillRequirement] = field(default_factory=list)
    experience_requirements: ExperienceRequirement = field(default_factory=ExperienceRequirement)
    education_requirements: EducationRequirement = field(default_factory=EducationRequirement)
    
    # Responsibilities and duties
    responsibilities: List[str] = field(default_factory=list)
    duties: List[str] = field(default_factory=list)
    
    # Benefits and perks
    benefits: List[str] = field(default_factory=list)
    perks: List[str] = field(default_factory=list)
    
    # Additional information
    keywords: List[str] = field(default_factory=list)
    industry_keywords: List[str] = field(default_factory=list)
    technology_stack: List[str] = field(default_factory=list)
    methodologies: List[str] = field(default_factory=list)  # agile, scrum, etc.
    
    # Analysis metadata
    confidence_score: float = 0.0
    extraction_quality: str = ""  # high, medium, low
    missing_information: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dictionary"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def get_all_required_skills(self) -> List[str]:
        """Get all required skills as a flat list"""
        return [skill.skill_name for skill in self.required_skills]

    def get_all_preferred_skills(self) -> List[str]:
        """Get all preferred skills as a flat list"""
        return [skill.skill_name for skill in self.preferred_skills]

    def get_all_skills(self) -> List[str]:
        """Get all skills (required and preferred)"""
        return self.get_all_required_skills() + self.get_all_preferred_skills()

    def get_skill_by_name(self, skill_name: str) -> Optional[SkillRequirement]:
        """Get a skill requirement by name"""
        all_skills = self.required_skills + self.preferred_skills
        for skill in all_skills:
            if skill.skill_name.lower() == skill_name.lower():
                return skill
        return None

    def is_skill_required(self, skill_name: str) -> bool:
        """Check if a skill is required"""
        skill = self.get_skill_by_name(skill_name)
        return skill.required if skill else False

    def get_skill_alternatives(self, skill_name: str) -> List[str]:
        """Get alternative skills for a given skill"""
        skill = self.get_skill_by_name(skill_name)
        return skill.alternatives if skill else []

    def get_high_priority_skills(self, threshold: float = 0.8) -> List[SkillRequirement]:
        """Get skills with high importance score"""
        return [skill for skill in self.required_skills if skill.importance >= threshold]

    def get_technical_skills(self) -> List[SkillRequirement]:
        """Get only technical skills"""
        return [skill for skill in self.required_skills + self.preferred_skills 
                if skill.category == "technical"]

    def get_soft_skills(self) -> List[SkillRequirement]:
        """Get only soft skills"""
        return [skill for skill in self.required_skills + self.preferred_skills 
                if skill.category == "soft"]

    def get_tool_skills(self) -> List[SkillRequirement]:
        """Get only tool skills"""
        return [skill for skill in self.required_skills + self.preferred_skills 
                if skill.category == "tool"]

    def add_skill_requirement(self, skill: SkillRequirement):
        """Add a skill requirement"""
        if skill.required:
            self.required_skills.append(skill)
        else:
            self.preferred_skills.append(skill)

    def remove_skill_requirement(self, skill_name: str):
        """Remove a skill requirement by name"""
        self.required_skills[:] = [s for s in self.required_skills 
                                  if s.skill_name.lower() != skill_name.lower()]
        self.preferred_skills[:] = [s for s in self.preferred_skills 
                                   if s.skill_name.lower() != skill_name.lower()]

    def get_keyword_density(self) -> Dict[str, int]:
        """Calculate keyword density in the job description"""
        text = f"{self.description} {' '.join(self.responsibilities)}"
        text_lower = text.lower()
        keyword_density = {}
        
        for keyword in self.keywords:
            keyword_density[keyword] = text_lower.count(keyword.lower())
        
        return keyword_density

    def get_industry_context(self) -> str:
        """Get industry context from company and keywords"""
        context_parts = []
        if self.company.industry:
            context_parts.append(self.company.industry)
        if self.industry_keywords:
            context_parts.extend(self.industry_keywords[:3])
        return ", ".join(context_parts)

    def is_remote_friendly(self) -> bool:
        """Check if the job is remote-friendly"""
        remote_keywords = ["remote", "work from home", "wfh", "virtual", "distributed"]
        text = f"{self.description} {self.employment_type}".lower()
        return any(keyword in text for keyword in remote_keywords)

    def get_experience_level_numeric(self) -> int:
        """Convert experience level to numeric value"""
        level_mapping = {
            "entry": 1,
            "junior": 2,
            "mid": 3,
            "senior": 4,
            "lead": 5,
            "executive": 6
        }
        return level_mapping.get(self.experience_level.lower(), 3)

    def get_company_size_numeric(self) -> int:
        """Convert company size to numeric value"""
        size_mapping = {
            "startup": 1,
            "small": 2,
            "medium": 3,
            "large": 4,
            "enterprise": 5
        }
        return size_mapping.get(self.company.size.lower(), 3)


@dataclass
class JobAnalysisResult:
    """Result of job description analysis"""
    job_description: JobDescription
    extracted_requirements: List[JobRequirement]
    skill_gaps: List[str]
    industry_insights: Dict[str, Any]
    company_culture: Dict[str, Any]
    salary_benchmarks: Dict[str, Any]
    processing_time: float
    confidence_score: float
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, default=str)


@dataclass
class JobMarketData:
    """Market data for job analysis"""
    average_salary: float
    salary_range: Dict[str, float]
    demand_score: float  # 0-100
    competition_level: str  # low, medium, high
    growth_rate: float
    required_skills_trend: List[str]
    emerging_skills: List[str]
    industry_trends: Dict[str, Any] 