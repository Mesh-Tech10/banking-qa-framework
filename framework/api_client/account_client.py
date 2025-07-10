import requests

class AccountClient:
    """API client for account operations"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def authenticate(self, username, password):
        """Authenticate and return token"""
        login_data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json=login_data
        )
        
        if response.status_code == 200:
            return response.json().get("token")
        return None
    
    def get_balance(self, account_number, token=None):
        """Get account balance"""
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = self.session.get(
            f"{self.base_url}/account/{account_number}/balance",
            headers=headers
        )
        
        return response
    
    def get_transactions(self, account_number, token):
        """Get account transactions"""
        headers = {"Authorization": f"Bearer {token}"}
        
        response = self.session.get(
            f"{self.base_url}/account/{account_number}/transactions",
            headers=headers
        )
        
        return response
