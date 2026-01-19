#!/usr/bin/env python3
"""
Fix JSON schemas and import to Contentful using CLI
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

SPACE_ID = "co4wdyhrijid"
ENV_ID = "master"
SCHEMAS_DIR = Path("contentful-schemas")

# Content type ID mappings
CONTENT_TYPES = {
    "seo.json": "seo",
    "social-link.json": "socialLink",
    "menu-item.json": "menuItem",
    "profile.json": "profile",
    "component-image.json": "componentImage",
    "component-quote.json": "componentQuote",
    "component-card.json": "componentCard",
    "component-carousel.json": "componentCarousel",
    "rich-text-block.json": "richTextBlock",
    "text-with-image.json": "textWithImage",
    "hero-banner.json": "heroBanner",
    "or-header.json": "orHeader",
    "footer.json": "footer",
    "homepage.json": "homePage",
    "blogpage.json": "blogPage",
}

def clean_field(field):
    """Remove invalid properties from field"""
    # Remove helpText
    field.pop('helpText', None)
    
    # Clean validations
    if 'validations' in field:
        for validation in field['validations']:
            validation.pop('message', None)
    
    # Clean items.validations
    if 'items' in field and 'validations' in field['items']:
        for validation in field['items']['validations']:
            validation.pop('message', None)
    
    return field

def clean_schema(schema_data):
    """Clean schema by removing invalid properties"""
    # Clean each field
    if 'fields' in schema_data:
        schema_data['fields'] = [clean_field(field) for field in schema_data['fields']]
    
    return schema_data

def create_import_json(schema_data, ct_id):
    """Create valid import format"""
    return {
        "contentTypes": [{
            "sys": {
                "id": ct_id,
                "type": "ContentType"
            },
            "name": schema_data['name'],
            "description": schema_data.get('description', ''),
            "displayField": schema_data['displayField'],
            "fields": schema_data['fields']
        }]
    }

def import_content_type(filename, ct_id):
    """Import a single content type"""
    print(f"📤 Processing: {filename} → {ct_id}")
    
    schema_path = SCHEMAS_DIR / filename
    
    # Read and parse JSON (Python handles trailing commas via eval if needed)
    try:
        with open(schema_path, 'r') as f:
            content = f.read()
            # Try standard JSON first
            try:
                schema_data = json.loads(content)
            except json.JSONDecodeError:
                # If it fails, try to fix common issues
                import re
                # Remove trailing commas
                content = re.sub(r',(\s*[}\]])', r'\1', content)
                schema_data = json.loads(content)
    except Exception as e:
        print(f"   ❌ Failed to parse JSON: {e}")
        return False
    
    # Clean schema
    schema_data = clean_schema(schema_data)
    
    # Create import format
    import_data = create_import_json(schema_data, ct_id)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(import_data, f, indent=2)
        temp_file = f.name
    
    try:
        # Import using CLI
        result = subprocess.run(
            [
                'contentful', 'space', 'import',
                '--space-id', SPACE_ID,
                '--environment-id', ENV_ID,
                '--content-file', temp_file
            ],
            capture_output=True,
            text=True
        )
        
        # Check if successful
        if 'Content Types' in result.stdout and '1' in result.stdout:
            print(f"   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed")
            if result.stderr:
                print(f"      Error: {result.stderr[:200]}")
            return False
    finally:
        # Cleanup
        os.unlink(temp_file)

def main():
    print("🚀 Fixing and Importing Content Types")
    print("=" * 40)
    print()
    
    # Test connection
    print("🔌 Testing connection...")
    result = subprocess.run(
        ['contentful', 'space', 'list'],
        capture_output=True,
        text=True
    )
    
    if SPACE_ID not in result.stdout:
        print("❌ Cannot access space 'ssa'. Run: contentful login")
        return 1
    
    print("✅ Connected to space 'ssa'")
    print()
    
    # Import each content type
    success = 0
    failed = 0
    
    for filename, ct_id in CONTENT_TYPES.items():
        if import_content_type(filename, ct_id):
            success += 1
        else:
            failed += 1
        print()
    
    # Summary
    print("=" * 40)
    print(f"Summary:")
    print(f"  ✅ Success: {success} / {len(CONTENT_TYPES)}")
    print(f"  ❌ Failed: {failed} / {len(CONTENT_TYPES)}")
    print()
    
    if success > 0:
        print(f"🎉 Imported {success} content types!")
        print()
        print("View them at:")
        print(f"  https://app.contentful.com/spaces/{SPACE_ID}/content_types")
        print()
        print("Next steps:")
        print("  1. Create content entries in Contentful")
        print("  2. Run: python scripts/contentful_to_jekyll.py")
        print("  3. Run: bundle exec jekyll serve")
    
    return failed

if __name__ == '__main__':
    exit(main())
