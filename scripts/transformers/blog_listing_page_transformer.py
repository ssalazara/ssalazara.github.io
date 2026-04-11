"""
Blog listing page transformer for Contentful blogListingPage content type.
Outputs to _data/blog-page-{locale}.yml
"""

from typing import Dict, Any, List
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger

CONTENT_TYPE_BLOG_LISTING = 'blogListingPage'


class BlogListingPageTransformer(BaseTransformer):
    """
    Transforms Contentful blogListingPage entries to Jekyll YAML data files.
    
    Extracts hero banner, SEO metadata, title, and description for
    the /blog/ archive page.
    """
    
    def __init__(self, client, locale: str = 'en') -> None:
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_BLOG_LISTING

    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        fields = entry.fields()
        
        # Extract hero banner if linked
        hero_data = {}
        hero_ref = self.resolve_reference(entry, 'hero')
        if hero_ref:
            hb_fields = hero_ref.fields()
            image_url = ''
            if hb_fields.get('image'):
                image_url = self.get_asset_url(hb_fields['image'])
            hero_data = {
                'title': hb_fields.get('title', ''),
                'description': hb_fields.get('description', ''),
                'cta_label': hb_fields.get('cta_label', ''),
                'cta_url': hb_fields.get('cta_url', ''),
                'image_url': image_url
            }
            hero_data = {k: v for k, v in hero_data.items() if v}
        
        # Extract SEO
        seo_data = {}
        seo_ref = self.resolve_reference(entry, 'seo')
        if seo_ref:
            seo_fields = seo_ref.fields()
            og_image = ''
            if seo_fields.get('ogImage'):
                og_image = self.get_asset_url(seo_fields['ogImage'])
            seo_data = {
                'title': seo_fields.get('title', ''),
                'description': seo_fields.get('description', ''),
                'og_image': og_image
            }
            seo_data = {k: v for k, v in seo_data.items() if v}
        
        title = fields.get('title', 'Blog')
        description = fields.get('description', '')
        
        # If no hero data from Contentful, build minimal hero from fields
        if not hero_data:
            hero_data = {
                'title': title,
                'description': description
            }
            hero_data = {k: v for k, v in hero_data.items() if v}
        
        self.log_transform_success(entry, f"title={title}")
        
        return {
            'hero': hero_data,
            'seo': seo_data
        }

    def transform_all(self) -> List[Dict[str, Any]]:
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=3
            )
            if not entries:
                logger.warning(f"⚠️ NO_BLOG_LISTING_PAGE locale={self.locale}")
                return []
            return [self.transform_single(entries[0])]
        except Exception as e:
            logger.error(f"❌ BLOG_LISTING_TRANSFORM_FAILED error={str(e)}")
            return []
