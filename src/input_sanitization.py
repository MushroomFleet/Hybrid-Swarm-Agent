"""
Input Sanitization Module
Provides security against encoding issues, injection attacks, and malformed inputs
"""

import re
import json
from pathlib import Path
from typing import Optional


class SanitizationError(Exception):
    """Raised when input cannot be safely sanitized"""
    pass


class InputSanitizer:
    """Centralized input sanitization for all entry points"""
    
    def __init__(self):
        self.max_prompt_length = 10000
        self.max_id_length = 100
        self.allowed_filename_chars = set("abcdefghijklmnopqrstuvwxyz0123456789_-.")
    
    def sanitize_prompt(self, prompt: str) -> str:
        """
        Sanitize user prompt for processing
        
        Steps:
        1. UTF-8 normalization
        2. Control character removal
        3. Length limiting
        4. Whitespace normalization
        
        Args:
            prompt: Raw user input
            
        Returns:
            Sanitized prompt string
            
        Raises:
            ValueError: If prompt is not a string
        """
        if not isinstance(prompt, str):
            raise ValueError(f"Prompt must be string, got {type(prompt)}")
        
        # 1. UTF-8 encode/decode with error handling
        # This replaces invalid UTF-8 sequences with  (replacement character)
        prompt = prompt.encode('utf-8', errors='replace').decode('utf-8')
        
        # 2. Remove control characters (keep \t, \n)
        # Control characters (0x00-0x1F except tab and newline) can break terminals
        prompt = ''.join(
            char for char in prompt 
            if char.isprintable() or char in '\t\n'
        )
        
        # 3. Length limit (prevent DoS via huge inputs)
        if len(prompt) > self.max_prompt_length:
            prompt = prompt[:self.max_prompt_length]
            prompt += "... [truncated]"
        
        # 4. Normalize whitespace (collapse multiple spaces)
        prompt = ' '.join(prompt.split())
        
        return prompt
    
    def sanitize_identifier(self, identifier: str) -> str:
        """
        Sanitize IDs (task_id, specialist_id, approach_id)
        
        Requirements:
        - Alphanumeric + underscore only
        - Max length
        - No path traversal
        
        Args:
            identifier: Raw identifier string
            
        Returns:
            Sanitized identifier
            
        Raises:
            ValueError: If identifier becomes empty or is invalid
        """
        if not isinstance(identifier, str):
            raise ValueError(f"Identifier must be string, got {type(identifier)}")
        
        # Remove any path components (prevent path traversal)
        identifier = identifier.split('/')[-1].split('\\')[-1]
        
        # Keep only safe characters (alphanumeric + underscore)
        identifier = ''.join(
            char for char in identifier 
            if char.isalnum() or char == '_'
        )
        
        # Length limit
        identifier = identifier[:self.max_id_length]
        
        if not identifier:
            raise ValueError("Identifier became empty after sanitization")
        
        return identifier
    
    def sanitize_for_json(self, text: str) -> str:
        """
        Prepare text for JSON storage (escape quotes, backslashes)
        
        Args:
            text: Text to sanitize for JSON
            
        Returns:
            JSON-safe string
        """
        # Use json.dumps to properly escape, then remove surrounding quotes
        return json.dumps(text)[1:-1]
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for safe storage
        
        Args:
            filename: Raw filename
            
        Returns:
            Safe filename
        """
        if not isinstance(filename, str):
            raise ValueError(f"Filename must be string, got {type(filename)}")
        
        # Remove path components
        filename = filename.split('/')[-1].split('\\')[-1]
        
        # Convert to lowercase, replace spaces with underscores
        filename = filename.lower().replace(' ', '_')
        
        # Keep only allowed characters
        filename = ''.join(
            char for char in filename
            if char in self.allowed_filename_chars
        )
        
        # Ensure has extension
        if '.' not in filename:
            filename += '.json'
        
        # Minimum length check
        if len(filename) < 5:  # At least X.json
            raise ValueError(f"Filename too short after sanitization: {filename}")
        
        return filename
    
    def sanitize_quality_score(self, quality: float) -> float:
        """
        Sanitize quality score to valid range
        
        Args:
            quality: Raw quality score
            
        Returns:
            Quality score clamped to [0.0, 1.0]
        """
        try:
            quality = float(quality)
        except (ValueError, TypeError):
            raise ValueError(f"Quality must be numeric, got {quality}")
        
        # Clamp to valid range
        return max(0.0, min(1.0, quality))


def safe_sanitize(text: str, context: str = "input", method: str = "prompt") -> str:
    """
    Wrapper with error handling for sanitization
    
    Args:
        text: Text to sanitize
        context: Context for logging
        method: Sanitization method to use ('prompt', 'identifier', 'filename')
        
    Returns:
        Sanitized text or safe fallback
    """
    try:
        sanitizer = InputSanitizer()
        
        if method == "prompt":
            return sanitizer.sanitize_prompt(text)
        elif method == "identifier":
            return sanitizer.sanitize_identifier(text)
        elif method == "filename":
            return sanitizer.sanitize_filename(text)
        else:
            raise ValueError(f"Unknown sanitization method: {method}")
            
    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"WARNING: Sanitization failed for {context}: {e}")
        
        # Return safe fallback
        if method == "prompt":
            return "[Input could not be processed safely]"
        elif method == "identifier":
            return f"sanitized_{hash(text) % 1000000}"
        elif method == "filename":
            return "unknown.json"
        else:
            return ""


# Module-level sanitizer instance
_sanitizer = InputSanitizer()

# Convenience functions
def sanitize_prompt(prompt: str) -> str:
    """Module-level convenience function"""
    return _sanitizer.sanitize_prompt(prompt)

def sanitize_identifier(identifier: str) -> str:
    """Module-level convenience function"""
    return _sanitizer.sanitize_identifier(identifier)

def sanitize_filename(filename: str) -> str:
    """Module-level convenience function"""
    return _sanitizer.sanitize_filename(filename)

def sanitize_for_json(text: str) -> str:
    """Module-level convenience function"""
    return _sanitizer.sanitize_for_json(text)

def sanitize_quality(quality: float) -> float:
    """Module-level convenience function"""
    return _sanitizer.sanitize_quality_score(quality)


if __name__ == "__main__":
    # Demo usage
    print("Input Sanitization Module Demo")
    print("=" * 70)
    
    # Test prompt sanitization
    print("\n1. Prompt Sanitization:")
    test_prompts = [
        "Normal prompt",
        "Prompt with émojis 🎉 and spëcial çhars",
        "Very\x00Bad\x01Control\x02Characters",
        "A" * 15000  # Too long
    ]
    
    for prompt in test_prompts:
        try:
            sanitized = sanitize_prompt(prompt)
            print(f"   Input: {repr(prompt[:50])}")
            print(f"   Output: {repr(sanitized[:50])}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    
    # Test identifier sanitization
    print("\n2. Identifier Sanitization:")
    test_ids = [
        "task_123",
        "../../etc/passwd",
        "task@#$%123",
        ""
    ]
    
    for identifier in test_ids:
        try:
            sanitized = sanitize_identifier(identifier)
            print(f"   Input: {repr(identifier)}")
            print(f"   Output: {repr(sanitized)}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    
    # Test filename sanitization
    print("\n3. Filename Sanitization:")
    test_files = [
        "test.json",
        "Test File With Spaces.json",
        "../../etc/passwd",
        "file!@#$%.json"
    ]
    
    for filename in test_files:
        try:
            sanitized = sanitize_filename(filename)
            print(f"   Input: {repr(filename)}")
            print(f"   Output: {repr(sanitized)}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    
    print("=" * 70)
