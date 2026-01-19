"""
Base transformer class for Contentful entries.
Provides common functionality for all transformers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from contentful.entry import Entry

from scripts.contentful_client.client import ContentfulClient
from scripts.config import logger


class BaseTransformer(ABC):
    """
    Abstract base class for content transformers.
    
    All transformers inherit from this class and implement
    transform_single() and transform_all() methods.
    
    Attributes:
        client: ContentfulClient instance
        locale: Locale code (e.g., 'en', 'es')
    """
    
    def __init__(self, client: ContentfulClient, locale: str = 'en') -> None:
        """
        Initialize transformer.
        
        Args:
            client: Configured ContentfulClient
            locale: Locale code
        """
        self.client = client
        self.locale = locale
        self.fallback_locale = 'en'  # Default fallback
        
        logger.info(
            f"✅ TRANSFORMER_INIT "
            f"type={self.__class__.__name__} "
            f"locale={locale}"
        )
    
    @abstractmethod
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        """
        Transform a single Contentful entry.
        
        Args:
            entry: Contentful Entry object
        
        Returns:
            Transformed data dictionary
        
        Raises:
            ValueError: If entry validation fails
        """
        pass
    
    @abstractmethod
    def transform_all(self) -> List[Dict[str, Any]]:
        """
        Transform all entries of this content type.
        
        Returns:
            List of transformed data dictionaries
        """
        pass
    
    def validate_required_fields(
        self,
        entry: Entry,
        fields: List[str]
    ) -> None:
        """
        Validate that required fields exist in entry.
        
        Args:
            entry: Contentful Entry object
            fields: List of required field names
        
        Raises:
            ValueError: If required field is missing
        """
        entry_fields = entry.fields()
        
        missing_fields = []
        for field in fields:
            if not entry_fields.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            missing_str = ', '.join(missing_fields)
            raise ValueError(
                f"❌ VALIDATION_FAILED "
                f"entry_id={entry.id} "
                f"missing_fields={missing_str}"
            )
    
    def get_asset_url(self, asset: Any) -> str:
        """
        Extract CDN URL from Contentful asset.
        
        Args:
            asset: Contentful Asset object
        
        Returns:
            CDN URL string or empty string if asset is None
        """
        if not asset:
            return ''
        
        try:
            # Contentful asset URL method
            url = asset.url()
            
            # Ensure HTTPS protocol
            if url and not url.startswith('https:'):
                url = f"https:{url}" if url.startswith('//') else url
            
            return url
        except Exception as e:
            logger.warning(
                f"⚠️ ASSET_URL_FAILED "
                f"error={str(e)}"
            )
            return ''
    
    def resolve_reference(
        self,
        entry: Entry,
        field_name: str
    ) -> Any:
        """
        Resolve a referenced entry field.
        
        Args:
            entry: Contentful Entry object
            field_name: Name of reference field
        
        Returns:
            Referenced entry or None if not found
        """
        entry_fields = entry.fields()
        
        referenced = entry_fields.get(field_name)
        
        if referenced and hasattr(referenced, 'id'):
            return referenced
        
        return None
    
    def resolve_reference_array(
        self,
        entry: Entry,
        field_name: str
    ) -> List[Entry]:
        """
        Resolve an array of referenced entries.
        
        Args:
            entry: Contentful Entry object
            field_name: Name of reference array field
        
        Returns:
            List of referenced entries
        """
        entry_fields = entry.fields()
        
        referenced_array = entry_fields.get(field_name, [])
        
        # Filter out None values and non-Entry objects
        valid_entries = [
            item for item in referenced_array
            if item and hasattr(item, 'id')
        ]
        
        return valid_entries
    
    def safe_get_field(
        self,
        entry: Entry,
        field_name: str,
        default: Any = None
    ) -> Any:
        """
        Safely get field value with fallback.
        
        Args:
            entry: Contentful Entry object
            field_name: Field name
            default: Default value if field missing
        
        Returns:
            Field value or default
        """
        try:
            entry_fields = entry.fields(
                locale=self.locale,
                fallback_locale=self.fallback_locale
            )
            return entry_fields.get(field_name, default)
        except Exception as e:
            logger.warning(
                f"⚠️ FIELD_ACCESS_FAILED "
                f"entry_id={entry.id} "
                f"field={field_name} "
                f"error={str(e)}"
            )
            return default
    
    def log_transform_success(
        self,
        entry: Entry,
        extra_info: str = ''
    ) -> None:
        """
        Log successful transformation.
        
        Args:
            entry: Transformed entry
            extra_info: Additional information
        """
        logger.info(
            f"✅ TRANSFORM_SUCCESS "
            f"entry_id={entry.id} "
            f"locale={self.locale} "
            f"{extra_info}"
        )
    
    def log_transform_error(
        self,
        entry: Entry,
        error: Exception
    ) -> None:
        """
        Log transformation error.
        
        Args:
            entry: Failed entry
            error: Exception that occurred
        """
        logger.error(
            f"❌ TRANSFORM_FAILED "
            f"entry_id={entry.id} "
            f"locale={self.locale} "
            f"error={str(error)}",
            exc_info=True
        )
