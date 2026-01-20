"""
Homepage transformer for Contentful homePage content type.
Transforms homepage entries with dynamic blocks to Jekyll YAML data files.
"""

from typing import Dict, Any, List, Set
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger, CONTENT_TYPE_HOMEPAGE
from scripts.writers.data_writer import DataWriter


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
        self.header_data = None
        self.footer_data = None
    
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
            elif content_type_id == 'componentSkillsList':
                return self._transform_skills_list(block_entry, fields)
            elif content_type_id == 'componentProjectsGrid':
                return self._transform_projects_grid(block_entry, fields)
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
    
    def _transform_skills_list(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform skills list block.
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Skills list data dictionary
        """
        skills_data = {
            'type': 'skillsList',
            'name': fields.get('name', ''),
            'title': fields.get('title', ''),
            'items': fields.get('skills', [])
        }
        
        # Remove empty optional fields
        skills_data = {k: v for k, v in skills_data.items() if v or k == 'type'}
        
        logger.info(
            f"✅ SKILLS_LIST_TRANSFORMED "
            f"entry_id={entry.id} "
            f"skills_count={len(fields.get('skills', []))}"
        )
        
        return skills_data
    
    def _transform_projects_grid(self, entry: Entry, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform projects grid block.
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Projects grid data dictionary
        """
        # Resolve project cards
        project_cards_entries = self.resolve_reference_array(entry, 'projects')
        projects = []
        
        for project_entry in project_cards_entries:
            try:
                project_fields = project_entry.fields()
                
                # Extract image URL
                image_url = ''
                image_asset = project_fields.get('image')
                if image_asset:
                    image_url = self.get_asset_url(image_asset)
                
                project_data = {
                    'title': project_fields.get('title', ''),
                    'description': project_fields.get('description', ''),
                    'url': project_fields.get('url', '#'),
                    'image_url': image_url,
                    'external': project_fields.get('external', False)
                }
                
                # Remove empty optional fields except external (boolean)
                project_data = {k: v for k, v in project_data.items() if v or k == 'external'}
                
                projects.append(project_data)
                
            except Exception as e:
                logger.error(
                    f"❌ PROJECT_CARD_TRANSFORM_FAILED "
                    f"entry_id={project_entry.id} "
                    f"error={str(e)}"
                )
        
        projects_grid_data = {
            'type': 'projectsGrid',
            'name': fields.get('name', ''),
            'title': fields.get('title', ''),
            'items': projects
        }
        
        # Remove empty optional fields
        projects_grid_data = {k: v for k, v in projects_grid_data.items() if v or k == 'type'}
        
        logger.info(
            f"✅ PROJECTS_GRID_TRANSFORMED "
            f"entry_id={entry.id} "
            f"projects_count={len(projects)}"
        )
        
        return projects_grid_data
    
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
        Transform text-with-image block.
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Text with image data dictionary
        """
        # Extract image asset
        image_url = ''
        image_asset = fields.get('image')
        if image_asset:
            image_url = self.get_asset_url(image_asset)
        
        # Extract rich text description
        description_text = ''
        description_rich_text = fields.get('description')
        if description_rich_text:
            # Extract plain text from Contentful rich text structure
            description_text = self._extract_text_from_rich_text(description_rich_text)
        
        text_with_image_data = {
            'type': 'textWithImage',
            'name': fields.get('name', ''),
            'title': fields.get('title', ''),
            'description': description_text,
            'image_url': image_url,
            'image_on_right': fields.get('image_on_right', False)
        }
        
        # Remove empty optional fields except booleans
        text_with_image_data = {
            k: v for k, v in text_with_image_data.items() 
            if v or k in ['type', 'image_on_right']
        }
        
        logger.info(
            f"✅ TEXT_WITH_IMAGE_TRANSFORMED "
            f"entry_id={entry.id} "
            f"has_image={bool(image_url)} "
            f"has_title={bool(fields.get('title'))}"
        )
        
        return text_with_image_data
    
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
        Transform quote block.
        
        Args:
            entry: Contentful Entry
            fields: Entry fields dictionary
        
        Returns:
            Quote data dictionary
        """
        # Extract author photo asset
        image_url = ''
        image_asset = fields.get('image')
        if image_asset:
            image_url = self.get_asset_url(image_asset)
        
        quote_data = {
            'type': 'quote',
            'name': fields.get('name', ''),
            'quote': fields.get('quote', ''),
            'author': fields.get('author', ''),
            'role': fields.get('role', ''),
            'image_url': image_url
        }
        
        # Remove empty optional fields
        quote_data = {k: v for k, v in quote_data.items() if v or k == 'type'}
        
        logger.info(
            f"✅ QUOTE_TRANSFORMED "
            f"entry_id={entry.id} "
            f"has_image={bool(image_url)} "
            f"has_author={bool(fields.get('author'))}"
        )
        
        return quote_data
    
    def _extract_text_from_rich_text(self, rich_text_obj: Any) -> str:
        """
        Extract plain text from Contentful rich text structure.
        
        Args:
            rich_text_obj: Contentful rich text object
        
        Returns:
            Plain text string with paragraphs separated by newlines
        """
        if not rich_text_obj:
            return ''
        
        try:
            # Rich text is a nested structure with content array
            content_items = []
            
            # Handle dict-like structure
            if hasattr(rich_text_obj, 'get'):
                content = rich_text_obj.get('content', [])
            elif hasattr(rich_text_obj, '__getitem__'):
                content = rich_text_obj.get('content', [])
            else:
                # Try to access as attribute
                content = getattr(rich_text_obj, 'content', [])
            
            for node in content:
                if hasattr(node, 'get') or hasattr(node, '__getitem__'):
                    node_type = node.get('nodeType', '') if hasattr(node, 'get') else node['nodeType']
                    
                    if node_type == 'paragraph':
                        # Extract text from paragraph content
                        para_content = node.get('content', []) if hasattr(node, 'get') else node['content']
                        para_text = []
                        
                        for text_node in para_content:
                            if hasattr(text_node, 'get'):
                                if text_node.get('nodeType') == 'text':
                                    para_text.append(text_node.get('value', ''))
                            elif hasattr(text_node, '__getitem__'):
                                if text_node['nodeType'] == 'text':
                                    para_text.append(text_node['value'])
                        
                        if para_text:
                            content_items.append(''.join(para_text))
            
            return '\n\n'.join(content_items)
            
        except Exception as e:
            logger.warning(
                f"⚠️ RICH_TEXT_EXTRACTION_FAILED "
                f"error={str(e)} "
                f"returning_empty_string"
            )
            return ''
    
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
                menu_fields = menu_entry.fields()
                
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
    
    def _extract_header(self, homepage_entry: Entry) -> Dict[str, Any]:
        """
        Extract header data from homepage entry.
        
        Args:
            homepage_entry: Homepage entry containing header reference
        
        Returns:
            Header data dictionary
        """
        fields = homepage_entry.fields()
        header_ref = fields.get('header')
        
        if not header_ref:
            logger.warning(f"⚠️ NO_HEADER_REFERENCE in homepage")
            return {'brand_url': '/'}
        
        try:
            header_fields = header_ref.fields()
            
            # Extract brand (note: SDK converts camelCase to snake_case)
            brand_url = header_fields.get('brand_url', '/')
            brand_logo_url = ''
            brand_image = header_fields.get('brand_image')
            if brand_image:
                brand_logo_url = self.get_asset_url(brand_image)
            
            # Resolve menu items with circular reference tracking
            # Note: Contentful SDK converts camelCase to snake_case
            visited_ids: Set[str] = set()
            menu_entries = self.resolve_reference_array(header_ref, 'menu_items')
            menu_items = self._resolve_menu_items(menu_entries, visited_ids)
            
            # Resolve top links (if present)
            visited_ids_top: Set[str] = set()
            top_link_entries = self.resolve_reference_array(header_ref, 'top_links')
            top_links = self._resolve_menu_items(top_link_entries, visited_ids_top)
            
            # Build header data structure
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
            
            logger.info(
                f"✅ HEADER_EXTRACTED "
                f"entry_id={header_ref.id} "
                f"menu_items_count={len(menu_items)}"
            )
            
            return header_data
            
        except Exception as e:
            logger.error(
                f"❌ HEADER_EXTRACTION_FAILED "
                f"error={str(e)}"
            )
            return {'brand_url': '/'}
    
    def _extract_footer(self, homepage_entry: Entry) -> Dict[str, Any]:
        """
        Extract footer data from homepage entry.
        
        Args:
            homepage_entry: Homepage entry containing footer reference
        
        Returns:
            Footer data dictionary
        """
        fields = homepage_entry.fields()
        footer_ref = fields.get('footer')
        
        if not footer_ref:
            logger.warning(f"⚠️ NO_FOOTER_REFERENCE in homepage")
            return {'brand_url': '/'}
        
        try:
            footer_fields = footer_ref.fields()
            
            # Extract brand (note: SDK converts camelCase to snake_case)
            brand_url = footer_fields.get('brand_url', '/')
            brand_logo_url = ''
            brand_image = footer_fields.get('brand_image')
            if brand_image:
                brand_logo_url = self.get_asset_url(brand_image)
            
            # Extract description and copyright
            description = footer_fields.get('description', '')
            copyright_text = footer_fields.get('copyright', '')
            
            # Resolve menu items with circular reference tracking
            # Note: Contentful SDK converts camelCase to snake_case
            visited_ids: Set[str] = set()
            menu_entries = self.resolve_reference_array(footer_ref, 'menu_items')
            menu_items = self._resolve_menu_items(menu_entries, visited_ids)
            
            # Build footer data structure
            footer_data = {
                'brand_url': brand_url,
                'brand_logo_url': brand_logo_url,
                'description': description,
                'copyright': copyright_text,
                'nav_links': menu_items  # Using nav_links to match footer template expectations
            }
            
            # Remove empty fields
            footer_data = {
                k: v for k, v in footer_data.items()
                if v
            }
            
            logger.info(
                f"✅ FOOTER_EXTRACTED "
                f"entry_id={footer_ref.id} "
                f"menu_items_count={len(menu_items)}"
            )
            
            return footer_data
            
        except Exception as e:
            logger.error(
                f"❌ FOOTER_EXTRACTION_FAILED "
                f"error={str(e)}"
            )
            return {'brand_url': '/'}
    
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
        
        # Extract header and footer (store for later writing to separate files)
        self.header_data = self._extract_header(entry)
        self.footer_data = self._extract_footer(entry)
        
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
    
    def get_header_data(self) -> Dict[str, Any]:
        """Get extracted header data."""
        return self.header_data or {'brand_url': '/'}
    
    def get_footer_data(self) -> Dict[str, Any]:
        """Get extracted footer data."""
        return self.footer_data or {'brand_url': '/'}
    
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
                include=10  # Deep include for header/footer menu items + blocks
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
