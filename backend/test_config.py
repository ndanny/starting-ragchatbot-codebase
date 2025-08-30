import os
import pytest
from unittest.mock import patch
from config import Config


class TestConfig:
    """Unit tests for the Config class"""

    def test_config_default_values(self):
        """Test that Config class has correct default values"""
        config = Config()
        
        assert config.ANTHROPIC_MODEL == "claude-sonnet-4-20250514"
        assert config.EMBEDDING_MODEL == "all-MiniLM-L6-v2"
        assert config.CHUNK_SIZE == 800
        assert config.CHUNK_OVERLAP == 100
        assert config.MAX_RESULTS == 5
        assert config.MAX_HISTORY == 2
        assert config.CHROMA_PATH == "./chroma_db"

    def test_config_has_api_key_from_env(self):
        """Test that Config loads ANTHROPIC_API_KEY (assuming it exists in environment)"""
        config = Config()
        # Just verify it's a string (could be empty or have value)
        assert isinstance(config.ANTHROPIC_API_KEY, str)

    def test_config_custom_initialization(self):
        """Test creating Config with custom values"""
        config = Config(
            ANTHROPIC_API_KEY="test-key",
            CHUNK_SIZE=1000,
            MAX_RESULTS=10
        )
        
        assert config.ANTHROPIC_API_KEY == "test-key"
        assert config.CHUNK_SIZE == 1000
        assert config.MAX_RESULTS == 10
        # Other values should remain default
        assert config.ANTHROPIC_MODEL == "claude-sonnet-4-20250514"

    def test_config_is_dataclass(self):
        """Test that Config is properly configured as a dataclass"""
        config = Config()
        assert hasattr(config, '__dataclass_fields__')
        
        # Check that all expected fields are present
        expected_fields = {
            'ANTHROPIC_API_KEY', 'ANTHROPIC_MODEL', 'EMBEDDING_MODEL',
            'CHUNK_SIZE', 'CHUNK_OVERLAP', 'MAX_RESULTS', 'MAX_HISTORY', 'CHROMA_PATH'
        }
        actual_fields = set(config.__dataclass_fields__.keys())
        assert expected_fields == actual_fields