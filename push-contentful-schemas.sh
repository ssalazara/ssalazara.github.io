#!/bin/bash

# Contentful Schema Push Script
# Project: GitHub Page
# Generated: 2026-01-19

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SPACE_ID="${CONTENTFUL_SPACE_ID:-}"
ENVIRONMENT="${CONTENTFUL_ENVIRONMENT:-master}"
SCHEMAS_DIR="./contentful-schemas"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Contentful Schema Import Tool${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if contentful CLI is installed
if ! command -v contentful &> /dev/null; then
    echo -e "${RED}❌ Contentful CLI not found!${NC}"
    echo -e "${YELLOW}Install with: npm install -g contentful-cli${NC}"
    exit 1
fi

# Check if logged in
if ! contentful space list &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with Contentful${NC}"
    echo -e "${YELLOW}Run: contentful login${NC}"
    exit 1
fi

# Get Space ID if not set
if [ -z "$SPACE_ID" ]; then
    echo -e "${YELLOW}⚠️  CONTENTFUL_SPACE_ID not set${NC}"
    echo ""
    echo "Available spaces:"
    contentful space list
    echo ""
    read -p "Enter your Space ID: " SPACE_ID
    
    if [ -z "$SPACE_ID" ]; then
        echo -e "${RED}❌ Space ID is required${NC}"
        exit 1
    fi
fi

# Confirm settings
echo -e "${GREEN}Configuration:${NC}"
echo "  Space ID: $SPACE_ID"
echo "  Environment: $ENVIRONMENT"
echo "  Schemas Directory: $SCHEMAS_DIR"
echo ""

# Check if schemas directory exists
if [ ! -d "$SCHEMAS_DIR" ]; then
    echo -e "${RED}❌ Schemas directory not found: $SCHEMAS_DIR${NC}"
    exit 1
fi

# Count JSON files
SCHEMA_COUNT=$(find "$SCHEMAS_DIR" -name "*.json" -type f | wc -l | tr -d ' ')

if [ "$SCHEMA_COUNT" -eq 0 ]; then
    echo -e "${RED}❌ No JSON schema files found in $SCHEMAS_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}Found $SCHEMA_COUNT schema file(s) to import${NC}"
echo ""

# Confirm before proceeding
read -p "Continue with import? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Import cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🚀 Starting import...${NC}"
echo ""

# Import each schema
SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_FILES=()

for schema_file in "$SCHEMAS_DIR"/*.json; do
    if [ -f "$schema_file" ]; then
        filename=$(basename "$schema_file")
        echo -e "${BLUE}📤 Importing: $filename${NC}"
        
        # Validate JSON first
        if ! jq empty "$schema_file" 2>/dev/null; then
            echo -e "${RED}  ✗ Invalid JSON, skipping${NC}"
            FAIL_COUNT=$((FAIL_COUNT + 1))
            FAILED_FILES+=("$filename (Invalid JSON)")
            echo ""
            continue
        fi
        
        # Import schema
        if contentful space import \
            --space-id "$SPACE_ID" \
            --environment-id "$ENVIRONMENT" \
            --content-file "$schema_file" \
            2>&1 | grep -q "success"; then
            
            echo -e "${GREEN}  ✓ Successfully imported${NC}"
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        else
            echo -e "${RED}  ✗ Import failed${NC}"
            FAIL_COUNT=$((FAIL_COUNT + 1))
            FAILED_FILES+=("$filename")
        fi
        
        echo ""
        sleep 1  # Rate limiting
    fi
done

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Import Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✓ Successful: $SUCCESS_COUNT${NC}"
echo -e "${RED}✗ Failed: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}Failed files:${NC}"
    for failed_file in "${FAILED_FILES[@]}"; do
        echo "  - $failed_file"
    done
    echo ""
fi

if [ $SUCCESS_COUNT -gt 0 ]; then
    echo -e "${GREEN}🎉 Import completed!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Verify content types in Contentful web app"
    echo "  2. Publish content types if needed"
    echo "  3. Create content entries"
    echo ""
    echo "View in Contentful:"
    echo "  https://app.contentful.com/spaces/$SPACE_ID/content_types"
fi

exit $FAIL_COUNT
