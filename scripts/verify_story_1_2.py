#!/usr/bin/env python3
"""
Verify Story 1.2: Contentful Client with Caching

This script checks that the Contentful client meets all acceptance criteria.
Run with: python scripts/verify_story_1_2.py
"""

import sys
import inspect
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

def check_type_hints(cls, method_name: str) -> bool:
    """Check if a method has type hints."""
    method = getattr(cls, method_name)
    sig = inspect.signature(method)
    
    # Check return type
    has_return_type = sig.return_annotation != inspect.Signature.empty
    
    # Check parameter types (skip 'self')
    params_with_types = [
        p for p in sig.parameters.values() 
        if p.name != 'self' and p.annotation != inspect.Signature.empty
    ]
    
    total_params = len([p for p in sig.parameters.values() if p.name != 'self'])
    
    return has_return_type and (len(params_with_types) == total_params)


def main():
    """Main verification function."""
    print("=" * 70)
    print("Story 1.2: Contentful Client with Caching Verification")
    print("=" * 70)
    
    checks_passed = []
    
    # Import the client
    print("\n📦 Importing ContentfulClient...")
    try:
        from scripts.contentful_client.client import ContentfulClient
        print("✅ ContentfulClient imported successfully")
        checks_passed.append(True)
    except ImportError as e:
        print(f"❌ Failed to import ContentfulClient: {e}")
        checks_passed.append(False)
        return 1
    
    # Check class attributes
    print("\n🔍 Checking Class Structure:")
    
    # Check __init__ parameters
    init_sig = inspect.signature(ContentfulClient.__init__)
    init_params = list(init_sig.parameters.keys())
    
    required_params = ['self', 'space_id', 'access_token', 'mode', 'cache_ttl']
    has_required_params = all(p in init_params for p in required_params)
    
    status = "✅" if has_required_params else "❌"
    print(f"{status} __init__ has required parameters: {required_params}")
    checks_passed.append(has_required_params)
    
    # Check public methods exist
    print("\n📋 Checking Public Methods:")
    
    required_methods = {
        'get_entries': 'Fetch entries with caching',
        'get_entry': 'Fetch single entry',
        'clear_cache': 'Clear cache',
        'get_cache_stats': 'Get cache statistics'
    }
    
    for method_name, description in required_methods.items():
        has_method = hasattr(ContentfulClient, method_name)
        status = "✅" if has_method else "❌"
        print(f"{status} {method_name}() - {description}")
        checks_passed.append(has_method)
    
    # Check type hints
    print("\n🏷️  Checking Type Hints:")
    
    methods_to_check = ['get_entries', 'get_entry', 'clear_cache', 'get_cache_stats']
    
    for method_name in methods_to_check:
        if hasattr(ContentfulClient, method_name):
            has_types = check_type_hints(ContentfulClient, method_name)
            status = "✅" if has_types else "❌"
            print(f"{status} {method_name}() has type hints")
            checks_passed.append(has_types)
        else:
            print(f"❌ {method_name}() not found")
            checks_passed.append(False)
    
    # Check cache implementation
    print("\n💾 Checking Cache Implementation:")
    
    # Check for cache-related attributes in __init__
    init_source = inspect.getsource(ContentfulClient.__init__)
    
    has_cache_dict = '_cache' in init_source
    has_cache_ttl = 'cache_ttl' in init_source
    
    status = "✅" if has_cache_dict else "❌"
    print(f"{status} In-memory cache dictionary (_cache)")
    checks_passed.append(has_cache_dict)
    
    status = "✅" if has_cache_ttl else "❌"
    print(f"{status} Cache TTL configuration")
    checks_passed.append(has_cache_ttl)
    
    # Check dual-mode support
    print("\n🔄 Checking Dual-Mode Support:")
    
    get_entries_source = inspect.getsource(ContentfulClient.get_entries) if hasattr(ContentfulClient, 'get_entries') else ""
    init_source_full = inspect.getsource(ContentfulClient.__init__)
    
    has_mode_param = 'mode' in init_source_full
    has_preview_support = 'preview' in init_source_full.lower()
    
    status = "✅" if has_mode_param else "❌"
    print(f"{status} Mode parameter (production/preview)")
    checks_passed.append(has_mode_param)
    
    status = "✅" if has_preview_support else "❌"
    print(f"{status} Preview API support")
    checks_passed.append(has_preview_support)
    
    # Check locale support
    print("\n🌍 Checking Locale Support:")
    
    has_locale_param = 'locale' in get_entries_source
    status = "✅" if has_locale_param else "❌"
    print(f"{status} Locale parameter in get_entries()")
    checks_passed.append(has_locale_param)
    
    # Check include parameter
    print("\n🔗 Checking Include Parameter:")
    
    has_include_param = 'include' in get_entries_source
    status = "✅" if has_include_param else "❌"
    print(f"{status} Include parameter for reference optimization")
    checks_passed.append(has_include_param)
    
    # Check structured logging
    print("\n📝 Checking Structured Logging:")
    
    client_source = inspect.getsource(ContentfulClient)
    has_logging = 'logger' in client_source
    has_structured_logs = 'content_type=' in client_source or 'locale=' in client_source
    
    status = "✅" if has_logging else "❌"
    print(f"{status} Logger imported and used")
    checks_passed.append(has_logging)
    
    status = "✅" if has_structured_logs else "❌"
    print(f"{status} Structured logging format (key=value)")
    checks_passed.append(has_structured_logs)
    
    # Summary
    print("\n" + "=" * 70)
    total_checks = len(checks_passed)
    passed_checks = sum(checks_passed)
    
    if passed_checks == total_checks:
        print(f"✅ ALL CHECKS PASSED ({passed_checks}/{total_checks})")
        print("\n🎉 Story 1.2 is COMPLETE!")
        print("\nNext step: Story 1.3 - Blog Post Transformer (Core Logic)")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed_checks}/{total_checks} passed)")
        print("\n⚠️  Please review the implementation above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
