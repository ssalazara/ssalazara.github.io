#!/usr/bin/env python3
"""
Verification script for Story 1.5: Graceful Error Handling & Structured Logging

Tests:
1. Single blog post failures don't crash the entire build
2. Errors are logged with full context
3. System continues processing remaining posts
4. Build is marked as failed if threshold exceeded (≥10%)
"""

import sys
import logging
from io import StringIO
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Add scripts to path
sys.path.insert(0, '/Users/simon.salazar/Documents/Apply Digital/github-page')

from scripts.transformers.blog_post_transformer import BlogPostTransformer
from scripts.writers.file_writer import FileWriter
from scripts.contentful_to_jekyll import calculate_exit_code


class TestResults:
    """Track test results and generate report."""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_details = []
    
    def add_pass(self, test_name: str, detail: str = ''):
        """Record a passing test."""
        self.tests_passed += 1
        self.test_details.append({
            'status': 'PASS',
            'name': test_name,
            'detail': detail
        })
        print(f"  ✅ {test_name}")
        if detail:
            print(f"     {detail}")
    
    def add_fail(self, test_name: str, error: str):
        """Record a failing test."""
        self.tests_failed += 1
        self.test_details.append({
            'status': 'FAIL',
            'name': test_name,
            'error': error
        })
        print(f"  ❌ {test_name}")
        print(f"     Error: {error}")
    
    def print_summary(self):
        """Print final test summary."""
        total = self.tests_passed + self.tests_failed
        print("\n" + "="*80)
        print("📊 STORY 1.5 VERIFICATION SUMMARY")
        print("="*80)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"Success Rate: {(self.tests_passed/total*100):.1f}%")
        
        if self.tests_failed == 0:
            print("\n🎉 Story 1.5: ALL REQUIREMENTS VERIFIED!")
            return 0
        else:
            print(f"\n⚠️  Story 1.5: {self.tests_failed} test(s) failed")
            return 1


def create_mock_entry(entry_id: str, has_seo: bool = True, valid_seo: bool = True):
    """
    Create a mock Contentful entry for testing.
    
    Args:
        entry_id: Entry ID
        has_seo: Whether entry has SEO reference
        valid_seo: Whether SEO entry is valid
    
    Returns:
        Mock Entry object
    """
    mock_entry = Mock()
    mock_entry.id = entry_id
    
    # Mock SEO entry
    if has_seo:
        mock_seo = Mock()
        mock_seo.id = f"seo-{entry_id}"
        
        if valid_seo:
            mock_seo.fields.return_value = {
                'title': f'SEO Title {entry_id}',
                'description': f'SEO Description {entry_id}',
                'keywords': ['test', 'blog']
            }
        else:
            # Missing required fields
            mock_seo.fields.return_value = {
                'title': '',
                'description': ''
            }
        
        mock_entry.fields.return_value = {
            'url': f'test-post-{entry_id}',
            'title': f'Test Post {entry_id}',
            'description': f'Test description {entry_id}',
            'label': 'Technology',
            'author': 'Test Author',
            'publishDate': '2026-01-19T12:00:00Z',
            'text': {'nodeType': 'document', 'content': []},
            'seo': mock_seo
        }
    else:
        # No SEO reference
        mock_entry.fields.return_value = {
            'url': f'test-post-{entry_id}',
            'title': f'Test Post {entry_id}',
            'description': f'Test description {entry_id}',
            'publishDate': '2026-01-19T12:00:00Z'
        }
    
    return mock_entry


def test_single_failure_doesnt_crash(results: TestResults):
    """Test that a single blog post failure doesn't crash the entire build."""
    print("\n" + "="*80)
    print("TEST 1: Single Failure Doesn't Crash Entire Build")
    print("="*80)
    
    try:
        # Create mock client
        mock_client = Mock()
        
        # Create mix of valid and invalid entries
        entries = [
            create_mock_entry('entry-1', has_seo=True, valid_seo=True),   # Valid
            create_mock_entry('entry-2', has_seo=False, valid_seo=False), # Missing SEO (should fail)
            create_mock_entry('entry-3', has_seo=True, valid_seo=True),   # Valid
            create_mock_entry('entry-4', has_seo=True, valid_seo=False),  # Invalid SEO (should fail)
            create_mock_entry('entry-5', has_seo=True, valid_seo=True),   # Valid
        ]
        
        mock_client.get_entries.return_value = entries
        
        # Initialize transformer
        transformer = BlogPostTransformer(mock_client, locale='en-US')
        
        # Capture log output
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.ERROR)
        logging.getLogger().addHandler(handler)
        
        # Transform all entries
        transformed = transformer.transform_all()
        
        # Remove handler
        logging.getLogger().removeHandler(handler)
        log_output = log_capture.getvalue()
        
        # Verify results
        if len(transformed) == 3:  # Should have 3 valid entries
            results.add_pass(
                "Build continues after failures",
                f"Processed 5 entries, 3 succeeded, 2 failed (as expected)"
            )
        else:
            results.add_fail(
                "Build continues after failures",
                f"Expected 3 successful transformations, got {len(transformed)}"
            )
        
        # Verify errors were logged
        if 'TRANSFORM_FAILED' in log_output:
            results.add_pass(
                "Failures are logged",
                "TRANSFORM_FAILED messages found in logs"
            )
        else:
            results.add_fail(
                "Failures are logged",
                "No TRANSFORM_FAILED messages in logs"
            )
        
        # Verify entry IDs are in error logs
        if 'entry-2' in log_output and 'entry-4' in log_output:
            results.add_pass(
                "Failed entry IDs are logged",
                "Both failed entry IDs present in error logs"
            )
        else:
            results.add_fail(
                "Failed entry IDs are logged",
                "Failed entry IDs not found in logs"
            )
    
    except Exception as e:
        results.add_fail("Test execution", str(e))


