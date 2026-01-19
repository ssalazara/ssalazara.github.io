#!/bin/bash
# Update SEO content type field validation via Contentful Management API

SPACE_ID="${CONTENTFUL_SPACE_ID:-co4wdyhrijid}"
MANAGEMENT_TOKEN="${CONTENTFUL_MANAGEMENT_TOKEN}"

if [ -z "$MANAGEMENT_TOKEN" ]; then
    echo "❌ CONTENTFUL_MANAGEMENT_TOKEN environment variable not set"
    echo ""
    echo "To get your Management Token:"
    echo "1. Go to https://app.contentful.com"
    echo "2. Navigate to: Settings → API keys → Content management tokens"
    echo "3. Generate a personal token"
    echo "4. Run: export CONTENTFUL_MANAGEMENT_TOKEN='your-token'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

BASE_URL="https://api.contentful.com/spaces/$SPACE_ID/environments/master"

echo "🔍 Fetching current SEO content type..."

# Get current content type
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "Authorization: Bearer $MANAGEMENT_TOKEN" \
    -H "Content-Type: application/vnd.contentful.management.v1+json" \
    "$BASE_URL/content_types/seo")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "❌ Error fetching content type: HTTP $HTTP_CODE"
    echo "$BODY"
    exit 1
fi

VERSION=$(echo "$BODY" | jq -r '.sys.version')
echo "✓ Current version: $VERSION"

echo "🔧 Updating ogImage field validation..."

# Update the content type with new validation
UPDATED_BODY=$(echo "$BODY" | jq '
  .fields |= map(
    if .id == "ogImage" then
      .validations = [
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
      ] |
      .helpText = "Image shown when page is shared on social media. Recommended: 1200x630px (1.9:1 ratio). Accepts 600x315px to 2400x1260px. Social platforms will crop/resize as needed."
    else
      .
    end
  )
')

echo "📤 Pushing updated content type..."

# Update the content type
UPDATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
    -H "Authorization: Bearer $MANAGEMENT_TOKEN" \
    -H "Content-Type: application/vnd.contentful.management.v1+json" \
    -H "X-Contentful-Version: $VERSION" \
    -d "$UPDATED_BODY" \
    "$BASE_URL/content_types/seo")

UPDATE_HTTP_CODE=$(echo "$UPDATE_RESPONSE" | tail -n1)
UPDATE_BODY=$(echo "$UPDATE_RESPONSE" | sed '$d')

if [ "$UPDATE_HTTP_CODE" != "200" ] && [ "$UPDATE_HTTP_CODE" != "201" ]; then
    echo "❌ Error updating content type: HTTP $UPDATE_HTTP_CODE"
    echo "$UPDATE_BODY"
    exit 1
fi

echo "✓ Content type updated"

NEW_VERSION=$(echo "$UPDATE_BODY" | jq -r '.sys.version')

echo "📢 Publishing content type..."

# Publish the content type
PUBLISH_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
    -H "Authorization: Bearer $MANAGEMENT_TOKEN" \
    -H "X-Contentful-Version: $NEW_VERSION" \
    "$BASE_URL/content_types/seo/published")

PUBLISH_HTTP_CODE=$(echo "$PUBLISH_RESPONSE" | tail -n1)
PUBLISH_BODY=$(echo "$PUBLISH_RESPONSE" | sed '$d')

if [ "$PUBLISH_HTTP_CODE" != "200" ] && [ "$PUBLISH_HTTP_CODE" != "201" ]; then
    echo "❌ Error publishing content type: HTTP $PUBLISH_HTTP_CODE"
    echo "$PUBLISH_BODY"
    exit 1
fi

echo "✅ SEO content type successfully updated and published!"
echo ""
echo "🎉 Your 1024x1024 image should now work without errors."
echo ""
echo "Next steps:"
echo "1. Refresh your Contentful browser page (Cmd+R)"
echo "2. Try uploading your image again"
echo "3. If still cached, try in an incognito/private window"
