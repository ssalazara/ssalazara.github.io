#!/usr/bin/env python3
"""
Main orchestration script for Contentful → Jekyll transformation.

Fetches content from Contentful, transforms to Jekyll format, and writes files.
Supports dual-mode operation (production/preview).
"""

import sys
import time
from typing import Dict, Any

# Import configuration and clients
from scripts.config import (
    logger,
    CONTENTFUL_SPACE_ID,
    CONTENTFUL_MODE,
    SUPPORTED_LOCALES,
    get_active_token,
    get_jekyll_locale
)
from scripts.contentful_client.client import ContentfulClient

# Import transformers
from scripts.transformers.blog_post_transformer import BlogPostTransformer
from scripts.transformers.profile_transformer import ProfileTransformer
from scripts.transformers.header_transformer import HeaderTransformer
from scripts.transformers.footer_transformer import FooterTransformer
from scripts.transformers.homepage_transformer import HomepageTransformer

# Import writers
from scripts.writers.file_writer import FileWriter
from scripts.writers.data_writer import DataWriter


def main() -> int:
    """
    Main entry point for transformation script.
    
    Returns:
        Exit code (0 = success, 1 = failure)
    """
    start_time = time.time()
    
    logger.info("🚀 BUILD_START")
    logger.info(
        f"📊 BUILD_CONFIG "
        f"space_id={CONTENTFUL_SPACE_ID} "
        f"mode={CONTENTFUL_MODE} "
        f"locales={SUPPORTED_LOCALES}"
    )
    
    # Get active token based on mode
    try:
        access_token = get_active_token()
    except Exception as e:
        logger.error(f"❌ CONFIG_ERROR: {str(e)}")
        return 1
    
    # Initialize Contentful client
    try:
        client = ContentfulClient(
            space_id=CONTENTFUL_SPACE_ID,
            access_token=access_token,
            mode=CONTENTFUL_MODE
        )
    except Exception as e:
        logger.error(f"❌ CLIENT_INIT_FAILED: {str(e)}")
        return 1
    
    # Initialize writers
    file_writer = FileWriter()
    data_writer = DataWriter()
    
    # Track statistics
    stats: Dict[str, Any] = {
        'total_entries': 0,
        'successful_transformations': 0,
        'failed_transformations': 0,
        'locales_processed': []
    }
    
    # Process each locale
    for locale in SUPPORTED_LOCALES:
        logger.info(f"\n📍 LOCALE_START locale={locale}")
        
        try:
            # Process locale
            locale_stats = process_locale(
                client,
                locale,
                file_writer,
                data_writer
            )
            
            # Aggregate statistics
            stats['total_entries'] += locale_stats['total_entries']
            stats['successful_transformations'] += locale_stats['successful']
            stats['failed_transformations'] += locale_stats['failed']
            stats['locales_processed'].append(locale)
            
            logger.info(
                f"✅ LOCALE_COMPLETE "
                f"locale={locale} "
                f"success={locale_stats['successful']} "
                f"failed={locale_stats['failed']}"
            )
            
        except Exception as e:
            logger.error(
                f"❌ LOCALE_FAILED "
                f"locale={locale} "
                f"error={str(e)}"
            )
            stats['failed_transformations'] += 1
    
    # Calculate build duration
    duration = time.time() - start_time
    
    # Build time monitoring
    if duration > 240:  # 4 minutes (critical threshold)
        logger.error(
            f"❌ BUILD_CRITICAL "
            f"duration={duration:.1f}s "
            f"threshold=240s "
            f"message='Approaching 5min limit, investigate caching/API calls'"
        )
    elif duration > 120:  # 2 minutes (warning threshold)
        logger.warning(
            f"⚠️ BUILD_SLOW "
            f"duration={duration:.1f}s "
            f"target=120s"
        )
    
    # Final summary
    logger.info(
        f"\n📊 BUILD_COMPLETE "
        f"duration={duration:.1f}s "
        f"total_entries={stats['total_entries']} "
        f"successful={stats['successful_transformations']} "
        f"failed={stats['failed_transformations']} "
        f"locales={stats['locales_processed']}"
    )
    
    # Determine exit code based on failure threshold
    exit_code = calculate_exit_code(stats)
    
    return exit_code


