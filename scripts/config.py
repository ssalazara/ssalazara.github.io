"""
Configuration module for Contentful to Jekyll transformation.
Loads environment variables, validates settings, and configures logging.
"""

import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# ============================================================================
# Configuration Constants
# ============================================================================

CONTENTFUL_SPACE_ID: str = os.getenv('CONTENTFUL_SPACE_ID', '')
CONTENTFUL_ACCESS_TOKEN: str = os.getenv('CONTENTFUL_ACCESS_TOKEN', '')
CONTENTFUL_PREVIEW_TOKEN: str = os.getenv('CONTENTFUL_PREVIEW_TOKEN', '')
CONTENTFUL_MODE: str = os.getenv('CONTENTFUL_MODE', 'production')

# Supported locales
SUPPORTED_LOCALES: list[str] = ['en', 'es']

# Content type IDs
CONTENT_TYPE_BLOG_POST: str = 'blogTemplate'
CONTENT_TYPE_PROFILE: str = 'profile'
CONTENT_TYPE_HEADER: str = 'orHeader'
CONTENT_TYPE_FOOTER: str = 'orFooter'


# ============================================================================
# Logging Configuration
# ============================================================================

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure structured logging with emoji markers.
    
    Args:
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('contentful_to_jekyll')
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create console handler with custom format
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Format: [LEVEL] message
    formatter = logging.Formatter(
        fmt='[%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


# Create default logger
logger = setup_logging()


# ============================================================================
# Configuration Validation
# ============================================================================

def validate_config() -> None:
    """
    Validate required environment variables are set.
    
    Raises:
        EnvironmentError: If required variables are missing
    """
    missing_vars: list[str] = []
    
    # Check Space ID
    if not CONTENTFUL_SPACE_ID:
        missing_vars.append('CONTENTFUL_SPACE_ID')
    
    # Check tokens based on mode
    if CONTENTFUL_MODE == 'production':
        if not CONTENTFUL_ACCESS_TOKEN:
            missing_vars.append('CONTENTFUL_ACCESS_TOKEN')
    elif CONTENTFUL_MODE == 'preview':
        if not CONTENTFUL_PREVIEW_TOKEN:
            missing_vars.append('CONTENTFUL_PREVIEW_TOKEN')
    else:
        logger.warning(
            f"⚠️ UNKNOWN_MODE mode={CONTENTFUL_MODE} "
            f"defaulting to 'production'"
        )
    
    # Raise error if missing required variables
    if missing_vars:
        missing_str = ', '.join(missing_vars)
        raise EnvironmentError(
            f"❌ CONFIG_ERROR: Missing required environment variables: {missing_str}\n"
            f"Create a .env file with these variables or set them in your environment.\n"
            f"See .env.example for template."
        )
    
    # Log successful configuration (without sensitive values)
    logger.info(
        f"✅ CONFIG_LOADED "
        f"space_id={CONTENTFUL_SPACE_ID} "
        f"mode={CONTENTFUL_MODE} "
        f"locales={SUPPORTED_LOCALES}"
    )


def get_active_token() -> str:
    """
    Get the appropriate API token based on current mode.
    
    Returns:
        Delivery or Preview API token
    
    Raises:
        EnvironmentError: If token not configured
    """
    if CONTENTFUL_MODE == 'preview':
        if not CONTENTFUL_PREVIEW_TOKEN:
            raise EnvironmentError("CONTENTFUL_PREVIEW_TOKEN not set")
        return CONTENTFUL_PREVIEW_TOKEN
    else:
        if not CONTENTFUL_ACCESS_TOKEN:
            raise EnvironmentError("CONTENTFUL_ACCESS_TOKEN not set")
        return CONTENTFUL_ACCESS_TOKEN


# ============================================================================
# Initialization
# ============================================================================

# Validate configuration on import
try:
    validate_config()
except EnvironmentError as e:
    logger.error(str(e))
    sys.exit(1)
