"""
Blog post transformer for Contentful blogTemplate content type.
Transforms blog posts to Jekyll markdown with frontmatter.
"""

from typing import Dict, Any, List
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.converters.markdown_converter import RichTextConverter
from scripts.config import logger, CONTENT_TYPE_BLOG_POST


class BlogPostTransformer(BaseTransformer):
    """
    Transforms Contentful blog posts to Jekyll markdown files.
    
    Validates SEO requirements before transformation.
    Converts RichText body to Markdown.
    Extracts featured images and metadata.
    """
    
    def __init__(self, client, locale: str = 'en') -> None:
        """
        Initialize blog post transformer.
        
        Args:
            client: ContentfulClient instance
            locale: Locale code
        """
        super().__init__(client, locale)
        self.markdown_converter = RichTextConverter()
        self.content_type = CONTENT_TYPE_BLOG_POST
    
    def validate_seo(self, entry: Entry) -> None:
        """
        Validate that entry has required SEO metadata.
        
        Args:
            entry: Blog post entry
        
        Raises:
            ValueError: If SEO entry missing or incomplete
        """
        # Get SEO entry reference
        seo_entry = self.resolve_reference(entry, 'seo')
        
        if not seo_entry:
            raise ValueError(
                f"❌ SEO_MISSING "
                f"entry_id={entry.id} "
                f"message='Blog post requires linked SEO entry'"
            )
        
        # Validate SEO fields
        seo_fields = seo_entry.fields()
        
        required_seo_fields = ['title', 'description']
        missing_fields = []
        
        for field in required_seo_fields:
            if not seo_fields.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            missing_str = ', '.join(missing_fields)
            raise ValueError(
                f"❌ SEO_INCOMPLETE "
                f"entry_id={entry.id} "
                f"seo_id={seo_entry.id} "
                f"missing_fields={missing_str}"
            )
    
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        """
        Transform a single blog post entry.
        
        Args:
            entry: Contentful blog post entry
        
        Returns:
            Dictionary with 'frontmatter' and 'body' keys
        
        Raises:
            ValueError: If validation fails
        """
        # Validate SEO FIRST (fail fast)
        self.validate_seo(entry)
        
        # Get entry fields
        fields = entry.fields()
        
        # Extract basic fields (Contentful camelCase → Jekyll snake_case)
        slug = fields.get('url', '')
        title = fields.get('title', '')
        excerpt = fields.get('description', '')
        category = fields.get('label', '')
        author = fields.get('author', '')
        publish_date = fields.get('publishDate', '')  # ISO 8601, no transformation
        
        # Extract featured image
        featured_image = ''
        image_asset = fields.get('image')
        if image_asset:
            featured_image = self.get_asset_url(image_asset)
        
        # Extract and convert Rich Text body
        body_markdown = ''
        rich_text_body = fields.get('text')
        if rich_text_body:
            try:
                body_markdown = self.markdown_converter.convert(rich_text_body)
            except Exception as e:
                logger.warning(
                    f"⚠️ RICHTEXT_CONVERSION_FAILED "
                    f"entry_id={entry.id} "
                    f"error={str(e)}"
                )
                body_markdown = '<!-- Rich text conversion failed -->'
        
        # Extract SEO fields
        seo_entry = self.resolve_reference(entry, 'seo')
        seo_fields = seo_entry.fields()
        
        seo_title = seo_fields.get('title', title)  # Fallback to post title
        seo_description = seo_fields.get('description', excerpt)  # Fallback to excerpt
        seo_keywords = seo_fields.get('keywords', [])
        
        # OG image
        og_image = ''
        og_image_asset = seo_fields.get('ogImage')
        if og_image_asset:
            og_image = self.get_asset_url(og_image_asset)
        elif featured_image:
            og_image = featured_image  # Fallback to featured image
        
        # Additional SEO fields
        canonical_url = seo_fields.get('canonicalUrl', '')
        no_index = seo_fields.get('noIndex', False)
        
        # Build frontmatter dictionary (all snake_case)
        frontmatter = {
            'layout': 'post-layout',
            'locale': self.locale,
            'slug': slug,
            'title': title,
            'excerpt': excerpt,
            'category': category,
            'author': author,
            'publish_date': publish_date,  # ISO 8601 preserved
            'featured_image': featured_image,
            'seo_title': seo_title,
            'seo_description': seo_description,
            'seo_keywords': seo_keywords,
            'og_image': og_image,
            'canonical_url': canonical_url,
            'no_index': no_index
        }
        
        # Remove empty fields
        frontmatter = {
            k: v for k, v in frontmatter.items()
            if v or isinstance(v, bool)  # Keep booleans even if False
        }
        
        self.log_transform_success(entry, f"slug={slug}")
        
        return {
            'frontmatter': frontmatter,
            'body': body_markdown
        }
    
    def transform_all(self) -> List[Dict[str, Any]]:
        """
        Transform all blog posts with graceful degradation.
        
        Returns:
            List of transformed blog post dictionaries
        """
        logger.info(
            f"📊 TRANSFORM_ALL_START "
            f"content_type={self.content_type} "
            f"locale={self.locale}"
        )
        
        # Fetch all blog post entries
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=2  # Include SEO and image references
            )
        except Exception as e:
            logger.error(
                f"❌ FETCH_FAILED "
                f"content_type={self.content_type} "
                f"locale={self.locale} "
                f"error={str(e)}"
            )
            return []
        
        # Transform with graceful degradation
        transformed = []
        failed_count = 0
        
        for entry in entries:
            try:
                post_data = self.transform_single(entry)
                transformed.append(post_data)
            except Exception as e:
                self.log_transform_error(entry, e)
                failed_count += 1
                # Continue with next entry
        
        # Summary
        total = len(entries)
        success_count = len(transformed)
        
        logger.info(
            f"📊 TRANSFORM_ALL_COMPLETE "
            f"content_type={self.content_type} "
            f"locale={self.locale} "
            f"total={total} "
            f"success={success_count} "
            f"failed={failed_count}"
        )
        
        return transformed
