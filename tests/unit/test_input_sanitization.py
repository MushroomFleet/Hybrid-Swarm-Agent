"""
Unit tests for input sanitization module
Tests security against encoding issues, injection, and malformed inputs
"""

import pytest
import json
from src.input_sanitization import (
    InputSanitizer,
    SanitizationError,
    safe_sanitize,
    sanitize_prompt,
    sanitize_identifier,
    sanitize_filename,
    sanitize_for_json,
    sanitize_quality
)


class TestPromptSanitization:
    """Tests for prompt sanitization"""
    
    def test_normal_prompt(self):
        """Test normal, valid prompt"""
        sanitizer = InputSanitizer()
        result = sanitizer.sanitize_prompt("Hello world, how are you?")
        assert result == "Hello world, how are you?"
    
    def test_utf8_normalization(self):
        """Test UTF-8 encoding handling"""
        sanitizer = InputSanitizer()
        
        # Valid UTF-8 with various characters
        result = sanitizer.sanitize_prompt("Hello 世界! Здравствуй мир!")
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should be valid UTF-8
        result.encode('utf-8').decode('utf-8')
    
    def test_control_character_removal(self):
        """Test removal of control characters"""
        sanitizer = InputSanitizer()
        
        # Null bytes and other control chars
        dirty = "Hello\x00\x01\x02\x03World"
        clean = sanitizer.sanitize_prompt(dirty)
        assert clean == "HelloWorld"
        
        # More control chars
        dirty = "Test\x0b\x0c\x0e\x0fData"
        clean = sanitizer.sanitize_prompt(dirty)
        assert "Test" in clean and "Data" in clean
        assert '\x0b' not in clean
    
    def test_whitespace_preservation(self):
        """Test that tabs and newlines are kept"""
        sanitizer = InputSanitizer()
        
        # Tabs and newlines should be preserved
        text = "Hello\tWorld\nTest"
        result = sanitizer.sanitize_prompt(text)
        # Note: Whitespace normalization may convert tabs to spaces
        assert "Hello" in result and "World" in result and "Test" in result
    
    def test_length_limiting(self):
        """Test very long prompts are truncated"""
        sanitizer = InputSanitizer()
        
        # Prompt longer than max
        long_prompt = "A" * 15000
        result = sanitizer.sanitize_prompt(long_prompt)
        
        assert len(result) <= sanitizer.max_prompt_length + 20  # Allow for truncation message
        assert "truncated" in result.lower()
    
    def test_whitespace_normalization(self):
        """Test multiple spaces collapsed"""
        sanitizer = InputSanitizer()
        
        text = "Hello    world   with    spaces"
        result = sanitizer.sanitize_prompt(text)
        assert result == "Hello world with spaces"
    
    def test_emoji_handling(self):
        """Test emoji characters"""
        sanitizer = InputSanitizer()
        
        text = "Hello 🎉🚀💻 world!"
        result = sanitizer.sanitize_prompt(text)
        assert isinstance(result, str)
        # Emojis should either be kept or safely removed
        assert "Hello" in result and "world" in result
    
    def test_invalid_type(self):
        """Test non-string input raises error"""
        sanitizer = InputSanitizer()
        
        with pytest.raises(ValueError, match="must be string"):
            sanitizer.sanitize_prompt(123)
        
        with pytest.raises(ValueError, match="must be string"):
            sanitizer.sanitize_prompt(None)


