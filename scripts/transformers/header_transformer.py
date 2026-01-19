"""
Header transformer for Contentful orHeader content type.
Transforms header navigation to Jekyll YAML data files.
"""

from typing import Dict, Any, List, Set
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger, CONTENT_TYPE_HEADER


class HeaderTransformer(BaseTransformer):
    """
    Transforms Contentful header entries to Jekyll YAML data.
    
    Handles menu item references with circular reference protection.
    Outputs to _data/header-{locale}.yml
    """
    
    def __init__(self, client, locale: str = 'en') -> None:
        """
        Initialize header transformer.
        
        Args:
            client: ContentfulClient instance
            locale: Locale code
        """
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_HEADER
    
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
    
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        """
        Transform a single header entry.
        
        Args:
            entry: Contentful header entry
        
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
        
        # Resolve menu items with circular reference tracking
        visited_ids: Set[str] = set()
        menu_entries = self.resolve_reference_array(entry, 'menuItems')
        menu_items = self._resolve_menu_items(menu_entries, visited_ids)
        
        # Resolve top links (if present)
        visited_ids_top: Set[str] = set()
        top_link_entries = self.resolve_reference_array(entry, 'topLinks')
        top_links = self._resolve_menu_items(top_link_entries, visited_ids_top)
        
        # Build YAML data structure
        header_data = {
            'brand_url': brand_url,
            'brand_logo_url': brand_logo_url,
            'menu_items': menu_items,
            'top_links': top_links
        }
        
        # Remove empty fields
        header_data = {
            k: v for k, v in header_data.items()
            if v
        }
        
        self.log_transform_success(
            entry,
            f"menu_items_count={len(menu_items)}"
        )
        
        return header_data
    
    def transform_all(self) -> List[Dict[str, Any]]:
        """
        Transform header entry (singleton).
        
        Returns:
            List with single header dictionary
        """
        logger.info(
            f"📊 TRANSFORM_HEADER "
            f"locale={self.locale}"
        )
        
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=2  # Include menu items
            )
            
            if not entries:
                logger.warning(
                    f"⚠️ NO_HEADER_FOUND "
                    f"locale={self.locale}"
                )
                return []
            
            # Transform first entry only (singleton)
            header_data = self.transform_single(entries[0])
            
            if len(entries) > 1:
                logger.warning(
                    f"⚠️ MULTIPLE_HEADERS_FOUND "
                    f"count={len(entries)} "
                    f"using_first=true"
                )
            
            return [header_data]
            
        except Exception as e:
            logger.error(
                f"❌ HEADER_TRANSFORM_FAILED "
                f"locale={self.locale} "
                f"error={str(e)}"
            )
            return []
