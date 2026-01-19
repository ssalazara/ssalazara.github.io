"""
Rich Text to Markdown converter for Contentful content.
Handles Contentful's RichText document structure.
"""

from typing import Dict, Any, List
from scripts.config import logger


class RichTextConverter:
    """
    Converts Contentful RichText JSON to Markdown.
    
    Supports:
    - Paragraphs, headings (H2-H4), lists, blockquotes, horizontal rules
    - Text marks: bold, italic, code, underline
    - Embedded assets (images)
    - Hyperlinks
    
    Handles unknown node types gracefully with warnings.
    """
    
    def __init__(self) -> None:
        """Initialize converter."""
        pass
    
    def convert(self, document: Dict[str, Any]) -> str:
        """
        Convert Contentful RichText document to Markdown.
        
        Args:
            document: RichText document dictionary
        
        Returns:
            Markdown string
        """
        if not document or document.get('nodeType') != 'document':
            logger.warning(
                f"⚠️ INVALID_RICHTEXT "
                f"missing or invalid document node"
            )
            return ''
        
        content = document.get('content', [])
        
        # Process all top-level nodes
        markdown_parts = []
        for node in content:
            markdown_parts.append(self._process_node(node))
        
        # Join with double newlines between blocks
        return '\n\n'.join(filter(None, markdown_parts))
    
    def _process_node(self, node: Dict[str, Any], depth: int = 0) -> str:
        """
        Process a single RichText node.
        
        Args:
            node: Node dictionary
            depth: Current nesting depth
        
        Returns:
            Markdown string for this node
        """
        if not node:
            return ''
        
        node_type = node.get('nodeType', '')
        content = node.get('content', [])
        value = node.get('value', '')
        
        # Text node
        if node_type == 'text':
            return self._process_text_node(node)
        
        # Paragraph
        if node_type == 'paragraph':
            text = ''.join(self._process_node(child, depth) for child in content)
            return text.strip()
        
        # Headings
        if node_type == 'heading-1':
            text = ''.join(self._process_node(child, depth) for child in content)
            return f"# {text}"
        if node_type == 'heading-2':
            text = ''.join(self._process_node(child, depth) for child in content)
            return f"## {text}"
        if node_type == 'heading-3':
            text = ''.join(self._process_node(child, depth) for child in content)
            return f"### {text}"
        if node_type == 'heading-4':
            text = ''.join(self._process_node(child, depth) for child in content)
            return f"#### {text}"
        if node_type == 'heading-5':
            text = ''.join(self._process_node(child, depth) for child in content)
            return f"##### {text}"
        if node_type == 'heading-6':
            text = ''.join(self._process_node(child, depth) for child in content)
            return f"###### {text}"
        
        # Unordered list
        if node_type == 'unordered-list':
            return self._process_list(content, ordered=False, depth=depth)
        
        # Ordered list
        if node_type == 'ordered-list':
            return self._process_list(content, ordered=True, depth=depth)
        
        # List item
        if node_type == 'list-item':
            text = '\n'.join(self._process_node(child, depth) for child in content)
            return text
        
        # Blockquote
        if node_type == 'blockquote':
            lines = []
            for child in content:
                child_text = self._process_node(child, depth)
                if child_text:
                    lines.append(f"> {child_text}")
            return '\n'.join(lines)
        
        # Horizontal rule
        if node_type == 'hr':
            return '---'
        
        # Hyperlink
        if node_type == 'hyperlink':
            text = ''.join(self._process_node(child, depth) for child in content)
            uri = node.get('data', {}).get('uri', '')
            return f"[{text}]({uri})"
        
        # Embedded asset (image)
        if node_type == 'embedded-asset-block':
            return self._process_embedded_asset(node)
        
        # Embedded entry (not fully supported - log and skip)
        if node_type == 'embedded-entry-block':
            logger.warning(
                f"⚠️ EMBEDDED_ENTRY_UNSUPPORTED "
                f"skipping embedded entry block"
            )
            return ''
        
        # Unknown node type - log warning and try to process children
        logger.warning(
            f"⚠️ UNKNOWN_NODE_TYPE "
            f"node_type={node_type} - attempting to process children"
        )
        
        # Try to process children if they exist
        if content:
            return ''.join(self._process_node(child, depth) for child in content)
        
        return ''
    
    def _process_text_node(self, node: Dict[str, Any]) -> str:
        """
        Process text node with marks (bold, italic, code, etc.).
        
        Args:
            node: Text node dictionary
        
        Returns:
            Markdown-formatted text
        """
        text = node.get('value', '')
        marks = node.get('marks', [])
        
        # Apply marks in order
        for mark in marks:
            mark_type = mark.get('type', '')
            
            if mark_type == 'bold':
                text = f"**{text}**"
            elif mark_type == 'italic':
                text = f"*{text}*"
            elif mark_type == 'code':
                text = f"`{text}`"
            elif mark_type == 'underline':
                text = f"<u>{text}</u>"
            else:
                # Unknown mark type
                logger.warning(
                    f"⚠️ UNKNOWN_MARK_TYPE "
                    f"mark_type={mark_type} - rendering as plain text"
                )
        
        return text
    
    def _process_list(
        self,
        items: List[Dict[str, Any]],
        ordered: bool,
        depth: int
    ) -> str:
        """
        Process list items.
        
        Args:
            items: List item nodes
            ordered: True for numbered list, False for bullets
            depth: Nesting depth for indentation
        
        Returns:
            Markdown list
        """
        indent = '  ' * depth
        lines = []
        
        for i, item in enumerate(items, 1):
            item_text = self._process_node(item, depth + 1)
            
            if ordered:
                lines.append(f"{indent}{i}. {item_text}")
            else:
                lines.append(f"{indent}- {item_text}")
        
        return '\n'.join(lines)
    
    def _process_embedded_asset(self, node: Dict[str, Any]) -> str:
        """
        Process embedded asset (typically images).
        
        Args:
            node: Embedded asset node
        
        Returns:
            Markdown image syntax
        """
        data = node.get('data', {})
        target = data.get('target')
        
        if not target:
            logger.warning(
                f"⚠️ EMBEDDED_ASSET_MISSING_TARGET "
                f"skipping asset"
            )
            return ''
        
        # Extract asset details
        try:
            title = target.get('fields', {}).get('title', {}).get('en', 'Image')
            description = target.get('fields', {}).get('description', {}).get('en', '')
            file_data = target.get('fields', {}).get('file', {}).get('en', {})
            url = file_data.get('url', '')
            
            # Ensure HTTPS
            if url and not url.startswith('https:'):
                url = f"https:{url}" if url.startswith('//') else url
            
            # Use description as alt text, fallback to title
            alt_text = description if description else title
            
            return f"![{alt_text}]({url})"
            
        except Exception as e:
            logger.warning(
                f"⚠️ EMBEDDED_ASSET_PROCESSING_FAILED "
                f"error={str(e)}"
            )
            return ''
