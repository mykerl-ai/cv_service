"""
Job description analyzer for the smart CV writer service
"""
import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from openai import OpenAI

from ..models.job_data import (
    JobDescription, JobRequirement, SkillRequirement, ExperienceRequirement,
    EducationRequirement, CompanyInfo, JobAnalysisResult, JobMarketData
)

logger = logging.getLogger(__name__)


class JobAnalyzer:
    """Analyzes job descriptions to extract requirements and insights"""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo", temperature: float = 0.1):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)
        
    def analyze_job_description(self, job_text: str) -> JobAnalysisResult:
        """Analyze a job description and extract structured information"""
        start_time = datetime.now()
        
        try:
            # Extract structured job data
            job_description = self._extract_job_data(job_text)
            
            # Extract requirements
            requirements = self._extract_requirements(job_text, job_description)
            
            # Analyze skill gaps and insights
            skill_gaps = self._identify_skill_gaps(job_description)
            industry_insights = self._analyze_industry_context(job_description)
            company_culture = self._analyze_company_culture(job_description)
            salary_benchmarks = self._get_salary_benchmarks(job_description)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(job_description, skill_gaps)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return JobAnalysisResult(
                job_description=job_description,
                extracted_requirements=requirements,
                skill_gaps=skill_gaps,
                industry_insights=industry_insights,
                company_culture=company_culture,
                salary_benchmarks=salary_benchmarks,
                processing_time=processing_time,
                confidence_score=0.85,  # TODO: Implement confidence scoring
                suggestions=suggestions
            )
            
        except Exception as e:
            logger.error(f"Error analyzing job description: {str(e)}")
            raise
    
    def _extract_job_data(self, job_text: str) -> JobDescription:
        """Extract structured job data from text"""
        system_prompt = """
        You are an expert job description analyzer. Extract structured information from the provided job description.
        
        Return the analysis as a JSON object with the following structure:
        {
          "title": "Job title",
          "company": {
            "name": "Company name",
            "industry": "Industry",
            "size": "Company size (startup/small/medium/large/enterprise)",
            "location": "Location",
            "remote_policy": "Remote policy",
            "culture_keywords": ["culture", "keywords"],
            "tech_stack": ["tech", "stack"]
          },
          "location": "Job location",
          "employment_type": "Employment type",
          "experience_level": "Experience level",
          "salary_range": "Salary range",
          "description": "Full description",
          "required_skills": [
            {
              "skill_name": "Skill name",
              "category": "technical/soft/tool/certification",
              "level": "beginner/intermediate/advanced/expert",
              "years_experience": null,
              "required": true,
              "alternatives": [],
              "industry_specific": false
            }
          ],
          "preferred_skills": [...],
          "experience_requirements": {
            "years_required": 0,
            "role_type": "Role type",
            "relevant_positions": [],
            "industry_preference": [],
            "project_scale": ""
          },
          "education_requirements": {
            "degree_level": "Degree level",
            "field_of_study": [],
            "required": true,
            "equivalent_experience": false,
            "certifications_accepted": []
          },
          "responsibilities": ["Responsibility 1", "Responsibility 2"],
          "duties": ["Duty 1", "Duty 2"],
          "benefits": ["Benefit 1", "Benefit 2"],
          "perks": ["Perk 1", "Perk 2"],
          "keywords": ["keyword1", "keyword2"],
          "industry_keywords": ["industry", "keywords"],
          "technology_stack": ["tech1", "tech2"],
          "methodologies": ["agile", "scrum"]
        }
        
        Be precise and extract only what is explicitly stated. Use null for missing information.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": job_text}
                ],
                temperature=self.temperature,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
            
            data = json.loads(content)
            
            # Build JobDescription object
            company_info = CompanyInfo(
                name=data.get("company", {}).get("name", ""),
                industry=data.get("company", {}).get("industry", ""),
                size=data.get("company", {}).get("size", ""),
                location=data.get("company", {}).get("location", ""),
                remote_policy=data.get("company", {}).get("remote_policy", ""),
                culture_keywords=data.get("company", {}).get("culture_keywords", []),
                tech_stack=data.get("company", {}).get("tech_stack", [])
            )
            
            # Build skill requirements
            required_skills = []
            for skill_data in data.get("required_skills", []):
                required_skills.append(SkillRequirement(
                    skill_name=skill_data.get("skill_name", ""),
                    category=skill_data.get("category", "technical"),
                    level=skill_data.get("level", "intermediate"),
                    years_experience=skill_data.get("years_experience"),
                    required=skill_data.get("required", True),
                    alternatives=skill_data.get("alternatives", []),
                    industry_specific=skill_data.get("industry_specific", False)
                ))
            
            preferred_skills = []
            for skill_data in data.get("preferred_skills", []):
                preferred_skills.append(SkillRequirement(
                    skill_name=skill_data.get("skill_name", ""),
                    category=skill_data.get("category", "technical"),
                    level=skill_data.get("level", "intermediate"),
                    years_experience=skill_data.get("years_experience"),
                    required=False,
                    alternatives=skill_data.get("alternatives", []),
                    industry_specific=skill_data.get("industry_specific", False)
                ))
            
            # Build experience requirements
            exp_req_data = data.get("experience_requirements", {})
            experience_requirements = ExperienceRequirement(
                years_required=exp_req_data.get("years_required", 0),
                role_type=exp_req_data.get("role_type", ""),
                relevant_positions=exp_req_data.get("relevant_positions", []),
                industry_preference=exp_req_data.get("industry_preference", []),
                project_scale=exp_req_data.get("project_scale", "")
            )
            
            # Build education requirements
            edu_req_data = data.get("education_requirements", {})
            education_requirements = EducationRequirement(
                degree_level=edu_req_data.get("degree_level", ""),
                field_of_study=edu_req_data.get("field_of_study", []),
                required=edu_req_data.get("required", True),
                equivalent_experience=edu_req_data.get("equivalent_experience", False),
                certifications_accepted=edu_req_data.get("certifications_accepted", [])
            )
            
            return JobDescription(
                title=data.get("title", ""),
                company=company_info,
                location=data.get("location", ""),
                employment_type=data.get("employment_type", ""),
                experience_level=data.get("experience_level", ""),
                salary_range=data.get("salary_range", ""),
                description=data.get("description", ""),
                required_skills=required_skills,
                preferred_skills=preferred_skills,
                experience_requirements=experience_requirements,
                education_requirements=education_requirements,
                responsibilities=data.get("responsibilities", []),
                duties=data.get("duties", []),
                benefits=data.get("benefits", []),
                perks=data.get("perks", []),
                keywords=data.get("keywords", []),
                industry_keywords=data.get("industry_keywords", []),
                technology_stack=data.get("technology_stack", []),
                methodologies=data.get("methodologies", [])
            )
            
        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
            raise
    
    def _extract_requirements(self, job_text: str, job_description: JobDescription) -> List[JobRequirement]:
        """Extract individual requirements from job description"""
        system_prompt = """
        Extract individual requirements from the job description. Each requirement should be categorized and scored for importance.
        
        Return as JSON array:
        [
          {
            "text": "Requirement text",
            "category": "required/preferred/bonus/nice_to_have",
            "importance": 0.0-1.0,
            "keywords": ["keyword1", "keyword2"],
            "synonyms": ["synonym1", "synonym2"],
            "industry_context": "Industry context"
          }
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": job_text}
                ],
                temperature=self.temperature,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if not content:
                return []
            
            data = json.loads(content)
            requirements = []
            
            for req_data in data:
                requirements.append(JobRequirement(
                    text=req_data.get("text", ""),
                    category=req_data.get("category", "required"),
                    importance=req_data.get("importance", 0.5),
                    keywords=req_data.get("keywords", []),
                    synonyms=req_data.get("synonyms", []),
                    industry_context=req_data.get("industry_context", "")
                ))
            
            return requirements
            
        except Exception as e:
            logger.error(f"Error extracting requirements: {str(e)}")
            return []
    
    def _identify_skill_gaps(self, job_description: JobDescription) -> List[str]:
        """Identify potential skill gaps in the job requirements"""
        skill_gaps = []
        
        # Analyze required skills for potential gaps
        for skill in job_description.required_skills:
            if skill.industry_specific and not skill.alternatives:
                skill_gaps.append(f"Industry-specific skill: {skill.skill_name}")
            
            if skill.level == "expert" and skill.years_experience and skill.years_experience > 5:
                skill_gaps.append(f"High experience requirement: {skill.skill_name} ({skill.years_experience} years)")
        
        # Check for emerging technologies
        emerging_tech = ["AI", "Machine Learning", "Blockchain", "IoT", "Edge Computing"]
        for tech in emerging_tech:
            if tech.lower() in job_description.description.lower():
                skill_gaps.append(f"Emerging technology: {tech}")
        
        return skill_gaps
    
    def _analyze_industry_context(self, job_description: JobDescription) -> Dict[str, Any]:
        """Analyze industry context and trends"""
        industry_insights = {
            "primary_industry": job_description.company.industry,
            "technology_trends": job_description.technology_stack,
            "methodologies": job_description.methodologies,
            "remote_friendly": job_description.is_remote_friendly(),
            "company_size": job_description.company.size,
            "experience_level": job_description.experience_level
        }
        
        # Add industry-specific insights
        if "software" in job_description.company.industry.lower():
            industry_insights["industry_type"] = "technology"
            industry_insights["growth_rate"] = "high"
        elif "finance" in job_description.company.industry.lower():
            industry_insights["industry_type"] = "finance"
            industry_insights["growth_rate"] = "medium"
        else:
            industry_insights["industry_type"] = "general"
            industry_insights["growth_rate"] = "medium"
        
        return industry_insights
    
    def _analyze_company_culture(self, job_description: JobDescription) -> Dict[str, Any]:
        """Analyze company culture from job description"""
        culture_analysis = {
            "culture_keywords": job_description.company.culture_keywords,
            "remote_policy": job_description.company.remote_policy,
            "benefits_focus": [],
            "work_style": "traditional"
        }
        
        # Analyze benefits for culture insights
        benefits_text = " ".join(job_description.benefits + job_description.perks).lower()
        
        if "flexible" in benefits_text or "remote" in benefits_text:
            culture_analysis["work_style"] = "flexible"
        
        if "startup" in job_description.company.size.lower():
            culture_analysis["work_style"] = "fast-paced"
        
        if "health" in benefits_text or "insurance" in benefits_text:
            culture_analysis["benefits_focus"].append("healthcare")
        
        if "equity" in benefits_text or "stock" in benefits_text:
            culture_analysis["benefits_focus"].append("equity")
        
        return culture_analysis
    
    def _get_salary_benchmarks(self, job_description: JobDescription) -> Dict[str, Any]:
        """Get salary benchmarks for the role"""
        # This would typically integrate with salary data APIs
        # For now, return estimated ranges based on role and experience
        salary_benchmarks = {
            "estimated_range": job_description.salary_range,
            "market_average": "To be determined",
            "location_factor": 1.0,
            "experience_multiplier": 1.0
        }
        
        # Simple estimation based on experience level
        base_salaries = {
            "entry": 50000,
            "junior": 65000,
            "mid": 85000,
            "senior": 120000,
            "lead": 150000,
            "executive": 200000
        }
        
        level = job_description.experience_level.lower()
        if level in base_salaries:
            salary_benchmarks["estimated_base"] = base_salaries[level]
        
        return salary_benchmarks
    
    def _generate_suggestions(self, job_description: JobDescription, skill_gaps: List[str]) -> List[str]:
        """Generate suggestions for CV optimization"""
        suggestions = []
        
        # Skill-based suggestions
        if skill_gaps:
            suggestions.append(f"Consider highlighting experience with: {', '.join(skill_gaps[:3])}")
        
        # Experience level suggestions
        if job_description.experience_level.lower() in ["senior", "lead"]:
            suggestions.append("Emphasize leadership and project management experience")
        
        # Industry suggestions
        if job_description.company.industry:
            suggestions.append(f"Highlight relevant {job_description.company.industry} experience")
        
        # Remote work suggestions
        if job_description.is_remote_friendly():
            suggestions.append("Emphasize remote work experience and self-management skills")
        
        # Technology suggestions
        if job_description.technology_stack:
            suggestions.append(f"Prioritize experience with: {', '.join(job_description.technology_stack[:5])}")
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def get_keyword_importance(self, job_description: JobDescription) -> Dict[str, float]:
        """Calculate keyword importance scores"""
        keyword_importance = {}
        
        # Required skills get highest importance
        for skill in job_description.required_skills:
            keyword_importance[skill.skill_name.lower()] = 1.0
        
        # Preferred skills get medium importance
        for skill in job_description.preferred_skills:
            keyword_importance[skill.skill_name.lower()] = 0.7
        
        # Technology stack keywords
        for tech in job_description.technology_stack:
            keyword_importance[tech.lower()] = 0.8
        
        # Industry keywords
        for keyword in job_description.industry_keywords:
            keyword_importance[keyword.lower()] = 0.6
        
        return keyword_importance
    
    def extract_action_verbs(self, job_description: JobDescription) -> List[str]:
        """Extract action verbs from job description"""
        action_verbs = []
        
        # Common action verbs in job descriptions
        common_verbs = [
            "develop", "design", "implement", "manage", "lead", "create",
            "build", "maintain", "optimize", "analyze", "improve", "deliver",
            "coordinate", "collaborate", "communicate", "solve", "innovate"
        ]
        
        text = job_description.description.lower()
        for verb in common_verbs:
            if verb in text:
                action_verbs.append(verb)
        
        return action_verbs 