#!/usr/bin/env python3
"""Debug script to inspect homepage entry structure."""

import sys
sys.path.insert(0, '/Users/simon.salazar/Documents/Apply Digital/github-page')

from scripts.contentful_client.client import ContentfulClient
from scripts.config import CONTENT_TYPE_HOMEPAGE, CONTENTFUL_SPACE_ID, get_active_token

# Initialize client
client = ContentfulClient(CONTENTFUL_SPACE_ID, get_active_token())

# Fetch homepage
entries = client.get_entries(
    content_type=CONTENT_TYPE_HOMEPAGE,
    locale='en-US',
    include=2
)

if entries:
    homepage = entries[0]
    print(f"Homepage ID: {homepage.id}")
    print(f"Homepage fields: {homepage.fields().keys()}")
    
    # Get blocks
    fields = homepage.fields()
    blocks = fields.get('blocks', [])
    
    print(f"\nFound {len(blocks)} blocks")
    
    for i, block in enumerate(blocks):
        print(f"\n--- Block {i+1} ---")
        print(f"Type of block: {type(block)}")
        print(f"Block ID: {block.id if hasattr(block, 'id') else 'N/A'}")
        
        # Try different ways to get content type
        print(f"Has 'content_type' attr: {hasattr(block, 'content_type')}")
        print(f"Has 'sys' attr: {hasattr(block, 'sys')}")
        
        if hasattr(block, 'content_type'):
            ct = block.content_type
            print(f"  content_type: {ct}")
            print(f"  content_type.id: {ct.id if hasattr(ct, 'id') else 'N/A'}")
        
        if hasattr(block, 'sys'):
            sys_obj = block.sys
            print(f"  sys: {sys_obj}")
            print(f"  sys type: {type(sys_obj)}")
            print(f"  sys.__dict__: {vars(sys_obj) if hasattr(sys_obj, '__dict__') else 'N/A'}")
        
        # Try to get fields
        try:
            block_fields = block.fields()
            print(f"  fields keys: {block_fields.keys()}")
        except Exception as e:
            print(f"  Error getting fields: {e}")
