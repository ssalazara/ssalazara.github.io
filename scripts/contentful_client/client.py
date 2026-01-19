"""
Dual-mode Contentful API client with in-memory caching.
Supports both Delivery API (production) and Preview API (draft content).
"""

import time
from typing import List, Optional, Dict, Any
from contentful import Client as ContentfulSDKClient
from contentful.entry import Entry

from scripts.config import logger, CONTENTFUL_MODE


class ContentfulClient:
    """
    Contentful API client with dual-mode support and in-memory caching.
    
    Attributes:
        space_id: Contentful space identifier
        access_token: API access token (Delivery or Preview)
        mode: 'production' (Delivery API) or 'preview' (Preview API)
        cache_ttl: Cache time-to-live in seconds (default: 300)
    """
    
    def __init__(
        self,
        space_id: str,
        access_token: str,
        mode: str = 'production',
        cache_ttl: int = 300
    ) -> None:
        """
        Initialize Contentful client with dual-mode support.
        
        Args:
            space_id: Contentful space ID
            access_token: Delivery or Preview API token
            mode: 'production' or 'preview'
            cache_ttl: Cache time-to-live in seconds
        """
        self.space_id = space_id
        self.access_token = access_token
        self.mode = mode
        self.cache_ttl = cache_ttl
        
        # In-memory cache: {cache_key: (entries, timestamp)}
        self._cache: Dict[str, tuple[List[Entry], float]] = {}
        
        # Initialize Contentful SDK client
        self._client = self._initialize_client()
        
        logger.info(
            f"✅ CLIENT_INITIALIZED "
            f"space_id={space_id} "
            f"mode={mode} "
            f"cache_ttl={cache_ttl}s"
        )
    
    def _initialize_client(self) -> ContentfulSDKClient:
        """
        Initialize Contentful SDK client based on mode.
        
        Returns:
            Configured Contentful SDK client
        """
        if self.mode == 'preview':
            # Preview API for draft content
            return ContentfulSDKClient(
                space_id=self.space_id,
                access_token=self.access_token,
                api_url='preview.contentful.com'
            )
        else:
            # Delivery API for published content (default)
            return ContentfulSDKClient(
                space_id=self.space_id,
                access_token=self.access_token
            )
    
    def _generate_cache_key(
        self,
        content_type: str,
        locale: str,
        include: int
    ) -> str:
        """
        Generate cache key for request.
        
        Args:
            content_type: Content type ID
            locale: Locale code
            include: Include depth
        
        Returns:
            Cache key string
        """
        return f"{content_type}:{locale}:{include}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """
        Check if cached data is still valid.
        
        Args:
            timestamp: Cache timestamp
        
        Returns:
            True if cache is valid, False if expired
        """
        return (time.time() - timestamp) < self.cache_ttl
    
    def get_entries(
        self,
        content_type: str,
        locale: str = 'en',
        include: int = 2
    ) -> List[Entry]:
        """
        Fetch entries from Contentful with caching.
        
        Args:
            content_type: Content type ID
            locale: Locale code (default: 'en')
            include: Reference include depth (default: 2)
        
        Returns:
            List of Contentful entries
        """
        cache_key = self._generate_cache_key(content_type, locale, include)
        
        # Check cache first
        if cache_key in self._cache:
            cached_entries, cached_time = self._cache[cache_key]
            
            if self._is_cache_valid(cached_time):
                logger.info(
                    f"✅ CACHE_HIT "
                    f"content_type={content_type} "
                    f"locale={locale} "
                    f"count={len(cached_entries)}"
                )
                return cached_entries
        
        # Cache miss or expired - fetch from API
        logger.info(
            f"📡 API_CALL "
            f"content_type={content_type} "
            f"locale={locale} "
            f"include={include}"
        )
        
        try:
            # Fetch entries from Contentful
            entries = self._client.entries({
                'content_type': content_type,
                'locale': locale,
                'include': include
            })
            
            # Convert to list
            entries_list = list(entries)
            
            # Cache the results
            self._cache[cache_key] = (entries_list, time.time())
            
            logger.info(
                f"✅ API_SUCCESS "
                f"content_type={content_type} "
                f"locale={locale} "
                f"count={len(entries_list)}"
            )
            
            return entries_list
            
        except Exception as e:
            logger.error(
                f"❌ API_FAILED "
                f"content_type={content_type} "
                f"locale={locale} "
                f"error={str(e)}"
            )
            raise
    
    def get_entry(
        self,
        entry_id: str,
        locale: str = 'en'
    ) -> Optional[Entry]:
        """
        Fetch a single entry by ID.
        
        Args:
            entry_id: Entry identifier
            locale: Locale code
        
        Returns:
            Entry or None if not found
        """
        try:
            entry = self._client.entry(entry_id, {'locale': locale})
            
            logger.info(
                f"✅ ENTRY_FETCHED "
                f"entry_id={entry_id} "
                f"locale={locale}"
            )
            
            return entry
            
        except Exception as e:
            logger.error(
                f"❌ ENTRY_FAILED "
                f"entry_id={entry_id} "
                f"locale={locale} "
                f"error={str(e)}"
            )
            return None
    
    def clear_cache(self) -> None:
        """
        Clear the in-memory cache.
        Useful for testing or when fresh data is required.
        """
        cache_size = len(self._cache)
        self._cache.clear()
        
        logger.info(
            f"🗑️ CACHE_CLEARED "
            f"entries_removed={cache_size}"
        )
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        total_entries = sum(
            len(entries) for entries, _ in self._cache.values()
        )
        
        return {
            'cached_requests': len(self._cache),
            'total_cached_entries': total_entries,
            'cache_ttl': self.cache_ttl
        }
