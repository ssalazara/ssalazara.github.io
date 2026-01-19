"""
Profile transformer for Contentful profile content type.
Transforms profile data to Jekyll YAML data files.
"""

from typing import Dict, Any, List
from contentful.entry import Entry

from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger, CONTENT_TYPE_PROFILE


class ProfileTransformer(BaseTransformer):
    """
    Transforms Contentful profile entries to Jekyll YAML data.
    
    Profile is a singleton content type (only one instance).
    Outputs to _data/profile-{locale}.yml
    """
    
    def __init__(self, client, locale: str = 'en') -> None:
        """
        Initialize profile transformer.
        
        Args:
            client: ContentfulClient instance
            locale: Locale code
        """
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_PROFILE
    
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        """
        Transform a single profile entry.
        
        Args:
            entry: Contentful profile entry
        
        Returns:
            YAML-ready dictionary
        """
        fields = entry.fields(
            locale=self.locale,
            fallback_locale=self.fallback_locale
        )
        
        # Extract basic fields
        full_name = fields.get('fullName', '')
        title = fields.get('title', '')  # Localized
        bio = fields.get('bio', '')  # Localized
        email = fields.get('email', '')
        
        # Extract profile image
        photo_url = ''
        profile_image = fields.get('profileImage')
        if profile_image:
            photo_url = self.get_asset_url(profile_image)
        
        # Extract social links (referenced entries)
        social_links = []
        social_link_entries = self.resolve_reference_array(entry, 'socialLinks')
        
        for social_entry in social_link_entries:
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
        
        # Extract CTA button
        cta_label = fields.get('ctaLabel', '')  # Localized
        cta_url = fields.get('ctaUrl', '')
        
        cta_button = {}
        if cta_label and cta_url:
            cta_button = {
                'text': cta_label,
                'url': cta_url,
                'external': cta_url.startswith('http')
            }
        
        # Build YAML data structure
        profile_data = {
            'name': full_name,
            'title': title,
            'bio': bio,
            'email': email,
            'photo_url': photo_url,
            'social_links': social_links,
            'cta_button': cta_button
        }
        
        # Remove empty fields
        profile_data = {
            k: v for k, v in profile_data.items()
            if v
        }
        
        self.log_transform_success(entry, f"name={full_name}")
        
        return profile_data
    
    def transform_all(self) -> List[Dict[str, Any]]:
        """
        Transform profile entry (singleton).
        
        Returns:
            List with single profile dictionary
        """
        logger.info(
            f"📊 TRANSFORM_PROFILE "
            f"locale={self.locale}"
        )
        
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=2  # Include social links
            )
            
            if not entries:
                logger.warning(
                    f"⚠️ NO_PROFILE_FOUND "
                    f"locale={self.locale}"
                )
                return []
            
            # Transform first entry only (singleton)
            profile_data = self.transform_single(entries[0])
            
            if len(entries) > 1:
                logger.warning(
                    f"⚠️ MULTIPLE_PROFILES_FOUND "
                    f"count={len(entries)} "
                    f"using_first=true"
                )
            
            return [profile_data]
            
        except Exception as e:
            logger.error(
                f"❌ PROFILE_TRANSFORM_FAILED "
                f"locale={self.locale} "
                f"error={str(e)}"
            )
            return []
