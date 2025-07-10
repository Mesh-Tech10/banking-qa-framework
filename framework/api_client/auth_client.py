import requests
import json

class AuthClient:
    """API client for authentication operations"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, username, password):
        """Login via API and get authentication token"""
        login_data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        return response
    
    def logout(self, token):
        """Logout using authentication token"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = self.session.post(
            f"{self.base_url}/auth/logout",
            headers=headers
        )
        
        return response
