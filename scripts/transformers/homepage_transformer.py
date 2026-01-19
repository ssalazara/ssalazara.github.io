"""
Homepage transformer for Contentful homePage content type.
Transforms homepage entries with dynamic blocks to Jekyll YAML data files.
"""

from typing import Dict, Any, List
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger, CONTENT_TYPE_HOMEPAGE


class HomepageTransformer(BaseTransformer):
    """
    Transforms Contentful homepage entries to Jekyll YAML data.
    
    Handles dynamic content blocks (hero banner, carousels, text-with-image, etc.)
    with graceful fallback for unsupported block types.
    
    Outputs to _data/homepage-{locale}.yml
    """
    
    def __init__(self, client, locale: str = 'en') -> None:
        """
        Initialize homepage transformer.
        
        Args:
            client: ContentfulClient instance
            locale: Locale code
        """
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_HOMEPAGE
    
    def _transform_block(self, block_entry: Entry) -> Dict[str, Any]:
        """
        Transform a single content block based on its type.
        
        Args:
            block_entry: Contentful Entry for a block component
        
        Returns:
            Dictionary with 'type' field and transformed block data
        """
        try:
            # Extract content type ID from entry's content_type attribute
            content_type_id = 'unknown'
            if hasattr(block_entry, 'content_type') and hasattr(block_entry.content_type, 'id'):
                content_type_id = block_entry.content_type.id
            
            fields = block_entry.fields()
            
            # Transform based on block type
            if content_type_id == 'heroBanner':
                return self._transform_hero_banner(block_entry, fields)
            elif content_type_id == 'componentRichText':
                return self._transform_rich_text(block_entry, fields)
            elif content_type_id == 'textWithImage':
                return self._transform_text_with_image(block_entry, fields)
            elif content_type_id == 'componentCarousel':
                return self._transform_carousel(block_entry, fields)
            elif content_type_id == 'componentQuote':
                return self._transform_quote(block_entry, fields)
            else:
                logger.warning(
                    f"⚠️ UNSUPPORTED_BLOCK_TYPE "
                    f"entry_id={block_entry.id} "
                    f"type={content_type_id}"
                )
                return {
                    'type': 'unsupported',
                    'content_type': content_type_id,
                    'entry_id': block_entry.id
                }
        
        except Exception as e:
            logger.error(
                f"❌ BLOCK_TRANSFORM_FAILED "
                f"entry_id={block_entry.id} "
                f"error={str(e)}"
            )
            return {
                'type': 'error',
                'entry_id': block_entry.id,
                'error': str(e)
            }
    
    def _transform_hero_banner(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform hero banner block.
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Hero banner data dictionary
        """
        # Extract image asset
        image_url = ''
        image_asset = fields.get('image')
        if image_asset:
            image_url = self.get_asset_url(image_asset)
        
        hero_data = {
            'type': 'heroBanner',
            'name': fields.get('name', ''),
            'title': fields.get('title', ''),
            'description': fields.get('description', ''),
            'cta_label': fields.get('cta_label', ''),
            'cta_url': fields.get('cta_url', ''),
            'image_url': image_url
        }
        
        # Remove empty optional fields
        hero_data = {k: v for k, v in hero_data.items() if v or k == 'type'}
        
        logger.info(
            f"✅ HERO_BANNER_TRANSFORMED "
            f"entry_id={entry.id} "
            f"has_image={bool(image_url)} "
            f"has_cta={bool(fields.get('cta_label'))}"
        )
        
        return hero_data
    
    def _transform_rich_text(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform rich text block (placeholder for future implementation).
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Placeholder data dictionary
        """
        logger.warning(
            f"⚠️ RICH_TEXT_NOT_IMPLEMENTED "
            f"entry_id={entry.id}"
        )
        return {
            'type': 'richText',
            'entry_id': entry.id,
            'placeholder': True
        }
    
    def _transform_text_with_image(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform text-with-image block (placeholder for future implementation).
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Placeholder data dictionary
        """
        logger.warning(
            f"⚠️ TEXT_WITH_IMAGE_NOT_IMPLEMENTED "
            f"entry_id={entry.id}"
        )
        return {
            'type': 'textWithImage',
            'entry_id': entry.id,
            'placeholder': True
        }
    
    def _transform_carousel(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform carousel block (placeholder for future implementation).
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Placeholder data dictionary
        """
        logger.warning(
            f"⚠️ CAROUSEL_NOT_IMPLEMENTED "
            f"entry_id={entry.id}"
        )
        return {
            'type': 'carousel',
            'entry_id': entry.id,
            'placeholder': True
        }
    
    def _transform_quote(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform quote block (placeholder for future implementation).
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Placeholder data dictionary
        """
        logger.warning(
            f"⚠️ QUOTE_NOT_IMPLEMENTED "
            f"entry_id={entry.id}"
        )
        return {
            'type': 'quote',
            'entry_id': entry.id,
            'placeholder': True
        }
    
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        """
        Transform a single homepage entry.
        
        Args:
            entry: Contentful homepage entry
        
        Returns:
            YAML-ready dictionary
        """
        fields = entry.fields()
        
        # Extract basic fields
        name = fields.get('name', '')
        url = fields.get('url', '/')
        
        # Resolve blocks array
        block_entries = self.resolve_reference_array(entry, 'blocks')
        blocks = []
        
        for block_entry in block_entries:
            transformed_block = self._transform_block(block_entry)
            
            # Only include successfully transformed blocks
            if transformed_block.get('type') not in ['error', 'unsupported']:
                blocks.append(transformed_block)
            elif transformed_block.get('type') == 'unsupported':
                # Log but continue - graceful degradation
                logger.warning(
                    f"⚠️ SKIPPING_UNSUPPORTED_BLOCK "
                    f"content_type={transformed_block.get('content_type')}"
                )
        
        # Build homepage data structure
        homepage_data = {
            'name': name,
            'url': url,
            'blocks': blocks
        }
        
        self.log_transform_success(
            entry,
            f"blocks_count={len(blocks)}"
        )
        
        return homepage_data
    
    def transform_all(self) -> List[Dict[str, Any]]:
        """
        Transform homepage entry (singleton).
        
        Returns:
            List with single homepage dictionary
        """
        logger.info(
            f"📊 TRANSFORM_HOMEPAGE "
            f"locale={self.locale}"
        )
        
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=2  # Include blocks and their references
            )
            
            if not entries:
                logger.warning(
                    f"⚠️ NO_HOMEPAGE_FOUND "
                    f"locale={self.locale}"
                )
                return []
            
            # Transform first entry only (singleton)
            homepage_data = self.transform_single(entries[0])
            
            if len(entries) > 1:
                logger.warning(
                    f"⚠️ MULTIPLE_HOMEPAGES_FOUND "
                    f"count={len(entries)} "
                    f"using_first=true"
                )
            
            return [homepage_data]
            
        except Exception as e:
            logger.error(
                f"❌ HOMEPAGE_TRANSFORM_FAILED "
                f"locale={self.locale} "
                f"error={str(e)}"
            )
            return []
