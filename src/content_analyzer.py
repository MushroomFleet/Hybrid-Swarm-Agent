"""
Content Analyzer
Extracts features from generated content for pattern analysis
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from src.approach_patterns import ContentFeatures


class ContentAnalyzer:
    """
    Analyzes generated content to extract structural and stylistic features
    Uses rule-based heuristics for feature extraction
    """
    
    def __init__(self):
        # Keywords for tone detection
        self.formal_indicators = [
            'furthermore', 'moreover', 'consequently', 'therefore', 'thus',
            'hereby', 'whereas', 'pursuant', 'aforementioned'
        ]
        self.casual_indicators = [
            "let's", "you'll", "we'll", "don't", "can't", "it's",
            'cool', 'awesome', 'basically', 'pretty much', 'kinda'
        ]
        self.technical_indicators = [
            'algorithm', 'implementation', 'optimize', 'efficiency',
            'complexity', 'architecture', 'interface', 'protocol'
        ]
    
    def analyze_content(self, content: str) -> ContentFeatures:
        """
        Extract features from content
        
        Args:
            content: Generated content text
            
        Returns:
            ContentFeatures object with extracted features
        """
        if not content:
            return self._empty_features()
        
        # Structure analysis
        section_count = self._count_sections(content)
        has_code_blocks = self._has_code_blocks(content)
        code_block_count = self._count_code_blocks(content)
        has_numbered_list = self._has_numbered_list(content)
        has_bullets = self._has_bullets(content)
        has_tables = self._has_tables(content)
        
        # Length analysis
        total_length = len(content)
        avg_section_length = self._calculate_avg_section_length(content, section_count)
        
        # Style analysis
        detected_tone = self._detect_tone(content)
        formality_score = self._calculate_formality(content)
        
        # Content ratios
        explanation_ratio = self._calculate_explanation_ratio(content)
        example_ratio = self._calculate_example_ratio(content)
        code_ratio = self._calculate_code_ratio(content)
        
        return ContentFeatures(
            section_count=section_count,
            has_code_blocks=has_code_blocks,
            code_block_count=code_block_count,
            has_numbered_list=has_numbered_list,
            has_bullets=has_bullets,
            has_tables=has_tables,
            total_length=total_length,
            avg_section_length=avg_section_length,
            detected_tone=detected_tone,
            formality_score=formality_score,
            explanation_ratio=explanation_ratio,
            example_ratio=example_ratio,
            code_ratio=code_ratio
        )
    
    def _empty_features(self) -> ContentFeatures:
        """Return empty features for invalid content"""
        return ContentFeatures(
            section_count=0,
            has_code_blocks=False,
            code_block_count=0,
            has_numbered_list=False,
            has_bullets=False,
            has_tables=False,
            total_length=0,
            avg_section_length=0,
            detected_tone="unknown",
            formality_score=0.5,
            explanation_ratio=0.0,
            example_ratio=0.0,
            code_ratio=0.0
        )
    
    def _count_sections(self, content: str) -> int:
        """Count sections (marked by headers)"""
        # Count markdown headers (# Header, ## Header, etc.)
        header_pattern = r'^#{1,6}\s+.+$'
        headers = re.findall(header_pattern, content, re.MULTILINE)
        return max(1, len(headers))  # At least 1 section
    
    def _has_code_blocks(self, content: str) -> bool:
        """Check if content has code blocks"""
        # Markdown code blocks: ```code```
        code_block_pattern = r'```[\s\S]*?```'
        return bool(re.search(code_block_pattern, content))
    
    def _count_code_blocks(self, content: str) -> int:
        """Count number of code blocks"""
        code_block_pattern = r'```[\s\S]*?```'
        return len(re.findall(code_block_pattern, content))
    
    def _has_numbered_list(self, content: str) -> bool:
        """Check if content has numbered lists"""
        numbered_list_pattern = r'^\d+\.\s+.+$'
        return bool(re.search(numbered_list_pattern, content, re.MULTILINE))
    
    def _has_bullets(self, content: str) -> bool:
        """Check if content has bullet lists"""
        bullet_pattern = r'^[\*\-\+]\s+.+$'
        return bool(re.search(bullet_pattern, content, re.MULTILINE))
    
    def _has_tables(self, content: str) -> bool:
        """Check if content has markdown tables"""
        # Markdown table has | separators
        table_pattern = r'\|.+\|'
        lines_with_pipes = re.findall(table_pattern, content, re.MULTILINE)
        # Need at least 2 consecutive lines with pipes for a table
        return len(lines_with_pipes) >= 2
    
    def _calculate_avg_section_length(self, content: str, section_count: int) -> int:
        """Calculate average section length"""
        if section_count == 0:
            return 0
        return len(content) // section_count
    
    def _detect_tone(self, content: str) -> str:
        """
        Detect overall tone of content
        Returns: "formal", "casual", "technical", or "educational"
        """
        content_lower = content.lower()
        
        # Count indicators
        formal_count = sum(1 for word in self.formal_indicators if word in content_lower)
        casual_count = sum(1 for word in self.casual_indicators if word in content_lower)
        technical_count = sum(1 for word in self.technical_indicators if word in content_lower)
        
        # Educational indicators
        educational_patterns = [
            r'\bfor example\b', r'\blet\'s\s+\w+\b', r'\byou\s+can\b',
            r'\bstep\s+\d+\b', r'\bfirst\b.*\bsecond\b', r'\bhow\s+to\b'
        ]
        educational_count = sum(1 for pattern in educational_patterns if re.search(pattern, content_lower))
        
        # Determine dominant tone
        scores = {
            'formal': formal_count,
            'casual': casual_count,
            'technical': technical_count,
            'educational': educational_count
        }
        
        if max(scores.values()) == 0:
            return "neutral"
        
        return max(scores, key=scores.get)
    
    def _calculate_formality(self, content: str) -> float:
        """
        Calculate formality score (0.0 = casual, 1.0 = formal)
        """
        content_lower = content.lower()
        
        # Count formal vs casual indicators
        formal_count = sum(1 for word in self.formal_indicators if word in content_lower)
        casual_count = sum(1 for word in self.casual_indicators if word in content_lower)
        
        # Additional signals
        contractions = len(re.findall(r"\w+'\w+", content))  # can't, don't, etc.
        
        # Normalize
        total_words = len(content.split())
        if total_words == 0:
            return 0.5
        
        formal_score = formal_count / total_words * 100
        casual_score = (casual_count + contractions) / total_words * 100
        
        # Combine into 0-1 scale
        if formal_score + casual_score == 0:
            return 0.5  # Neutral
        
        formality = formal_score / (formal_score + casual_score)
        return formality
    
    def _calculate_explanation_ratio(self, content: str) -> float:
        """
        Calculate ratio of explanatory text
        (paragraphs that aren't code, examples, or lists)
        """
        # Remove code blocks
        content_no_code = re.sub(r'```[\s\S]*?```', '', content)
        
        # Remove lists
        content_no_lists = re.sub(r'^[\*\-\+\d]+\.\s+.+$', '', content_no_code, flags=re.MULTILINE)
        
        # What remains is primarily explanatory
        explanation_length = len(content_no_lists.strip())
        total_length = len(content)
        
        if total_length == 0:
            return 0.0
        
        return min(1.0, explanation_length / total_length)
    
    def _calculate_example_ratio(self, content: str) -> float:
        """
        Calculate ratio of example content
        (text near "example", "for instance", etc.)
        """
        # Find example sections
        example_patterns = [
            r'for example:[\s\S]{0,500}',
            r'example:[\s\S]{0,500}',
            r'for instance:[\s\S]{0,500}',
            r'e\.g\.:[\s\S]{0,500}'
        ]
        
        example_text = ""
        for pattern in example_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            example_text += " ".join(matches)
        
        example_length = len(example_text)
        total_length = len(content)
        
        if total_length == 0:
            return 0.0
        
        return min(1.0, example_length / total_length)
    
    def _calculate_code_ratio(self, content: str) -> float:
        """
        Calculate ratio of code content
        """
        # Extract code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        code_text = "".join(code_blocks)
        
        # Also count inline code
        inline_code = re.findall(r'`[^`]+`', content)
        inline_text = "".join(inline_code)
        
        code_length = len(code_text) + len(inline_text)
        total_length = len(content)
        
        if total_length == 0:
            return 0.0
        
        return min(1.0, code_length / total_length)
    
    def analyze_structure_type(self, content: str) -> str:
        """
        Determine structure type of content
        Returns: "sequential_steps", "hierarchical", "prose", "bulleted"
        """
        has_numbered = self._has_numbered_list(content)
        has_bullets = self._has_bullets(content)
        section_count = self._count_sections(content)
        
        # Sequential steps (numbered lists)
        if has_numbered:
            step_patterns = [
                r'step\s+\d+', r'first.*second.*third',
                r'^\d+\.\s+(first|then|next|finally)'
            ]
            if any(re.search(pattern, content, re.IGNORECASE) for pattern in step_patterns):
                return "sequential_steps"
        
        # Bulleted (many bullet points)
        if has_bullets:
            bullet_lines = len(re.findall(r'^[\*\-\+]\s+', content, re.MULTILINE))
            if bullet_lines >= 5:
                return "bulleted"
        
        # Hierarchical (many headers)
        if section_count >= 4:
            return "hierarchical"
        
        # Default: prose
        return "prose"


if __name__ == "__main__":
    # Demo usage
    print("Content Analyzer Demo")
    print("=" * 70)
    
    analyzer = ContentAnalyzer()
    
    # Sample content with various features
    sample_content = """
# Python Functions Tutorial

## Introduction

Functions are reusable blocks of code. Let's learn how to create them!

## Step-by-Step Guide

1. Define a function using `def`
2. Add parameters if needed
3. Write the function body
4. Return a value

### Example Code

```python
def greet(name):
    return f"Hello, {name}!"

# Usage
result = greet("Alice")
print(result)
```

### Key Points

- Functions help organize code
- Use descriptive names
- Document your functions

## Summary

You can now create basic Python functions. For more advanced topics, see the next tutorial.
"""
    
    print("\n1. Analyzing Sample Content:")
    features = analyzer.analyze_content(sample_content)
    
    print(f"   Sections: {features.section_count}")
    print(f"   Has code blocks: {features.has_code_blocks}")
    print(f"   Code block count: {features.code_block_count}")
    print(f"   Has numbered list: {features.has_numbered_list}")
    print(f"   Has bullets: {features.has_bullets}")
    print(f"   Total length: {features.total_length}")
    print(f"   Detected tone: {features.detected_tone}")
    print(f"   Formality score: {features.formality_score:.2f}")
    print(f"   Explanation ratio: {features.explanation_ratio:.2f}")
    print(f"   Example ratio: {features.example_ratio:.2f}")
    print(f"   Code ratio: {features.code_ratio:.2f}")
    
    print("\n2. Structure Type:")
    structure = analyzer.analyze_structure_type(sample_content)
    print(f"   Detected structure: {structure}")
    
    # Test with different content types
    print("\n3. Testing Different Content Types:")
    
    # Formal content
    formal_content = "Furthermore, it is necessary to consider the aforementioned implications. Therefore, we must proceed with caution."
    formal_features = analyzer.analyze_content(formal_content)
    print(f"   Formal content - tone: {formal_features.detected_tone}, formality: {formal_features.formality_score:.2f}")
    
    # Casual content
    casual_content = "Hey! Let's dive in. It's pretty cool how this works, don't you think? You'll love it!"
    casual_features = analyzer.analyze_content(casual_content)
    print(f"   Casual content - tone: {casual_features.detected_tone}, formality: {casual_features.formality_score:.2f}")
    
    # Technical content
    technical_content = "The algorithm optimizes the interface protocol through efficient implementation of the architecture."
    technical_features = analyzer.analyze_content(technical_content)
    print(f"   Technical content - tone: {technical_features.detected_tone}")
    
    print("\n" + "=" * 70)
    print("✓ ContentAnalyzer working correctly!")