def process_locale(
    client: ContentfulClient,
    locale: str,
    file_writer: FileWriter,
    data_writer: DataWriter
) -> Dict[str, int]:
    """
    Process all content for a single locale.
    
    Args:
        client: Contentful client instance
        locale: Contentful locale code (e.g., 'en-US')
        file_writer: File writer instance
        data_writer: Data writer instance
    
    Returns:
        Statistics dictionary with success/failure counts
    """
    stats = {
        'total_entries': 0,
        'successful': 0,
        'failed': 0
    }
    
    # Map Contentful locale to Jekyll folder name
    jekyll_locale = get_jekyll_locale(locale)
    
    # Initialize transformers for this locale
    blog_transformer = BlogPostTransformer(client, locale)
    profile_transformer = ProfileTransformer(client, locale)
    header_transformer = HeaderTransformer(client, locale)
    footer_transformer = FooterTransformer(client, locale)
    homepage_transformer = HomepageTransformer(client, locale)
    
    # Transform blog posts
    logger.info(f"📝 Transforming blog posts...")
    blog_posts = blog_transformer.transform_all()
    stats['total_entries'] += len(blog_posts)
    
    # Write blog posts (use Jekyll locale for folder name)
    if blog_posts:
        try:
            file_writer.write_multiple_posts(blog_posts, jekyll_locale)
            stats['successful'] += len(blog_posts)
        except Exception as e:
            logger.error(f"❌ BLOG_POSTS_WRITE_FAILED: {str(e)}")
            stats['failed'] += len(blog_posts)
    
    # Transform and write profile (use Jekyll locale for filename)
    logger.info(f"👤 Transforming profile...")
    profiles = profile_transformer.transform_all()
    stats['total_entries'] += len(profiles)
    
    if profiles:
        try:
            data_writer.write_data_file(profiles[0], 'profile', jekyll_locale)
            stats['successful'] += 1
        except Exception as e:
            logger.error(f"❌ PROFILE_WRITE_FAILED: {str(e)}")
            stats['failed'] += 1
    
    # Transform and write header (use Jekyll locale for filename)
    logger.info(f"🔝 Transforming header...")
    headers = header_transformer.transform_all()
    stats['total_entries'] += len(headers)
    
    if headers:
        try:
            data_writer.write_data_file(headers[0], 'header', jekyll_locale)
            stats['successful'] += 1
        except Exception as e:
            logger.error(f"❌ HEADER_WRITE_FAILED: {str(e)}")
            stats['failed'] += 1
    
    # Transform and write footer (use Jekyll locale for filename)
    logger.info(f"🔽 Transforming footer...")
    footers = footer_transformer.transform_all()
    stats['total_entries'] += len(footers)
    
    if footers:
        try:
            data_writer.write_data_file(footers[0], 'footer', jekyll_locale)
            stats['successful'] += 1
        except Exception as e:
            logger.error(f"❌ FOOTER_WRITE_FAILED: {str(e)}")
            stats['failed'] += 1
    
    # Transform and write homepage (use Jekyll locale for filename)
    logger.info(f"🏠 Transforming homepage...")
    homepages = homepage_transformer.transform_all()
    stats['total_entries'] += len(homepages)
    
    if homepages:
        try:
            data_writer.write_data_file(homepages[0], 'homepage', jekyll_locale)
            stats['successful'] += 1
        except Exception as e:
            logger.error(f"❌ HOMEPAGE_WRITE_FAILED: {str(e)}")
            stats['failed'] += 1
    
    return stats


def calculate_exit_code(stats: Dict[str, Any]) -> int:
    """
    Calculate exit code based on failure threshold.
    
    Failure threshold logic:
    - < 10% failure rate: Exit 0 (success, deploy partial content)
    - >= 10% failure rate: Exit 1 (failure, abort deployment)
    - 0 total entries: Exit 0 (empty site is valid)
    
    Args:
        stats: Statistics dictionary
    
    Returns:
        Exit code (0 or 1)
    """
    total = stats['total_entries']
    failed = stats['failed_transformations']
    
    # Empty site is valid
    if total == 0:
        logger.warning(
            "⚠️ NO_CONTENT_FOUND "
            "message='No content entries found in Contentful'"
        )
        return 0
    
    # Calculate failure rate
    failure_rate = failed / total if total > 0 else 0
    
    if failure_rate >= 0.10:  # 10% threshold
        logger.error(
            f"❌ FAILURE_THRESHOLD_EXCEEDED "
            f"failure_rate={failure_rate:.1%} "
            f"threshold=10% "
            f"failed={failed} "
            f"total={total} "
            f"action=abort_deployment"
        )
        return 1
    elif failed > 0:
        logger.warning(
            f"⚠️ PARTIAL_FAILURE "
            f"failure_rate={failure_rate:.1%} "
            f"failed={failed} "
            f"total={total} "
            f"action=deploy_partial_content"
        )
        return 0
    else:
        # All successful
        return 0


if __name__ == '__main__':
    sys.exit(main())