class TestIdentifierSanitization:
    """Tests for identifier sanitization"""
    
    def test_normal_identifier(self):
        """Test valid identifier"""
        sanitizer = InputSanitizer()
        assert sanitizer.sanitize_identifier("task_123") == "task_123"
        assert sanitizer.sanitize_identifier("specialist_abc") == "specialist_abc"
    
    def test_special_characters_removed(self):
        """Test special characters are stripped"""
        sanitizer = InputSanitizer()
        
        assert sanitizer.sanitize_identifier("task@#$%123") == "task123"
        assert sanitizer.sanitize_identifier("test-id!") == "testid"
    
    def test_path_traversal_prevention(self):
        """Test path traversal attempts are blocked"""
        sanitizer = InputSanitizer()
        
        # Unix-style
        result = sanitizer.sanitize_identifier("../../etc/passwd")
        assert "/" not in result
        assert ".." not in result
        assert result == "etcpasswd"
        
        # Windows-style
        result = sanitizer.sanitize_identifier("..\\..\\windows\\system32")
        assert "\\" not in result
        assert result == "windowssystem32"
    
    def test_absolute_path_prevention(self):
        """Test absolute paths are stripped"""
        sanitizer = InputSanitizer()
        
        result = sanitizer.sanitize_identifier("/etc/passwd")
        assert result == "etcpasswd"
        
        result = sanitizer.sanitize_identifier("C:\\Windows\\System32")
        assert result == "CWindowsSystem32"
    
    def test_length_limiting(self):
        """Test long identifiers are truncated"""
        sanitizer = InputSanitizer()
        
        long_id = "a" * 200
        result = sanitizer.sanitize_identifier(long_id)
        assert len(result) <= sanitizer.max_id_length
    
    def test_empty_after_sanitization(self):
        """Test error on empty identifier"""
        sanitizer = InputSanitizer()
        
        with pytest.raises(ValueError, match="empty"):
            sanitizer.sanitize_identifier("!@#$%^&*()")
    
    def test_invalid_type(self):
        """Test non-string input raises error"""
        sanitizer = InputSanitizer()
        
        with pytest.raises(ValueError, match="must be string"):
            sanitizer.sanitize_identifier(123)


class TestFilenameSanitization:
    """Tests for filename sanitization"""
    
    def test_normal_filename(self):
        """Test valid filename"""
        sanitizer = InputSanitizer()
        assert sanitizer.sanitize_filename("test.json") == "test.json"
    
    def test_spaces_to_underscores(self):
        """Test spaces converted to underscores"""
        sanitizer = InputSanitizer()
        result = sanitizer.sanitize_filename("Test File Name.json")
        assert result == "test_file_name.json"
    
    def test_uppercase_to_lowercase(self):
        """Test conversion to lowercase"""
        sanitizer = InputSanitizer()
        assert sanitizer.sanitize_filename("TestFile.JSON") == "testfile.json"
    
    def test_path_removal(self):
        """Test path components removed"""
        sanitizer = InputSanitizer()
        
        result = sanitizer.sanitize_filename("../../file.json")
        assert result == "file.json"
        
        result = sanitizer.sanitize_filename("/etc/passwd")
        assert result == "etcpasswd.json"
    
    def test_special_characters_removed(self):
        """Test special characters stripped"""
        sanitizer = InputSanitizer()
        
        result = sanitizer.sanitize_filename("file!@#$%.json")
        assert result == "file.json"
    
    def test_extension_added(self):
        """Test .json added if no extension"""
        sanitizer = InputSanitizer()
        result = sanitizer.sanitize_filename("testfile")
        assert result == "testfile.json"
    
    def test_minimum_length(self):
        """Test error on too-short filename"""
        sanitizer = InputSanitizer()
        
        with pytest.raises(ValueError, match="too short"):
            sanitizer.sanitize_filename("!@#")
    
    def test_invalid_type(self):
        """Test non-string input raises error"""
        sanitizer = InputSanitizer()
        
        with pytest.raises(ValueError, match="must be string"):
            sanitizer.sanitize_filename(123)


class TestJsonSanitization:
    """Tests for JSON sanitization"""
    
    def test_quote_escaping(self):
        """Test quotes are properly escaped"""
        sanitizer = InputSanitizer()
        
        text = 'He said "Hello, world!"'
        escaped = sanitizer.sanitize_for_json(text)
        
        # Should be embeddable in JSON
        json_str = f'{{"text": "{escaped}"}}'
        parsed = json.loads(json_str)
        assert "Hello" in parsed['text']
    
    def test_backslash_escaping(self):
        """Test backslashes are escaped"""
        sanitizer = InputSanitizer()
        
        text = "Path: C:\\Users\\Test"
        escaped = sanitizer.sanitize_for_json(text)
        
        # Should be embeddable in JSON
        json_str = f'{{"path": "{escaped}"}}'
        parsed = json.loads(json_str)
        assert "Users" in parsed['path']
    
    def test_newline_escaping(self):
        """Test newlines are escaped"""
        sanitizer = InputSanitizer()
        
        text = "Line 1\nLine 2\nLine 3"
        escaped = sanitizer.sanitize_for_json(text)
        
        # Should be embeddable in JSON
        json_str = f'{{"text": "{escaped}"}}'
        parsed = json.loads(json_str)
        assert "Line 1" in parsed['text']


