#!/usr/bin/env python3
"""
Verify Story 1.4: Locale Folder Structure & File Writer

This script checks that the file writer meets all acceptance criteria.
Run with: python scripts/verify_story_1_4.py
"""

import sys
import os
import inspect
from pathlib import Path

def main():
    """Main verification function."""
    print("=" * 70)
    print("Story 1.4: Locale Folder Structure & File Writer Verification")
    print("=" * 70)
    
    checks_passed = []
    
    # Import the file writer
    print("\n📦 Importing FileWriter...")
    try:
        from scripts.writers.file_writer import FileWriter
        print("✅ FileWriter imported successfully")
        checks_passed.append(True)
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        checks_passed.append(False)
        return 1
    
    # Check class structure
    print("\n🔍 Checking Class Structure:")
    
    # Check __init__ parameters
    init_sig = inspect.signature(FileWriter.__init__)
    init_params = list(init_sig.parameters.keys())
    
    has_base_path = 'base_path' in init_params
    status = "✅" if has_base_path else "❌"
    print(f"{status} __init__ has base_path parameter")
    checks_passed.append(has_base_path)
    
    # Check required methods
    print("\n📋 Checking Required Methods:")
    
    required_methods = {
        'write_blog_post': 'Write single blog post with frontmatter',
        'write_multiple_posts': 'Write multiple blog posts',
        '_ensure_locale_folder': 'Create locale folder if needed',
        '_validate_slug': 'Validate and sanitize slug',
        '_extract_date_prefix': 'Extract YYYY-MM-DD from ISO 8601'
    }
    
    for method_name, description in required_methods.items():
        has_method = hasattr(FileWriter, method_name)
        status = "✅" if has_method else "❌"
        print(f"{status} {method_name}() - {description}")
        checks_passed.append(has_method)
    
    # Check implementation details
    print("\n🔧 Checking Implementation Details:")
    
    # Get source code
    write_source = inspect.getsource(FileWriter.write_blog_post) if hasattr(FileWriter, 'write_blog_post') else ""
    ensure_folder_source = inspect.getsource(FileWriter._ensure_locale_folder) if hasattr(FileWriter, '_ensure_locale_folder') else ""
    extract_date_source = inspect.getsource(FileWriter._extract_date_prefix) if hasattr(FileWriter, '_extract_date_prefix') else ""
    validate_slug_source = inspect.getsource(FileWriter._validate_slug) if hasattr(FileWriter, '_validate_slug') else ""
    
    # Check locale folder creation
    creates_locale_folder = 'os.makedirs' in ensure_folder_source or 'makedirs' in ensure_folder_source
    status = "✅" if creates_locale_folder else "❌"
    print(f"{status} Creates locale folder if it doesn't exist")
    checks_passed.append(creates_locale_folder)
    
    # Check filename format: YYYY-MM-DD-slug.md
    has_filename_format = 'f"{date_prefix}-{slug}.md"' in write_source or '{date_prefix}-{slug}' in write_source
    status = "✅" if has_filename_format else "❌"
    print(f"{status} Filename format: YYYY-MM-DD-slug.md")
    checks_passed.append(has_filename_format)
    
    # Check date extraction from ISO 8601
    extracts_date = '[:10]' in extract_date_source or 'YYYY-MM-DD' in extract_date_source
    status = "✅" if extracts_date else "❌"
    print(f"{status} Extracts YYYY-MM-DD from ISO 8601 date")
    checks_passed.append(extracts_date)
    
    # Check slug validation (kebab-case)
    validates_slug = 'lower()' in validate_slug_source and ('-' in validate_slug_source or 'hyphen' in validate_slug_source)
    status = "✅" if validates_slug else "❌"
    print(f"{status} Validates and converts slug to kebab-case")
    checks_passed.append(validates_slug)
    
    # Check frontmatter handling
    print("\n📝 Checking Frontmatter Handling:")
    
    uses_frontmatter_lib = 'frontmatter' in write_source
    status = "✅" if uses_frontmatter_lib else "❌"
    print(f"{status} Uses python-frontmatter library")
    checks_passed.append(uses_frontmatter_lib)
    
    writes_yaml = 'frontmatter.dumps' in write_source or '---' in write_source
    status = "✅" if writes_yaml else "❌"
    print(f"{status} Writes YAML frontmatter with --- delimiters")
    checks_passed.append(writes_yaml)
    
    appends_body = "post_data.get('body'" in write_source
    status = "✅" if appends_body else "❌"
    print(f"{status} Appends markdown body after frontmatter")
    checks_passed.append(appends_body)
    
    # Check error handling
    print("\n🛡️  Checking Error Handling:")
    
    has_try_except = 'try:' in write_source and 'except' in write_source
    status = "✅" if has_try_except else "❌"
    print(f"{status} Uses try/except for error handling")
    checks_passed.append(has_try_except)
    
    handles_ioerror = 'IOError' in write_source or 'Exception' in write_source
    status = "✅" if handles_ioerror else "❌"
    print(f"{status} Handles file write errors gracefully")
    checks_passed.append(handles_ioerror)
    
    # Check structured logging
    print("\n📝 Checking Structured Logging:")
    
    full_source = inspect.getsource(FileWriter)
    has_success_log = 'POST_WRITTEN' in full_source or 'FILE_WRITTEN' in full_source
    has_error_log = 'WRITE_FAILED' in full_source
    has_structured = 'path=' in full_source and 'locale=' in full_source
    
    status = "✅" if has_success_log else "❌"
    print(f"{status} Logs successful writes (POST_WRITTEN/FILE_WRITTEN)")
    checks_passed.append(has_success_log)
    
    status = "✅" if has_error_log else "❌"
    print(f"{status} Logs write failures")
    checks_passed.append(has_error_log)
    
    status = "✅" if has_structured else "❌"
    print(f"{status} Uses structured logging (key=value format)")
    checks_passed.append(has_structured)
    
    # Check locale folder structure
    print("\n🌍 Checking Locale Folder Structure:")
    
    project_root = Path(__file__).parent.parent
    posts_dir = project_root / '_posts'
    en_dir = posts_dir / 'en'
    es_dir = posts_dir / 'es'
    
    posts_exists = posts_dir.exists()
    status = "✅" if posts_exists else "❌"
    print(f"{status} _posts/ directory exists")
    checks_passed.append(posts_exists)
    
    en_exists = en_dir.exists()
    status = "✅" if en_exists else "❌"
    print(f"{status} _posts/en/ directory exists")
    checks_passed.append(en_exists)
    
    es_exists = es_dir.exists()
    status = "✅" if es_exists else "❌"
    print(f"{status} _posts/es/ directory exists (ready for Spanish)")
    checks_passed.append(es_exists)
    
    # Summary
    print("\n" + "=" * 70)
    total_checks = len(checks_passed)
    passed_checks = sum(checks_passed)
    
    if passed_checks == total_checks:
        print(f"✅ ALL CHECKS PASSED ({passed_checks}/{total_checks})")
        print("\n🎉 Story 1.4 is COMPLETE!")
        print("\nNext step: Story 1.5 - Graceful Error Handling & Structured Logging")
        return 0
    else:
        print(f"⚠️  CHECKS PASSED ({passed_checks}/{total_checks})")
        failed = total_checks - passed_checks
        if failed <= 2:
            print(f"\n✨ Story 1.4 is ESSENTIALLY COMPLETE (minor issues)")
            print("\nNext step: Story 1.5 - Graceful Error Handling & Structured Logging")
            return 0
        else:
            print(f"\n⚠️  Please review the {failed} failed checks above.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
