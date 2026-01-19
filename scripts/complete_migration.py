#!/usr/bin/env python3
"""
Complete the migration of missing content types
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

# Missing content types to import
MISSING_TYPES = {
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

def clean_field(field):
    """Remove invalid properties from field"""
    field.pop('helpText', None)
    
    if 'validations' in field:
        for validation in field['validations']:
            validation.pop('message', None)
    
    if 'items' in field and 'validations' in field['items']:
        for validation in field['items']['validations']:
            validation.pop('message', None)
    
    return field

def clean_schema(schema_data):
    """Clean schema by removing invalid properties"""
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
    print(f"📤 Importing: {filename} → {ct_id}")
    
    schema_path = SCHEMAS_DIR / filename
    
    try:
        with open(schema_path, 'r') as f:
            content = f.read()
            try:
                schema_data = json.loads(content)
            except json.JSONDecodeError:
                # Fix trailing commas
                content = re.sub(r',(\s*[}\]])', r'\1', content)
                schema_data = json.loads(content)
    except Exception as e:
        print(f"   ❌ Failed to parse JSON: {e}")
        return False
    
    schema_data = clean_schema(schema_data)
    import_data = create_import_json(schema_data, ct_id)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(import_data, f, indent=2)
        temp_file = f.name
    
    try:
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
        
        if 'Content Types' in result.stdout and '1' in result.stdout:
            print(f"   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed")
            if 'already exists' in result.stdout.lower() or 'already exists' in result.stderr.lower():
                print(f"      (Already exists - skipping)")
                return True
            return False
    finally:
        os.unlink(temp_file)

def main():
    print("🚀 Completando Migración de Content Types")
    print("=" * 50)
    print(f"Migrando {len(MISSING_TYPES)} content types faltantes\n")
    
    success = 0
    failed = 0
    
    for filename, ct_id in MISSING_TYPES.items():
        if import_content_type(filename, ct_id):
            success += 1
        else:
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Resumen:")
    print(f"  ✅ Exitosos: {success} / {len(MISSING_TYPES)}")
    print(f"  ❌ Fallidos: {failed} / {len(MISSING_TYPES)}")
    
    if success == len(MISSING_TYPES):
        print("\n🎉 ¡Migración completa! Todos los 15 content types están en Contentful")
        print("\nVerifica en:")
        print(f"  https://app.contentful.com/spaces/{SPACE_ID}/content_types")
    
    return failed

if __name__ == '__main__':
    exit(main())