def test_structured_error_logging(results: TestResults):
    """Test that errors are logged with full context."""
    print("\n" + "="*80)
    print("TEST 2: Structured Error Logging with Full Context")
    print("="*80)
    
    try:
        # Create mock client
        mock_client = Mock()
        
        # Create entry that will fail validation
        failing_entry = create_mock_entry('failing-entry', has_seo=False)
        mock_client.get_entries.return_value = [failing_entry]
        
        # Initialize transformer
        transformer = BlogPostTransformer(mock_client, locale='en-US')
        
        # Capture log output at ERROR level
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        
        # Transform entries (should fail)
        transformer.transform_all()
        
        # Remove handler
        logging.getLogger().removeHandler(handler)
        log_output = log_capture.getvalue()
        
        # Verify log structure
        required_fields = [
            'TRANSFORM_FAILED',
            'entry_id=failing-entry',
            'locale=en-US',
            'error='
        ]
        
        all_present = all(field in log_output for field in required_fields)
        
        if all_present:
            results.add_pass(
                "Error logs contain required fields",
                "entry_id, locale, and error present"
            )
        else:
            missing = [f for f in required_fields if f not in log_output]
            results.add_fail(
                "Error logs contain required fields",
                f"Missing fields: {missing}"
            )
        
        # Verify structured format (key=value pairs)
        if '=' in log_output and 'entry_id=' in log_output:
            results.add_pass(
                "Logs use structured format",
                "key=value format detected"
            )
        else:
            results.add_fail(
                "Logs use structured format",
                "key=value format not found"
            )
    
    except Exception as e:
        results.add_fail("Test execution", str(e))


def test_file_writer_graceful_degradation(results: TestResults):
    """Test that file writer continues after individual write failures."""
    print("\n" + "="*80)
    print("TEST 3: File Writer Graceful Degradation")
    print("="*80)
    
    try:
        # Create file writer
        file_writer = FileWriter('/tmp/test-jekyll')
        
        # Create mix of valid and invalid post data
        posts = [
            {
                'frontmatter': {
                    'slug': 'valid-post-1',
                    'title': 'Valid Post 1',
                    'publish_date': '2026-01-19T12:00:00Z'
                },
                'body': 'Content 1'
            },
            {
                'frontmatter': {
                    'slug': '',  # Invalid slug
                    'title': 'Invalid Post',
                    'publish_date': 'invalid-date'  # Invalid date
                },
                'body': 'Content 2'
            },
            {
                'frontmatter': {
                    'slug': 'valid-post-2',
                    'title': 'Valid Post 2',
                    'publish_date': '2026-01-20T12:00:00Z'
                },
                'body': 'Content 3'
            }
        ]
        
        # Capture log output
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(handler)
        
        # Write posts (should handle invalid gracefully)
        file_writer.write_multiple_posts(posts, 'en')
        
        # Remove handler
        logging.getLogger().removeHandler(handler)
        log_output = log_capture.getvalue()
        
        # Verify summary log exists
        if 'POSTS_WRITTEN' in log_output:
            results.add_pass(
                "Write operation completes",
                "POSTS_WRITTEN summary logged"
            )
        else:
            results.add_fail(
                "Write operation completes",
                "No POSTS_WRITTEN summary found"
            )
        
        # Verify success/failed counts are tracked
        if 'success=' in log_output and 'failed=' in log_output:
            results.add_pass(
                "Success/failure counts tracked",
                "success= and failed= counters present"
            )
        else:
            results.add_fail(
                "Success/failure counts tracked",
                "Counters not found in logs"
            )
    
    except Exception as e:
        results.add_fail("Test execution", str(e))


