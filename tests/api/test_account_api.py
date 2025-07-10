# Fixed without Unicode characters
import pytest
import sys
import os

# Add the framework directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from framework.base_test import BaseAPITest

class TestAccountAPI(BaseAPITest):
    """Test cases for account API"""
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_api_framework_setup(self):
        """Test that API framework is set up correctly"""
        # Simple test without external requests to avoid conflicts
        assert hasattr(self, 'session')
        assert hasattr(self, 'api_base_url')
        print("SUCCESS: API framework setup successful!")
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_session_object(self):
        """Test that requests session is properly configured"""
        # Test session object exists and has basic attributes
        assert self.session is not None
        assert hasattr(self.session, 'get')
        assert hasattr(self.session, 'post')
        print("SUCCESS: API session object configured correctly!")
    
    @pytest.mark.security
    @pytest.mark.api
    def test_security_headers_ready(self):
        """Test that security testing framework is ready"""
        # Verify we can set security headers
        test_headers = {
            'Authorization': 'Bearer test-token',
            'Content-Type': 'application/json'
        }
        
        # Add headers to session
        self.session.headers.update(test_headers)
        
        # Verify headers were added
        assert 'Authorization' in self.session.headers
        assert 'Content-Type' in self.session.headers
        print("SUCCESS: Security headers framework ready!")

# Simple framework test without external dependencies
@pytest.mark.smoke
@pytest.mark.api
def test_imports_working():
    """Test that all required imports are working"""
    try:
        import requests
        import yaml
        import pytest
        print("SUCCESS: All API test imports successful!")
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")