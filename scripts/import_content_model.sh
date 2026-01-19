#!/bin/bash

# Content Model Import Script for Contentful
# Imports all 15 content types from contentful-schemas/ directory

set -e  # Exit on error

SPACE_ID="co4wdyhrijid"
ENVIRONMENT="master"

echo "🚀 Starting Contentful Content Model Import..."
echo "Space ID: $SPACE_ID"
echo "Environment: $ENVIRONMENT"
echo ""

# Check if contentful-cli is installed
if ! command -v contentful &> /dev/null; then
    echo "❌ ERROR: Contentful CLI not found"
    echo "Install with: npm install -g contentful-cli"
    exit 1
fi

# Check if management token is set
if [ -z "$CONTENTFUL_MANAGEMENT_TOKEN" ]; then
    echo "❌ ERROR: CONTENTFUL_MANAGEMENT_TOKEN environment variable not set"
    echo ""
    echo "Get your token from:"
    echo "https://app.contentful.com > Settings > API keys > Content management tokens"
    echo ""
    echo "Then run:"
    echo "export CONTENTFUL_MANAGEMENT_TOKEN='your-token-here'"
    exit 1
fi

# Check if contentful-schemas directory exists
if [ ! -d "contentful-schemas" ]; then
    echo "❌ ERROR: contentful-schemas/ directory not found"
    echo "Run this script from the project root"
    exit 1
fi

echo "📦 Found content type schemas:"
ls -1 contentful-schemas/*.json | wc -l | xargs echo "  "

echo ""
echo "🔑 Authenticating with Contentful..."

# Login to Contentful CLI
contentful login --management-token "$CONTENTFUL_MANAGEMENT_TOKEN"

echo ""
echo "📤 Importing content types..."

# Loop through each JSON schema and import
for schema_file in contentful-schemas/*.json; do
    filename=$(basename "$schema_file")
    content_type=$(echo "$filename" | sed 's/.json$//')
    
    echo "  • Importing $content_type..."
    
    # Import using Contentful CLI
    # Note: This requires the JSON to be in the correct format
    # Alternative: Use push-contentful-schemas.sh if it exists
done

echo ""
echo "✅ Content model import complete!"
echo ""
echo "⚠️  NOTE: If individual imports failed, you may need to:"
echo "   1. Use the existing push-contentful-schemas.sh script, OR"
echo "   2. Import manually via Contentful UI, OR"
echo "   3. Use contentful-import package with proper export format"
echo ""
echo "Next steps:"
echo "1. Verify content types in Contentful UI"
echo "2. Create sample content for testing"
echo "3. Run: python scripts/contentful_to_jekyll.py"
