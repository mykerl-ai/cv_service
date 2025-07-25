"""
File processing utilities for the CV writer service
"""
import os
import re
import logging
from typing import List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class FileProcessor:
    """Handles file operations and validation"""
    
    def __init__(self, max_file_size: int = 10 * 1024 * 1024):  # 10MB default
        self.max_file_size = max_file_size
        self.allowed_extensions = [".pdf", ".docx", ".doc", ".txt"]
        self.allowed_mime_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
            "text/plain"
        ]
    
    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate file for processing"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return False, f"File size ({file_size} bytes) exceeds maximum allowed size ({self.max_file_size} bytes)"
            
            # Check file extension
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.allowed_extensions:
                return False, f"File extension '{file_extension}' is not supported. Allowed: {', '.join(self.allowed_extensions)}"
            
            # Check if file is readable
            if not os.access(file_path, os.R_OK):
                return False, "File is not readable"
            
            return True, "File is valid"
            
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {str(e)}")
            return False, f"Error validating file: {str(e)}"
    
    def get_file_info(self, file_path: str) -> dict:
        """Get file information"""
        try:
            file_stat = os.stat(file_path)
            file_path_obj = Path(file_path)
            
            return {
                "name": file_path_obj.name,
                "extension": file_path_obj.suffix.lower(),
                "size": file_stat.st_size,
                "size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                "created": file_stat.st_ctime,
                "modified": file_stat.st_mtime,
                "is_readable": os.access(file_path, os.R_OK),
                "is_writable": os.access(file_path, os.W_OK)
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return {}
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove or replace unsafe characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip('. ')
        
        # Limit length
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:255-len(ext)] + ext
        
        return sanitized
    
    def create_safe_filename(self, base_name: str, extension: str, job_title: str = "") -> str:
        """Create a safe filename for output files"""
        # Sanitize components
        safe_base = self.sanitize_filename(base_name)
        safe_job = self.sanitize_filename(job_title) if job_title else ""
        safe_ext = extension.lower() if extension.startswith('.') else f".{extension.lower()}"
        
        # Create filename
        if safe_job:
            filename = f"{safe_base}_{safe_job}{safe_ext}"
        else:
            filename = f"{safe_base}{safe_ext}"
        
        # Ensure uniqueness by adding timestamp if needed
        timestamp = int(os.path.getmtime(__file__))  # Use current timestamp
        filename = f"{os.path.splitext(filename)[0]}_{timestamp}{safe_ext}"
        
        return filename
    
    def ensure_directory_exists(self, directory_path: str) -> bool:
        """Ensure directory exists, create if it doesn't"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory_path}: {str(e)}")
            return False
    
    def cleanup_temp_files(self, directory: str, pattern: str = "*", max_age_hours: int = 24) -> int:
        """Clean up temporary files older than specified age"""
        import time
        import glob
        
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            cleaned_count = 0
            
            # Find files matching pattern
            search_pattern = os.path.join(directory, pattern)
            files = glob.glob(search_pattern)
            
            for file_path in files:
                try:
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        cleaned_count += 1
                        logger.info(f"Cleaned up old file: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not clean up file {file_path}: {str(e)}")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return 0
    
    def get_file_extension(self, file_path: str) -> str:
        """Get file extension"""
        return Path(file_path).suffix.lower()
    
    def is_pdf_file(self, file_path: str) -> bool:
        """Check if file is a PDF"""
        return self.get_file_extension(file_path) == ".pdf"
    
    def is_docx_file(self, file_path: str) -> bool:
        """Check if file is a DOCX"""
        return self.get_file_extension(file_path) == ".docx"
    
    def is_doc_file(self, file_path: str) -> bool:
        """Check if file is a DOC"""
        return self.get_file_extension(file_path) == ".doc"
    
    def is_text_file(self, file_path: str) -> bool:
        """Check if file is a text file"""
        return self.get_file_extension(file_path) in [".txt", ".md", ".rtf"]
    
    def get_mime_type(self, file_path: str) -> Optional[str]:
        """Get MIME type of file"""
        import mimetypes
        
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            return mime_type
        except Exception as e:
            logger.error(f"Error getting MIME type for {file_path}: {str(e)}")
            return None
    
    def validate_mime_type(self, file_path: str) -> bool:
        """Validate MIME type of file"""
        mime_type = self.get_mime_type(file_path)
        return mime_type in self.allowed_mime_types if mime_type else False
    
    def extract_text_from_file(self, file_path: str) -> Optional[str]:
        """Extract text content from file"""
        try:
            if self.is_pdf_file(file_path):
                return self._extract_text_from_pdf(file_path)
            elif self.is_docx_file(file_path):
                return self._extract_text_from_docx(file_path)
            elif self.is_doc_file(file_path):
                return self._extract_text_from_doc(file_path)
            elif self.is_text_file(file_path):
                return self._extract_text_from_text(file_path)
            else:
                logger.error(f"Unsupported file type: {file_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return None
    
    def _extract_text_from_pdf(self, file_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return None
    
    def _extract_text_from_docx(self, file_path: str) -> Optional[str]:
        """Extract text from DOCX file"""
        try:
            import docx
            
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
            return None
    
    def _extract_text_from_doc(self, file_path: str) -> Optional[str]:
        """Extract text from DOC file"""
        try:
            # This would require additional libraries like python-docx2txt or similar
            # For now, return None as DOC files are less common
            logger.warning("DOC file extraction not implemented")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting text from DOC {file_path}: {str(e)}")
            return None
    
    def _extract_text_from_text(self, file_path: str) -> Optional[str]:
        """Extract text from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
                
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Error reading text file {file_path} with latin-1 encoding: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Error extracting text from text file {file_path}: {str(e)}")
            return None
    
    def save_file_safely(self, content: bytes, file_path: str) -> bool:
        """Save file content safely with error handling"""
        try:
            # Ensure directory exists
            directory = os.path.dirname(file_path)
            if directory and not self.ensure_directory_exists(directory):
                return False
            
            # Write file atomically
            temp_path = f"{file_path}.tmp"
            with open(temp_path, 'wb') as f:
                f.write(content)
            
            # Rename to final path
            os.replace(temp_path, file_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {str(e)}")
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            return False
    
    def copy_file_safely(self, source_path: str, dest_path: str) -> bool:
        """Copy file safely with error handling"""
        try:
            # Ensure destination directory exists
            dest_directory = os.path.dirname(dest_path)
            if dest_directory and not self.ensure_directory_exists(dest_directory):
                return False
            
            # Copy file
            import shutil
            shutil.copy2(source_path, dest_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Error copying file from {source_path} to {dest_path}: {str(e)}")
            return False
    
    def get_file_hash(self, file_path: str, algorithm: str = "md5") -> Optional[str]:
        """Get file hash for integrity checking"""
        import hashlib
        
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {str(e)}")
            return None 