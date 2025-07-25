"""
CV optimizer for the smart CV writer service
"""
import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from difflib import SequenceMatcher

from openai import OpenAI

from ..models.cv_data import CVData, EmploymentDetail, Skill, Project, CVOptimizationResult
from ..models.job_data import JobDescription, JobAnalysisResult

logger = logging.getLogger(__name__)


class CVOptimizer:
    """Main CV optimization engine"""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo", temperature: float = 0.1):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)
        
    def optimize_cv(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> CVOptimizationResult:
        """Optimize CV to match job description"""
        start_time = datetime.now()
        
        try:
            # Create a copy of the original CV
            original_cv = cv_data
            
            # Apply optimizations
            optimized_cv = self._apply_optimizations(cv_data, job_analysis)
            
            # Calculate optimization score
            optimization_score = self._calculate_optimization_score(optimized_cv, job_analysis)
            
            # Generate improvements list
            improvements = self._generate_improvements_list(original_cv, optimized_cv, job_analysis)
            
            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(optimized_cv, job_analysis)
            
            # Calculate keyword matches
            keyword_matches = self._calculate_keyword_matches(optimized_cv, job_analysis)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return CVOptimizationResult(
                original_cv=original_cv,
                optimized_cv=optimized_cv,
                optimization_score=optimization_score,
                improvements_made=improvements,
                skill_gaps_identified=skill_gaps,
                keyword_matches=keyword_matches,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error optimizing CV: {str(e)}")
            raise
    
    def _apply_optimizations(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> CVData:
        """Apply all optimization strategies"""
        optimized_cv = cv_data
        
        # 1. Optimize summary
        optimized_cv.summary = self._optimize_summary(cv_data.summary, job_analysis)
        
        # 2. Optimize skills
        optimized_cv.technical_skills = self._optimize_skills(cv_data.technical_skills, job_analysis, "technical")
        optimized_cv.soft_skills = self._optimize_skills(cv_data.soft_skills, job_analysis, "soft")
        
        # 3. Optimize employment history
        optimized_cv.employment_history = self._optimize_employment_history(cv_data.employment_history, job_analysis)
        
        # 4. Optimize projects
        optimized_cv.projects = self._optimize_projects(cv_data.projects, job_analysis)
        
        # 5. Add missing skills
        self._add_missing_skills(optimized_cv, job_analysis)
        
        # 6. Optimize keywords
        self._optimize_keywords(optimized_cv, job_analysis)
        
        # Update metadata
        optimized_cv.optimization_date = datetime.now()
        optimized_cv.target_job_title = job_analysis.job_description.title
        optimized_cv.target_company = job_analysis.job_description.company.name
        
        return optimized_cv
    
    def _optimize_summary(self, summary: str, job_analysis: JobAnalysisResult) -> str:
        """Optimize professional summary for the job"""
        if not summary:
            return self._generate_summary(job_analysis)
        
        system_prompt = """
        You are an expert CV writer. Optimize the provided professional summary to better match the job requirements.
        
        Guidelines:
        1. Keep it concise (2-3 sentences, max 200 words)
        2. Highlight relevant skills and experience
        3. Use action verbs and keywords from the job description
        4. Emphasize achievements and impact
        5. Match the tone and style of the job description
        6. Include industry-specific terminology
        
        Return only the optimized summary text.
        """
        
        job_context = f"""
        Job Title: {job_analysis.job_description.title}
        Company: {job_analysis.job_description.company.name}
        Required Skills: {', '.join([s.skill_name for s in job_analysis.job_description.required_skills])}
        Preferred Skills: {', '.join([s.skill_name for s in job_analysis.job_description.preferred_skills])}
        Experience Level: {job_analysis.job_description.experience_level}
        Industry: {job_analysis.job_description.company.industry}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Job Context:\n{job_context}\n\nCurrent Summary:\n{summary}"}
                ],
                temperature=self.temperature,
                max_tokens=300
            )
            
            optimized_summary = response.choices[0].message.content.strip()
            return optimized_summary if optimized_summary else summary
            
        except Exception as e:
            logger.error(f"Error optimizing summary: {str(e)}")
            return summary
    
    def _generate_summary(self, job_analysis: JobAnalysisResult) -> str:
        """Generate a new professional summary based on job requirements"""
        system_prompt = """
        Generate a compelling professional summary for a CV that matches the job requirements.
        
        Guidelines:
        1. 2-3 sentences, max 200 words
        2. Highlight relevant skills and experience
        3. Use action verbs and keywords from the job description
        4. Emphasize achievements and impact
        5. Match the tone and style of the job description
        6. Include industry-specific terminology
        
        Return only the summary text.
        """
        
        job_context = f"""
        Job Title: {job_analysis.job_description.title}
        Company: {job_analysis.job_description.company.name}
        Required Skills: {', '.join([s.skill_name for s in job_analysis.job_description.required_skills])}
        Preferred Skills: {', '.join([s.skill_name for s in job_analysis.job_description.preferred_skills])}
        Experience Level: {job_analysis.job_description.experience_level}
        Industry: {job_analysis.job_description.company.industry}
        Responsibilities: {'; '.join(job_analysis.job_description.responsibilities[:5])}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Job Context:\n{job_context}"}
                ],
                temperature=self.temperature,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Experienced professional with strong technical skills and proven track record of delivering results."
    
    def _optimize_skills(self, skills: List[Skill], job_analysis: JobAnalysisResult, category: str) -> List[Skill]:
        """Optimize skills list for the job"""
        if not skills:
            return skills
        
        # Calculate relevance scores for existing skills
        for skill in skills:
            skill.relevance_score = self._calculate_skill_relevance(skill.name, job_analysis)
        
        # Sort skills by relevance
        skills.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Limit to top skills (configurable)
        max_skills = 15 if category == "technical" else 10
        optimized_skills = skills[:max_skills]
        
        # Enhance skill descriptions with keywords
        for skill in optimized_skills:
            skill.keywords = self._extract_skill_keywords(skill.name, job_analysis)
        
        return optimized_skills
    
    def _calculate_skill_relevance(self, skill_name: str, job_analysis: JobAnalysisResult) -> float:
        """Calculate relevance score for a skill"""
        job_desc = job_analysis.job_description
        skill_lower = skill_name.lower()
        
        # Check required skills (highest weight)
        for skill in job_desc.required_skills:
            if skill_lower in skill.skill_name.lower() or skill.skill_name.lower() in skill_lower:
                return 1.0
        
        # Check preferred skills (medium weight)
        for skill in job_desc.preferred_skills:
            if skill_lower in skill.skill_name.lower() or skill.skill_name.lower() in skill_lower:
                return 0.8
        
        # Check technology stack
        for tech in job_desc.technology_stack:
            if skill_lower in tech.lower() or tech.lower() in skill_lower:
                return 0.7
        
        # Check keywords
        for keyword in job_desc.keywords:
            if skill_lower in keyword.lower() or keyword.lower() in skill_lower:
                return 0.6
        
        # Check for related skills
        related_skills = self._get_related_skills(skill_name)
        for related in related_skills:
            for skill in job_desc.required_skills + job_desc.preferred_skills:
                if related.lower() in skill.skill_name.lower():
                    return 0.5
        
        return 0.1  # Default low relevance
    
    def _get_related_skills(self, skill_name: str) -> List[str]:
        """Get related skills for a given skill"""
        skill_relationships = {
            "python": ["django", "flask", "fastapi", "pandas", "numpy"],
            "javascript": ["react", "vue", "angular", "node.js", "typescript"],
            "aws": ["ec2", "s3", "lambda", "cloudformation"],
            "docker": ["kubernetes", "containerization"],
            "sql": ["postgresql", "mysql", "sqlite", "database"],
            "git": ["github", "gitlab", "version control"],
            "machine learning": ["tensorflow", "pytorch", "scikit-learn", "ml"],
        }
        
        skill_lower = skill_name.lower()
        for main_skill, related in skill_relationships.items():
            if skill_lower in main_skill or main_skill in skill_lower:
                return related
            for related_skill in related:
                if skill_lower in related_skill or related_skill in skill_lower:
                    return related
        
        return []
    
    def _extract_skill_keywords(self, skill_name: str, job_analysis: JobAnalysisResult) -> List[str]:
        """Extract relevant keywords for a skill"""
        keywords = []
        job_desc = job_analysis.job_description
        
        # Add skill name variations
        keywords.append(skill_name)
        
        # Add related keywords from job description
        for keyword in job_desc.keywords:
            if skill_name.lower() in keyword.lower() or keyword.lower() in skill_name.lower():
                keywords.append(keyword)
        
        return list(set(keywords))[:5]  # Limit to 5 keywords
    
    def _optimize_employment_history(self, employment_history: List[EmploymentDetail], job_analysis: JobAnalysisResult) -> List[EmploymentDetail]:
        """Optimize employment history for the job"""
        if not employment_history:
            return employment_history
        
        optimized_history = []
        
        for job in employment_history:
            # Calculate relevance score
            job.relevance_score = self._calculate_job_relevance(job, job_analysis)
            
            # Optimize job description and achievements
            optimized_job = self._optimize_job_description(job, job_analysis)
            optimized_history.append(optimized_job)
        
        # Sort by relevance score
        optimized_history.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Limit to most relevant jobs
        max_jobs = 8  # Configurable
        return optimized_history[:max_jobs]
    
    def _calculate_job_relevance(self, job: EmploymentDetail, job_analysis: JobAnalysisResult) -> float:
        """Calculate relevance score for a job position"""
        job_desc = job_analysis.job_description
        job_text = f"{job.position} {' '.join(job.description)} {' '.join(job.achievements)}".lower()
        
        relevance_score = 0.0
        
        # Check job title similarity
        title_similarity = SequenceMatcher(None, job.position.lower(), job_desc.title.lower()).ratio()
        relevance_score += title_similarity * 0.3
        
        # Check for required skills in job description
        for skill in job_desc.required_skills:
            if skill.skill_name.lower() in job_text:
                relevance_score += 0.2
        
        # Check for technology stack
        for tech in job_desc.technology_stack:
            if tech.lower() in job_text:
                relevance_score += 0.1
        
        # Check for industry keywords
        for keyword in job_desc.industry_keywords:
            if keyword.lower() in job_text:
                relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    def _optimize_job_description(self, job: EmploymentDetail, job_analysis: JobAnalysisResult) -> EmploymentDetail:
        """Optimize individual job description and achievements"""
        system_prompt = """
        Optimize the job description and achievements to better match the job requirements.
        
        Guidelines:
        1. Use action verbs from the job description
        2. Include relevant keywords and skills
        3. Quantify achievements where possible
        4. Emphasize impact and results
        5. Match the tone and style of the job description
        6. Keep descriptions concise and impactful
        
        Return as JSON:
        {
          "description": ["optimized description 1", "optimized description 2"],
          "achievements": ["optimized achievement 1", "optimized achievement 2"]
        }
        """
        
        job_context = f"""
        Job Title: {job_analysis.job_description.title}
        Required Skills: {', '.join([s.skill_name for s in job_analysis.job_description.required_skills])}
        Technology Stack: {', '.join(job_analysis.job_description.technology_stack)}
        Action Verbs: {', '.join(job_analysis.job_description.keywords)}
        """
        
        current_content = f"""
        Position: {job.position}
        Company: {job.company}
        Current Description: {'; '.join(job.description)}
        Current Achievements: {'; '.join(job.achievements)}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Job Context:\n{job_context}\n\nCurrent Job:\n{current_content}"}
                ],
                temperature=self.temperature,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if content:
                data = json.loads(content)
                job.description = data.get("description", job.description)
                job.achievements = data.get("achievements", job.achievements)
            
        except Exception as e:
            logger.error(f"Error optimizing job description: {str(e)}")
        
        return job
    
    def _optimize_projects(self, projects: List[Project], job_analysis: JobAnalysisResult) -> List[Project]:
        """Optimize projects for the job"""
        if not projects:
            return projects
        
        optimized_projects = []
        
        for project in projects:
            # Calculate relevance score
            project_text = f"{project.name} {project.description} {' '.join(project.technologies)}".lower()
            relevance_score = 0.0
            
            # Check for required skills
            for skill in job_analysis.job_description.required_skills:
                if skill.skill_name.lower() in project_text:
                    relevance_score += 0.3
            
            # Check for technology stack
            for tech in job_analysis.job_description.technology_stack:
                if tech.lower() in project_text:
                    relevance_score += 0.2
            
            # Only include relevant projects
            if relevance_score > 0.3:
                optimized_projects.append(project)
        
        # Sort by relevance and limit
        optimized_projects.sort(key=lambda x: x.relevance_score, reverse=True)
        return optimized_projects[:5]  # Limit to 5 most relevant projects
    
    def _add_missing_skills(self, cv_data: CVData, job_analysis: JobAnalysisResult):
        """Add missing but relevant skills to the CV"""
        existing_skills = cv_data.get_all_skills()
        missing_skills = []
        
        # Check for missing required skills
        for skill_req in job_analysis.job_description.required_skills:
            if not any(skill_req.skill_name.lower() in existing.lower() for existing in existing_skills):
                missing_skills.append(skill_req)
        
        # Add missing skills with appropriate proficiency levels
        for skill_req in missing_skills[:5]:  # Limit to 5 missing skills
            new_skill = Skill(
                name=skill_req.skill_name,
                category=skill_req.category,
                proficiency="intermediate",  # Default to intermediate
                relevance_score=1.0,  # High relevance for required skills
                keywords=[skill_req.skill_name]
            )
            cv_data.add_skill(new_skill)
    
    def _optimize_keywords(self, cv_data: CVData, job_analysis: JobAnalysisResult):
        """Optimize keyword distribution throughout the CV"""
        # This would implement keyword density optimization
        # For now, we'll just track keyword matches
        job_keywords = job_analysis.job_description.keywords
        cv_text = f"{cv_data.summary} {' '.join(cv_data.get_all_skills())}"
        
        keyword_matches = {}
        for keyword in job_keywords:
            count = cv_text.lower().count(keyword.lower())
            if count > 0:
                keyword_matches[keyword] = count
        
        cv_data.keyword_matches = keyword_matches
    
    def _calculate_optimization_score(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> float:
        """Calculate overall optimization score"""
        score = 0.0
        
        # Skill match score (40% weight)
        skill_score = self._calculate_skill_match_score(cv_data, job_analysis)
        score += skill_score * 0.4
        
        # Experience relevance score (30% weight)
        experience_score = self._calculate_experience_relevance_score(cv_data, job_analysis)
        score += experience_score * 0.3
        
        # Keyword match score (20% weight)
        keyword_score = self._calculate_keyword_match_score(cv_data, job_analysis)
        score += keyword_score * 0.2
        
        # Summary optimization score (10% weight)
        summary_score = self._calculate_summary_optimization_score(cv_data, job_analysis)
        score += summary_score * 0.1
        
        return min(score, 100.0)
    
    def _calculate_skill_match_score(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> float:
        """Calculate skill match score"""
        required_skills = job_analysis.job_description.required_skills
        cv_skills = cv_data.get_all_skills()
        
        if not required_skills:
            return 100.0
        
        matched_skills = 0
        for skill_req in required_skills:
            if any(skill_req.skill_name.lower() in cv_skill.lower() for cv_skill in cv_skills):
                matched_skills += 1
        
        return (matched_skills / len(required_skills)) * 100
    
    def _calculate_experience_relevance_score(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> float:
        """Calculate experience relevance score"""
        if not cv_data.employment_history:
            return 0.0
        
        total_relevance = sum(job.relevance_score for job in cv_data.employment_history)
        avg_relevance = total_relevance / len(cv_data.employment_history)
        
        return avg_relevance * 100
    
    def _calculate_keyword_match_score(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> float:
        """Calculate keyword match score"""
        job_keywords = job_analysis.job_description.keywords
        if not job_keywords:
            return 100.0
        
        cv_text = f"{cv_data.summary} {' '.join(cv_data.get_all_skills())}".lower()
        matched_keywords = 0
        
        for keyword in job_keywords:
            if keyword.lower() in cv_text:
                matched_keywords += 1
        
        return (matched_keywords / len(job_keywords)) * 100
    
    def _calculate_summary_optimization_score(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> float:
        """Calculate summary optimization score"""
        if not cv_data.summary:
            return 0.0
        
        summary_lower = cv_data.summary.lower()
        job_keywords = job_analysis.job_description.keywords
        required_skills = [s.skill_name for s in job_analysis.job_description.required_skills]
        
        keyword_matches = sum(1 for keyword in job_keywords if keyword.lower() in summary_lower)
        skill_matches = sum(1 for skill in required_skills if skill.lower() in summary_lower)
        
        total_expected = len(job_keywords) + len(required_skills)
        if total_expected == 0:
            return 100.0
        
        return ((keyword_matches + skill_matches) / total_expected) * 100
    
    def _generate_improvements_list(self, original_cv: CVData, optimized_cv: CVData, job_analysis: JobAnalysisResult) -> List[str]:
        """Generate list of improvements made"""
        improvements = []
        
        # Summary improvements
        if original_cv.summary != optimized_cv.summary:
            improvements.append("Professional summary optimized for job requirements")
        
        # Skill improvements
        if len(optimized_cv.technical_skills) > len(original_cv.technical_skills):
            improvements.append("Added missing technical skills")
        
        # Experience improvements
        if optimized_cv.employment_history != original_cv.employment_history:
            improvements.append("Job descriptions enhanced with relevant keywords and achievements")
        
        # Keyword improvements
        if optimized_cv.keyword_matches:
            improvements.append("Improved keyword distribution for ATS optimization")
        
        return improvements
    
    def _identify_skill_gaps(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> List[str]:
        """Identify remaining skill gaps"""
        cv_skills = cv_data.get_all_skills()
        skill_gaps = []
        
        for skill_req in job_analysis.job_description.required_skills:
            if not any(skill_req.skill_name.lower() in cv_skill.lower() for cv_skill in cv_skills):
                skill_gaps.append(skill_req.skill_name)
        
        return skill_gaps
    
    def _calculate_keyword_matches(self, cv_data: CVData, job_analysis: JobAnalysisResult) -> Dict[str, int]:
        """Calculate keyword matches in the CV"""
        return cv_data.keyword_matches 