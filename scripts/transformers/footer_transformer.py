"""
Footer transformer for Contentful orFooter content type.
Transforms footer content to Jekyll YAML data files.
"""

from typing import Dict, Any, List, Set
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger, CONTENT_TYPE_FOOTER


class FooterTransformer(BaseTransformer):
    """
    Transforms Contentful footer entries to Jekyll YAML data.
    
    Handles menu items and social links with reference resolution.
    Outputs to _data/footer-{locale}.yml
    """
    
    def __init__(self, client, locale: str = 'en') -> None:
        """
        Initialize footer transformer.
        
        Args:
            client: ContentfulClient instance
            locale: Locale code
        """
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_FOOTER
    
    def _resolve_menu_items(
        self,
        menu_entries: List[Entry],
        visited: Set[str]
    ) -> List[Dict[str, Any]]:
        """
        Resolve menu item entries with circular reference protection.
        
        Args:
            menu_entries: List of menu item entries
            visited: Set of visited entry IDs
        
        Returns:
            List of menu item dictionaries
        """
        menu_items = []
        
        for menu_entry in menu_entries:
            # Circular reference protection
            if menu_entry.id in visited:
                logger.warning(
                    f"⚠️ CIRCULAR_REFERENCE_DETECTED "
                    f"entry_id={menu_entry.id} "
                    f"skipping"
                )
                continue
            
            visited.add(menu_entry.id)
            
            try:
                menu_fields = menu_entry.fields(
                    locale=self.locale,
                    fallback_locale=self.fallback_locale
                )
                
                label = menu_fields.get('label', '')  # Localized
                url = menu_fields.get('url', '')
                
                if label and url:
                    menu_items.append({
                        'label': label,
                        'url': url,
                        'external': url.startswith('http')
                    })
            except Exception as e:
                logger.warning(
                    f"⚠️ MENU_ITEM_FAILED "
                    f"entry_id={menu_entry.id} "
                    f"error={str(e)}"
                )
        
        return menu_items
    
    def _resolve_social_links(
        self,
        social_entries: List[Entry]
    ) -> List[Dict[str, Any]]:
        """
        Resolve social link entries.
        
        Args:
            social_entries: List of social link entries
        
        Returns:
            List of social link dictionaries
        """
        social_links = []
        
        for social_entry in social_entries:
            try:
                social_fields = social_entry.fields(
                    locale=self.locale,
                    fallback_locale=self.fallback_locale
                )
                
                platform = social_fields.get('platform', '')
                url = social_fields.get('url', '')
                
                if platform and url:
                    social_links.append({
                        'platform': platform,
                        'url': url
                    })
            except Exception as e:
                logger.warning(
                    f"⚠️ SOCIAL_LINK_FAILED "
                    f"entry_id={social_entry.id} "
                    f"error={str(e)}"
                )
        
        return social_links
    
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        """
        Transform a single footer entry.
        
        Args:
            entry: Contentful footer entry
        
        Returns:
            YAML-ready dictionary
        """
        fields = entry.fields(
            locale=self.locale,
            fallback_locale=self.fallback_locale
        )
        
        # Extract brand
        brand_url = fields.get('brandUrl', '/')
        brand_logo_url = ''
        brand_image = fields.get('brandImage')
        if brand_image:
            brand_logo_url = self.get_asset_url(brand_image)
        
        # Extract description and copyright
        description = fields.get('description', '')
        copyright = fields.get('copyright', '')
        
        # Resolve menu items with circular reference tracking
        visited_ids: Set[str] = set()
        menu_entries = self.resolve_reference_array(entry, 'menuItems')
        menu_items = self._resolve_menu_items(menu_entries, visited_ids)
        
        # Resolve social links
        social_entries = self.resolve_reference_array(entry, 'socialLinks')
        social_links = self._resolve_social_links(social_entries)
        
        # Build YAML data structure
        footer_data = {
            'brand_url': brand_url,
            'brand_logo_url': brand_logo_url,
            'description': description,
            'copyright': copyright,
            'menu_items': menu_items,
            'social_links': social_links
        }
        
        # Remove empty fields
        footer_data = {
            k: v for k, v in footer_data.items()
            if v
        }
        
        self.log_transform_success(
            entry,
            f"menu_items={len(menu_items)} social_links={len(social_links)}"
        )
        
        return footer_data
    
    def transform_all(self) -> List[Dict[str, Any]]:
        """
        Transform footer entry (singleton).
        
        Returns:
            List with single footer dictionary
        """
        logger.info(
            f"📊 TRANSFORM_FOOTER "
            f"locale={self.locale}"
        )
        
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=2  # Include menu items and social links
            )
            
            if not entries:
                logger.warning(
                    f"⚠️ NO_FOOTER_FOUND "
                    f"locale={self.locale}"
                )
                return []
            
            # Transform first entry only (singleton)
            footer_data = self.transform_single(entries[0])
            
            if len(entries) > 1:
                logger.warning(
                    f"⚠️ MULTIPLE_FOOTERS_FOUND "
                    f"count={len(entries)} "
                    f"using_first=true"
                )
            
            return [footer_data]
            
        except Exception as e:
            logger.error(
                f"❌ FOOTER_TRANSFORM_FAILED "
                f"locale={self.locale} "
                f"error={str(e)}"
            )
            return []