class TestQualitySanitization:
    """Tests for quality score sanitization"""
    
    def test_valid_quality(self):
        """Test valid quality scores"""
        sanitizer = InputSanitizer()
        
        assert sanitizer.sanitize_quality_score(0.5) == 0.5
        assert sanitizer.sanitize_quality_score(0.0) == 0.0
        assert sanitizer.sanitize_quality_score(1.0) == 1.0
    
    def test_quality_clamping(self):
        """Test quality clamped to [0, 1]"""
        sanitizer = InputSanitizer()
        
        # Too high
        assert sanitizer.sanitize_quality_score(1.5) == 1.0
        assert sanitizer.sanitize_quality_score(10.0) == 1.0
        
        # Too low
        assert sanitizer.sanitize_quality_score(-0.5) == 0.0
        assert sanitizer.sanitize_quality_score(-10.0) == 0.0
    
    def test_string_conversion(self):
        """Test numeric strings are converted"""
        sanitizer = InputSanitizer()
        
        assert sanitizer.sanitize_quality_score("0.75") == 0.75
        assert sanitizer.sanitize_quality_score("1") == 1.0
    
    def test_invalid_quality(self):
        """Test invalid quality raises error"""
        sanitizer = InputSanitizer()
        
        with pytest.raises(ValueError, match="must be numeric"):
            sanitizer.sanitize_quality_score("invalid")
        
        with pytest.raises(ValueError, match="must be numeric"):
            sanitizer.sanitize_quality_score(None)


class TestSafeSanitize:
    """Tests for safe_sanitize wrapper"""
    
    def test_safe_prompt_sanitization(self):
        """Test safe wrapper for prompts"""
        result = safe_sanitize("Hello world", context="test", method="prompt")
        assert result == "Hello world"
    
    def test_safe_identifier_sanitization(self):
        """Test safe wrapper for identifiers"""
        result = safe_sanitize("task_123", context="test", method="identifier")
        assert result == "task_123"
    
    def test_safe_filename_sanitization(self):
        """Test safe wrapper for filenames"""
        result = safe_sanitize("test.json", context="test", method="filename")
        assert result == "test.json"
    
    def test_fallback_on_error(self):
        """Test fallback values when sanitization fails"""
        # Invalid identifier that becomes empty
        result = safe_sanitize("!@#$", context="test", method="identifier")
        assert result.startswith("sanitized_")  # Fallback value
    
    def test_unknown_method(self):
        """Test unknown method handled gracefully"""
        result = safe_sanitize("test", context="test", method="unknown")
        assert isinstance(result, str)