def test_exit_code_calculation(results: TestResults):
    """Test that build exit code reflects failure threshold."""
    print("\n" + "="*80)
    print("TEST 4: Exit Code Calculation & Failure Thresholds")
    print("="*80)
    
    try:
        # Test case 1: All successful (0% failure)
        stats_all_success = {
            'total_entries': 10,
            'successful_transformations': 10,
            'failed_transformations': 0,
            'locales_processed': ['en-US']
        }
        
        exit_code = calculate_exit_code(stats_all_success)
        if exit_code == 0:
            results.add_pass(
                "100% success → exit 0",
                "All successful builds exit with 0"
            )
        else:
            results.add_fail(
                "100% success → exit 0",
                f"Expected exit 0, got {exit_code}"
            )
        
        # Test case 2: Partial failure <10% (5% failure)
        stats_partial_failure = {
            'total_entries': 20,
            'successful_transformations': 19,
            'failed_transformations': 1,
            'locales_processed': ['en-US']
        }
        
        exit_code = calculate_exit_code(stats_partial_failure)
        if exit_code == 0:
            results.add_pass(
                "5% failure (<10%) → exit 0",
                "Partial content deploys when failure rate <10%"
            )
        else:
            results.add_fail(
                "5% failure (<10%) → exit 0",
                f"Expected exit 0, got {exit_code}"
            )
        
        # Test case 3: Exactly 10% failure (threshold)
        stats_threshold = {
            'total_entries': 10,
            'successful_transformations': 9,
            'failed_transformations': 1,
            'locales_processed': ['en-US']
        }
        
        exit_code = calculate_exit_code(stats_threshold)
        if exit_code == 1:
            results.add_pass(
                "10% failure (threshold) → exit 1",
                "Build aborts at 10% failure rate"
            )
        else:
            results.add_fail(
                "10% failure (threshold) → exit 1",
                f"Expected exit 1, got {exit_code}"
            )
        
        # Test case 4: High failure rate (50% failure)
        stats_high_failure = {
            'total_entries': 10,
            'successful_transformations': 5,
            'failed_transformations': 5,
            'locales_processed': ['en-US']
        }
        
        exit_code = calculate_exit_code(stats_high_failure)
        if exit_code == 1:
            results.add_pass(
                "50% failure (>10%) → exit 1",
                "Build aborts with high failure rate"
            )
        else:
            results.add_fail(
                "50% failure (>10%) → exit 1",
                f"Expected exit 1, got {exit_code}"
            )
        
        # Test case 5: Empty site (0 entries)
        stats_empty = {
            'total_entries': 0,
            'successful_transformations': 0,
            'failed_transformations': 0,
            'locales_processed': []
        }
        
        exit_code = calculate_exit_code(stats_empty)
        if exit_code == 0:
            results.add_pass(
                "Empty site (0 entries) → exit 0",
                "Empty site is considered valid"
            )
        else:
            results.add_fail(
                "Empty site (0 entries) → exit 0",
                f"Expected exit 0, got {exit_code}"
            )
    
    except Exception as e:
        results.add_fail("Test execution", str(e))


def test_error_context_preservation(results: TestResults):
    """Test that error context is preserved through the stack."""
    print("\n" + "="*80)
    print("TEST 5: Error Context Preservation")
    print("="*80)
    
    try:
        from scripts.transformers.base_transformer import BaseTransformer
        from scripts.config import logger
        
        # Create mock entry
        mock_entry = Mock()
        mock_entry.id = 'context-test-entry'
        
        # Create transformer instance
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en-US')
        
        # Capture log output with full context
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.ERROR)
        logging.getLogger().addHandler(handler)
        
        # Log an error
        test_error = ValueError("SEO validation failed: missing description")
        transformer.log_transform_error(mock_entry, test_error)
        
        # Remove handler
        logging.getLogger().removeHandler(handler)
        log_output = log_capture.getvalue()
        
        # Verify context is preserved
        context_elements = [
            'context-test-entry',  # Entry ID
            'en-US',               # Locale
            'SEO validation failed' # Original error message
        ]
        
        all_present = all(elem in log_output for elem in context_elements)
        
        if all_present:
            results.add_pass(
                "Error context preserved",
                "Entry ID, locale, and error message all present"
            )
        else:
            missing = [elem for elem in context_elements if elem not in log_output]
            results.add_fail(
                "Error context preserved",
                f"Missing context elements: {missing}"
            )
    
    except Exception as e:
        results.add_fail("Test execution", str(e))


def main():
    """Run all Story 1.5 verification tests."""
    print("\n" + "="*80)
    print("🚀 STORY 1.5 VERIFICATION")
    print("Graceful Error Handling & Structured Logging")
    print("="*80)
    
    results = TestResults()
    
    # Run all tests
    test_single_failure_doesnt_crash(results)
    test_structured_error_logging(results)
    test_file_writer_graceful_degradation(results)
    test_exit_code_calculation(results)
    test_error_context_preservation(results)
    
    # Print summary and return exit code
    return results.print_summary()


if __name__ == '__main__':
    sys.exit(main())
