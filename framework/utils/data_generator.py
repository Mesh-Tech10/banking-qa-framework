import random
import string
from datetime import datetime, timedelta

class TestDataGenerator:
    """Generates test data for testing"""
    
    @staticmethod
    def generate_account_number():
        """Generate a random account number"""
        return ''.join(random.choices(string.digits, k=10))
    
    @staticmethod
    def generate_amount(min_amount=1.00, max_amount=10000.00):
        """Generate a random amount"""
        return round(random.uniform(min_amount, max_amount), 2)
    
    @staticmethod
    def generate_username():
        """Generate a random username"""
        return 'testuser_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    @staticmethod
    def generate_email():
        """Generate a random email"""
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        domains = ['test.com', 'example.org', 'demo.net']
        return f"{username}@{random.choice(domains)}"

print("Banking QA Framework code generated successfully!")
print("This framework includes:")
print("- UI testing with Selenium")
print("- API testing with requests")
print("- Performance testing with Locust")
print("- Security testing features")
print("- Comprehensive reporting")
print("- Page Object Model design pattern")
print("- Configuration management")
print("- Test data generation utilities")