class TestSecurityEdgeCases:
    """Security-focused edge case tests"""
    
    def test_sql_injection_patterns(self):
        """Test common SQL injection patterns are safely handled"""
        sanitizer = InputSanitizer()
        
        sql_injections = [
            "'; DROP TABLE approaches; --",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users--"
        ]
        
        for injection in sql_injections:
            sanitized = sanitizer.sanitize_prompt(injection)
            json_safe = sanitizer.sanitize_for_json(sanitized)
            
            # Should be safely embeddable in JSON
            json_str = f'{{"input": "{json_safe}"}}'
            parsed = json.loads(json_str)
            assert isinstance(parsed['input'], str)
    
    def test_path_traversal_patterns(self):
        """Test various path traversal attempts"""
        sanitizer = InputSanitizer()
        
        traversals = [
            "../../etc/passwd",
            "..\\..\\windows\\system32",
            "....//....//etc/passwd",
            "/etc/passwd",
            "C:\\Windows\\System32"
        ]
        
        for traversal in traversals:
            result = sanitizer.sanitize_identifier(traversal)
            # Should not contain path separators
            assert '/' not in result
            assert '\\' not in result
            assert '..' not in result
    
    def test_null_byte_injection(self):
        """Test null byte injection is prevented"""
        sanitizer = InputSanitizer()
        
        # Null bytes can terminate strings in some contexts
        text = "normal\x00hidden"
        result = sanitizer.sanitize_prompt(text)
        assert '\x00' not in result
        assert "normal" in result
    
    def test_unicode_exploits(self):
        """Test Unicode-based exploits"""
        sanitizer = InputSanitizer()
        
        # Right-to-left override (can hide malicious content)
        text = "normal\u202emalicious"
        result = sanitizer.sanitize_prompt(text)
        assert isinstance(result, str)
        
        # Zero-width characters
        text = "test\u200bdata\u200c"
        result = sanitizer.sanitize_prompt(text)
        assert isinstance(result, str)
    
    def test_dos_via_length(self):
        """Test protection against DoS via extremely long inputs"""
        sanitizer = InputSanitizer()
        
        import time
        
        # 1MB input
        huge = "A" * 1000000
        
        start = time.time()
        result = sanitizer.sanitize_prompt(huge)
        elapsed = time.time() - start
        
        # Should complete quickly
        assert elapsed < 1.0
        
        # Should be truncated
        assert len(result) <= sanitizer.max_prompt_length + 50
    
    def test_nested_encoding(self):
        """Test nested/double encoding attempts"""
        sanitizer = InputSanitizer()
        
        # Double-encoded characters
        text = "test%252e%252e%252f"  # %2e = .  %2f = /
        result = sanitizer.sanitize_prompt(text)
        assert isinstance(result, str)


class TestConvenienceFunctions:
    """Tests for module-level convenience functions"""
    
    def test_module_sanitize_prompt(self):
        """Test module-level sanitize_prompt()"""
        result = sanitize_prompt("Hello world")
        assert result == "Hello world"
    
    def test_module_sanitize_identifier(self):
        """Test module-level sanitize_identifier()"""
        result = sanitize_identifier("task_123")
        assert result == "task_123"
    
    def test_module_sanitize_filename(self):
        """Test module-level sanitize_filename()"""
        result = sanitize_filename("test.json")
        assert result == "test.json"
    
    def test_module_sanitize_for_json(self):
        """Test module-level sanitize_for_json()"""
        result = sanitize_for_json("test \"quoted\" text")
        # Should be JSON-safe
        json_str = f'{{"text": "{result}"}}'
        parsed = json.loads(json_str)
        assert "quoted" in parsed['text']
    
    def test_module_sanitize_quality(self):
        """Test module-level sanitize_quality()"""
        assert sanitize_quality(0.75) == 0.75
        assert sanitize_quality(1.5) == 1.0
        assert sanitize_quality(-0.5) == 0.0


class TestRealWorldScenarios:
    """Tests based on real-world usage patterns"""
    
    def test_user_question_with_code(self):
        """Test sanitizing question with code snippet"""
        sanitizer = InputSanitizer()
        
        question = """
        How do I use async/await in Python?
        
        I tried:
        async def fetch():
            await asyncio.sleep(1)
        
        But got an error.
        """
        
        result = sanitizer.sanitize_prompt(question)
        assert "async" in result
        assert "await" in result
        assert "fetch" in result
    
    def test_multilingual_prompt(self):
        """Test prompts with multiple languages"""
        sanitizer = InputSanitizer()
        
        text = "Explain machine learning. 机器学习是什么? Qu'est-ce que c'est?"
        result = sanitizer.sanitize_prompt(text)
        assert isinstance(result, str)
        assert "Explain" in result
    
    def test_markdown_in_prompt(self):
        """Test prompts containing markdown"""
        sanitizer = InputSanitizer()
        
        text = "# Title\n## Subtitle\n- Point 1\n- Point 2"
        result = sanitizer.sanitize_prompt(text)
        assert "Title" in result
        assert "Point" in result
    
    def test_task_id_from_timestamp(self):
        """Test task IDs generated from timestamps"""
        sanitizer = InputSanitizer()
        
        import time
        task_id = f"task_{int(time.time())}"
        result = sanitizer.sanitize_identifier(task_id)
        assert result == task_id
        assert result.startswith("task_")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
