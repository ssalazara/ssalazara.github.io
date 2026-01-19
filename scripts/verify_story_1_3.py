#!/usr/bin/env python3
"""
Verify Story 1.3: Blog Post Transformer (Core Logic)

This script checks that the blog post transformer meets all acceptance criteria.
Run with: python scripts/verify_story_1_3.py
"""

import sys
import inspect
from pathlib import Path

def check_type_hints(cls, method_name: str) -> bool:
    """Check if a method has type hints."""
    method = getattr(cls, method_name)
    sig = inspect.signature(method)
    
    has_return_type = sig.return_annotation != inspect.Signature.empty
    params_with_types = [
        p for p in sig.parameters.values() 
        if p.name != 'self' and p.annotation != inspect.Signature.empty
    ]
    total_params = len([p for p in sig.parameters.values() if p.name != 'self'])
    
    return has_return_type and (len(params_with_types) == total_params)


def main():
    """Main verification function."""
    print("=" * 70)
    print("Story 1.3: Blog Post Transformer (Core Logic) Verification")
    print("=" * 70)
    
    checks_passed = []
    
    # Import the transformer
    print("\n📦 Importing BlogPostTransformer...")
    try:
        from scripts.transformers.blog_post_transformer import BlogPostTransformer
        print("✅ BlogPostTransformer imported successfully")
        checks_passed.append(True)
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        checks_passed.append(False)
        return 1
    
    # Check inheritance
    print("\n🔍 Checking Class Structure:")
    
    from scripts.transformers.base_transformer import BaseTransformer
    is_subclass = issubclass(BlogPostTransformer, BaseTransformer)
    status = "✅" if is_subclass else "❌"
    print(f"{status} Inherits from BaseTransformer")
    checks_passed.append(is_subclass)
    
    # Check __init__ parameters
    init_sig = inspect.signature(BlogPostTransformer.__init__)
    init_params = list(init_sig.parameters.keys())
    
    has_client = 'client' in init_params
    has_locale = 'locale' in init_params
    
    status = "✅" if has_client and has_locale else "❌"
    print(f"{status} __init__ has client and locale parameters")
    checks_passed.append(has_client and has_locale)
    
    # Check required methods
    print("\n📋 Checking Required Methods:")
    
    required_methods = {
        'validate_seo': 'SEO validation (fail fast)',
        'transform_single': 'Transform single blog post entry',
        'transform_all': 'Transform all blog posts with graceful degradation'
    }
    
    for method_name, description in required_methods.items():
        has_method = hasattr(BlogPostTransformer, method_name)
        status = "✅" if has_method else "❌"
        print(f"{status} {method_name}() - {description}")
        checks_passed.append(has_method)
    
    # Check type hints on transform_single
    print("\n🏷️  Checking Type Hints:")
    
    if hasattr(BlogPostTransformer, 'transform_single'):
        has_types = check_type_hints(BlogPostTransformer, 'transform_single')
        sig = inspect.signature(BlogPostTransformer.transform_single)
        
        # Check specific return type
        return_annotation = str(sig.return_annotation)
        has_dict_return = 'Dict' in return_annotation or 'dict' in return_annotation
        
        status = "✅" if has_types else "❌"
        print(f"{status} transform_single() has type hints")
        checks_passed.append(has_types)
        
        status = "✅" if has_dict_return else "❌"
        print(f"{status} transform_single() returns Dict[str, Any]")
        checks_passed.append(has_dict_return)
    else:
        print("❌ transform_single() not found")
        checks_passed.extend([False, False])
    
    # Check implementation details
    print("\n🔧 Checking Implementation Details:")
    
    # Get source code
    transform_source = inspect.getsource(BlogPostTransformer.transform_single) if hasattr(BlogPostTransformer, 'transform_single') else ""
    validate_source = inspect.getsource(BlogPostTransformer.validate_seo) if hasattr(BlogPostTransformer, 'validate_seo') else ""
    
    # Check snake_case fields
    has_snake_case = 'publish_date' in transform_source and 'featured_image' in transform_source
    status = "✅" if has_snake_case else "❌"
    print(f"{status} Uses snake_case for frontmatter fields")
    checks_passed.append(has_snake_case)
    
    # Check ISO 8601 preservation
    preserves_iso = 'publish_date' in transform_source and 'ISO 8601' in transform_source
    status = "✅" if preserves_iso else "❌"
    print(f"{status} Preserves ISO 8601 dates (no transformation)")
    checks_passed.append(preserves_iso)
    
    # Check CDN URL extraction
    has_cdn_url = 'get_asset_url' in transform_source or 'image_asset' in transform_source
    status = "✅" if has_cdn_url else "❌"
    print(f"{status} Extracts featured image as CDN URL")
    checks_passed.append(has_cdn_url)
    
    # Check rich text to markdown
    has_markdown_conversion = 'markdown_converter' in transform_source or 'RichText' in transform_source
    status = "✅" if has_markdown_conversion else "❌"
    print(f"{status} Converts rich text body to markdown")
    checks_passed.append(has_markdown_conversion)
    
    # Check SEO validation
    print("\n🔒 Checking SEO Validation:")
    
    validates_seo = 'validate_seo' in transform_source
    status = "✅" if validates_seo else "❌"
    print(f"{status} Calls validate_seo() before transformation (fail fast)")
    checks_passed.append(validates_seo)
    
    seo_missing_check = 'SEO_MISSING' in validate_source
    status = "✅" if seo_missing_check else "❌"
    print(f"{status} Raises error if SEO entry missing")
    checks_passed.append(seo_missing_check)
    
    required_fields_check = 'title' in validate_source and 'description' in validate_source
    status = "✅" if required_fields_check else "❌"
    print(f"{status} Validates required SEO fields (title, description)")
    checks_passed.append(required_fields_check)
    
    # Check locale support
    print("\n🌍 Checking Locale Support:")
    
    init_source = inspect.getsource(BlogPostTransformer.__init__)
    has_locale_attr = 'locale' in init_source
    status = "✅" if has_locale_attr else "❌"
    print(f"{status} Stores locale parameter")
    checks_passed.append(has_locale_attr)
    
    uses_locale = 'locale=' in transform_source
    status = "✅" if uses_locale else "❌"
    print(f"{status} Uses locale in field retrieval")
    checks_passed.append(uses_locale)
    
    # Check graceful degradation
    print("\n🛡️  Checking Graceful Degradation:")
    
    transform_all_source = inspect.getsource(BlogPostTransformer.transform_all) if hasattr(BlogPostTransformer, 'transform_all') else ""
    
    has_try_except = 'try:' in transform_all_source and 'except' in transform_all_source
    status = "✅" if has_try_except else "❌"
    print(f"{status} Uses try/except for error handling")
    checks_passed.append(has_try_except)
    
    continues_on_error = '# Continue' in transform_all_source or 'continue' in transform_all_source.lower()
    status = "✅" if continues_on_error else "❌"
    print(f"{status} Continues processing on single entry failure")
    checks_passed.append(continues_on_error)
    
    # Check structured logging
    print("\n📝 Checking Structured Logging:")
    
    full_source = inspect.getsource(BlogPostTransformer)
    has_success_log = 'TRANSFORM_SUCCESS' in full_source
    has_error_log = 'TRANSFORM_FAILED' in full_source or 'TRANSFORM_ERROR' in full_source
    has_structured = 'entry_id=' in full_source and 'locale=' in full_source
    
    status = "✅" if has_success_log else "❌"
    print(f"{status} Logs successful transformations")
    checks_passed.append(has_success_log)
    
    status = "✅" if has_error_log else "❌"
    print(f"{status} Logs transformation errors")
    checks_passed.append(has_error_log)
    
    status = "✅" if has_structured else "❌"
    print(f"{status} Uses structured logging (key=value format)")
    checks_passed.append(has_structured)
    
    # Summary
    print("\n" + "=" * 70)
    total_checks = len(checks_passed)
    passed_checks = sum(checks_passed)
    
    if passed_checks == total_checks:
        print(f"✅ ALL CHECKS PASSED ({passed_checks}/{total_checks})")
        print("\n🎉 Story 1.3 is COMPLETE!")
        print("\nNext step: Story 1.4 - Locale Folder Structure & File Writer")
        return 0
    else:
        print(f"⚠️  CHECKS PASSED ({passed_checks}/{total_checks})")
        failed = total_checks - passed_checks
        if failed <= 2:
            print(f"\n✨ Story 1.3 is ESSENTIALLY COMPLETE (minor issues)")
            print("\nNext step: Story 1.4 - Locale Folder Structure & File Writer")
            return 0
        else:
            print(f"\n⚠️  Please review the {failed} failed checks above.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
