#!/usr/bin/env python3
"""
Update SEO content type field validation directly via Contentful Management API
"""

import os
import sys
import requests
import json

def update_seo_content_type():
    """Update the ogImage field validation for SEO content type"""
    
    # Get credentials from environment or prompt
    space_id = os.getenv('CONTENTFUL_SPACE_ID', 'co4wdyhrijid')
    management_token = os.getenv('CONTENTFUL_MANAGEMENT_TOKEN')
    
    if not management_token:
        print("❌ CONTENTFUL_MANAGEMENT_TOKEN environment variable not set")
        print("\nTo get your Management Token:")
        print("1. Go to https://app.contentful.com")
        print("2. Navigate to: Settings → API keys → Content management tokens")
        print("3. Generate a personal token")
        print("4. Export it: export CONTENTFUL_MANAGEMENT_TOKEN='your-token'")
        sys.exit(1)
    
    base_url = f"https://api.contentful.com/spaces/{space_id}/environments/master"
    headers = {
        "Authorization": f"Bearer {management_token}",
        "Content-Type": "application/vnd.contentful.management.v1+json"
    }
    
    print("🔍 Fetching current SEO content type...")
    
    # Get current content type
    response = requests.get(
        f"{base_url}/content_types/seo",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Error fetching content type: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    content_type = response.json()
    version = content_type['sys']['version']
    
    print(f"✓ Current version: {version}")
    
    # Update the ogImage field validation
    for field in content_type['fields']:
        if field['id'] == 'ogImage':
            print(f"🔧 Updating ogImage field validation...")
            field['validations'] = [
                {
                    "linkMimetypeGroup": ["image"],
                    "message": "Must be an image file"
                },
                {
                    "assetImageDimensions": {
                        "width": {"min": 600, "max": 2400},
                        "height": {"min": 315, "max": 1260}
                    },
                    "message": "Image dimensions should be between 600x315px and 2400x1260px. Recommended: 1200x630px for optimal display"
                },
                {
                    "assetFileSize": {
                        "max": 8388608
                    },
                    "message": "File size must be under 8MB"
                }
            ]
            field['helpText'] = "Image shown when page is shared on social media. Recommended: 1200x630px (1.9:1 ratio). Accepts 600x315px to 2400x1260px. Social platforms will crop/resize as needed."
            break
    
    # Update headers with version
    headers['X-Contentful-Version'] = str(version)
    
    print("📤 Pushing updated content type...")
    
    # Update the content type
    update_response = requests.put(
        f"{base_url}/content_types/seo",
        headers=headers,
        json=content_type
    )
    
    if update_response.status_code not in [200, 201]:
        print(f"❌ Error updating content type: {update_response.status_code}")
        print(update_response.text)
        sys.exit(1)
    
    print("✓ Content type updated")
    
    # Publish the content type
    updated_ct = update_response.json()
    new_version = updated_ct['sys']['version']
    
    headers['X-Contentful-Version'] = str(new_version)
    
    print("📢 Publishing content type...")
    
    publish_response = requests.put(
        f"{base_url}/content_types/seo/published",
        headers=headers
    )
    
    if publish_response.status_code not in [200, 201]:
        print(f"❌ Error publishing content type: {publish_response.status_code}")
        print(publish_response.text)
        sys.exit(1)
    
    print("✅ SEO content type successfully updated and published!")
    print("\n🎉 Your 1024x1024 image should now work without errors.")
    print("\nNext steps:")
    print("1. Refresh your Contentful browser page (Cmd+R or Ctrl+R)")
    print("2. Try uploading your image again")
    print("3. If cached, try in an incognito/private window")

if __name__ == "__main__":
    update_seo_content_type()
