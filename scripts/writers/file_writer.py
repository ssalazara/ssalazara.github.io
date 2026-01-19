"""
File writer for Jekyll markdown blog posts.
Writes posts with YAML frontmatter to locale-specific folders.
"""

import os
import re
from datetime import datetime
from typing import Dict, Any
import frontmatter

from scripts.config import logger


class FileWriter:
    """
    Writes Jekyll markdown files with YAML frontmatter.
    
    Handles:
    - Locale folder creation (_posts/en/, _posts/es/)
    - Filename generation (YYYY-MM-DD-slug.md)
    - YAML frontmatter serialization
    - Date and slug validation
    """
    
    def __init__(self, base_path: str = '.') -> None:
        """
        Initialize file writer.
        
        Args:
            base_path: Base directory path (default: current directory)
        """
        self.base_path = base_path
        self.posts_dir = os.path.join(base_path, '_posts')
    
    def _validate_slug(self, slug: str) -> str:
        """
        Validate and sanitize slug for filename.
        
        Args:
            slug: Original slug
        
        Returns:
            Sanitized kebab-case slug
        """
        if not slug:
            return 'untitled'
        
        # Convert to lowercase
        slug = slug.lower()
        
        # Replace spaces with hyphens
        slug = slug.replace(' ', '-')
        
        # Remove non-alphanumeric characters except hyphens
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Strip leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug if slug else 'untitled'
    
    def _extract_date_prefix(self, publish_date: str) -> str:
        """
        Extract YYYY-MM-DD prefix from ISO 8601 date.
        
        Args:
            publish_date: ISO 8601 date string
        
        Returns:
            YYYY-MM-DD string
        """
        if not publish_date:
            # Use current date as fallback
            logger.warning("⚠️ MISSING_PUBLISH_DATE using current date")
            return datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Extract first 10 characters (YYYY-MM-DD)
            date_str = publish_date[:10]
            
            # Validate format
            datetime.strptime(date_str, '%Y-%m-%d')
            
            return date_str
            
        except (ValueError, IndexError) as e:
            logger.warning(
                f"⚠️ INVALID_PUBLISH_DATE "
                f"date={publish_date} "
                f"error={str(e)} "
                f"using_current_date=true"
            )
            return datetime.now().strftime('%Y-%m-%d')
    
    def _ensure_locale_folder(self, locale: str) -> str:
        """
        Ensure locale-specific posts folder exists.
        
        Args:
            locale: Locale code
        
        Returns:
            Path to locale folder
        """
        locale_path = os.path.join(self.posts_dir, locale)
        
        if not os.path.exists(locale_path):
            os.makedirs(locale_path, exist_ok=True)
            logger.info(
                f"📁 FOLDER_CREATED "
                f"path={locale_path}"
            )
        
        return locale_path
    
    def write_blog_post(
        self,
        post_data: Dict[str, Any],
        locale: str
    ) -> None:
        """
        Write blog post to markdown file with frontmatter.
        
        Args:
            post_data: Dictionary with 'frontmatter' and 'body' keys
            locale: Locale code
        
        Raises:
            IOError: If file write fails
        """
        frontmatter_dict = post_data.get('frontmatter', {})
        body = post_data.get('body', '')
        
        # Extract and validate slug
        slug = frontmatter_dict.get('slug', '')
        slug = self._validate_slug(slug)
        
        # Extract and validate publish date
        publish_date = frontmatter_dict.get('publish_date', '')
        date_prefix = self._extract_date_prefix(publish_date)
        
        # Generate filename: YYYY-MM-DD-slug.md
        filename = f"{date_prefix}-{slug}.md"
        
        # Ensure locale folder exists
        locale_folder = self._ensure_locale_folder(locale)
        
        # Full file path
        file_path = os.path.join(locale_folder, filename)
        
        try:
            # Create frontmatter post
            post = frontmatter.Post(body, **frontmatter_dict)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            logger.info(
                f"✅ POST_WRITTEN "
                f"path={file_path} "
                f"locale={locale} "
                f"slug={slug}"
            )
            
        except Exception as e:
            logger.error(
                f"❌ WRITE_FAILED "
                f"path={file_path} "
                f"error={str(e)}"
            )
            raise IOError(f"Failed to write post: {str(e)}")
    
    def write_multiple_posts(
        self,
        posts_data: list[Dict[str, Any]],
        locale: str
    ) -> None:
        """
        Write multiple blog posts.
        
        Args:
            posts_data: List of post dictionaries
            locale: Locale code
        """
        success_count = 0
        failed_count = 0
        
        for post_data in posts_data:
            try:
                self.write_blog_post(post_data, locale)
                success_count += 1
            except Exception as e:
                logger.error(
                    f"❌ POST_WRITE_FAILED "
                    f"locale={locale} "
                    f"error={str(e)}"
                )
                failed_count += 1
        
        logger.info(
            f"📊 POSTS_WRITTEN "
            f"locale={locale} "
            f"success={success_count} "
            f"failed={failed_count}"
        )
