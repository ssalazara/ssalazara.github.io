#!/usr/bin/env python3
"""
Final migration script with deep cleaning
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
import re

SPACE_ID = "co4wdyhrijid"
ENV_ID = "master"
SCHEMAS_DIR = Path("contentful-schemas")

# All content types to import
CONTENT_TYPES = {
    "seo.json": "seo",
    "social-link.json": "socialLink",
    "menu-item.json": "menuItem",
    "profile.json": "profile",
    "component-card.json": "componentCard",
    "hero-banner.json": "heroBanner",
    "or-header.json": "orHeader",
    "footer.json": "footer",
    "homepage.json": "homePage",
    "blogpage.json": "blogPage",
}

def deep_remove_properties(obj, keys_to_remove):
    """Recursively remove properties from nested objects"""
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if key in keys_to_remove:
                del obj[key]
            else:
                deep_remove_properties(obj[key], keys_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            deep_remove_properties(item, keys_to_remove)
    return obj

def clean_schema(schema_data):
    """Deep clean schema by removing invalid properties"""
    # Remove helpText and message recursively
    cleaned = deep_remove_properties(schema_data, {'helpText', 'message'})
    return cleaned

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
    print(f"📤 {filename} → {ct_id}")
    
    schema_path = SCHEMAS_DIR / filename
    
    try:
        with open(schema_path, 'r') as f:
            content = f.read()
            # Fix trailing commas
            content = re.sub(r',(\s*[}\]])', r'\1', content)
            schema_data = json.loads(content)
    except Exception as e:
        print(f"   ❌ Parse error: {e}")
        return False
    
    # Deep clean
    schema_data = clean_schema(schema_data)
    import_data = create_import_json(schema_data, ct_id)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(import_data, f, indent=2)
        temp_file = f.name
    
    try:
        # Import
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
        
        # Check success
        if 'ValidationFailed' in result.stdout or 'ValidationFailed' in result.stderr:
            print(f"   ❌ Validation failed")
            # Show first error line
            for line in result.stdout.split('\n'):
                if 'Details:' in line:
                    print(f"      {line.strip()}")
                    break
            return False
        elif 'Content Types' in result.stdout and ('1' in result.stdout or 'imported' in result.stdout.lower()):
            print(f"   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed (unknown reason)")
            return False
    finally:
        os.unlink(temp_file)

def main():
    print("🚀 Migración Final de Content Types")
    print("=" * 60)
    print(f"Importando {len(CONTENT_TYPES)} content types\n")
    
    success = 0
    failed = 0
    
    for filename, ct_id in CONTENT_TYPES.items():
        if import_content_type(filename, ct_id):
            success += 1
        else:
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Resultado:")
    print(f"  ✅ {success} exitosos")
    print(f"  ❌ {failed} fallidos")
    
    if success == len(CONTENT_TYPES):
        print("\n🎉 ¡Todos los content types importados!")
        print(f"\nVer en: https://app.contentful.com/spaces/{SPACE_ID}/content_types")
    
    return failed

if __name__ == '__main__':
    exit(main())
