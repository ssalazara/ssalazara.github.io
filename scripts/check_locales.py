#!/usr/bin/env python3
"""
Quick script to check available locales in Contentful space.
"""

import os
import sys
from dotenv import load_dotenv
import contentful

# Load environment variables
load_dotenv()

CONTENTFUL_SPACE_ID = os.getenv('CONTENTFUL_SPACE_ID')
CONTENTFUL_ACCESS_TOKEN = os.getenv('CONTENTFUL_ACCESS_TOKEN')

if not CONTENTFUL_SPACE_ID or not CONTENTFUL_ACCESS_TOKEN:
    print("❌ ERROR: Missing CONTENTFUL_SPACE_ID or CONTENTFUL_ACCESS_TOKEN in .env")
    sys.exit(1)

print(f"🔍 Checking locales for space: {CONTENTFUL_SPACE_ID}\n")

try:
    # Initialize client
    client = contentful.Client(
        CONTENTFUL_SPACE_ID,
        CONTENTFUL_ACCESS_TOKEN
    )
    
    # Fetch locales
    print("📡 Fetching locales from Contentful API...")
    locales = client.locales()
    
    print(f"\n✅ Found {len(locales)} locale(s):\n")
    
    for idx, locale in enumerate(locales, 1):
        is_default = "✓ DEFAULT" if locale.default else ""
        fallback = f" (fallback: {locale.fallback_code})" if hasattr(locale, 'fallback_code') and locale.fallback_code else ""
        
        print(f"{idx}. Code: '{locale.code}' - Name: '{locale.name}' {is_default}{fallback}")
    
    print("\n" + "="*60)
    print("📝 TO FIX YOUR SCRIPT:")
    print("="*60)
    
    locale_codes = [locale.code for locale in locales]
    print(f"\nEdit scripts/config.py and change line ~20 to:")
    print(f"LOCALES = {locale_codes}")
    
    print("\n" + "="*60)
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    sys.exit(1)
