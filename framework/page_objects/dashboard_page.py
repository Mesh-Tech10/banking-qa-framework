from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """Page Object for Dashboard page"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Define page elements
        self.welcome_message = (By.CLASS_NAME, "welcome-message")
        self.account_balance = (By.ID, "account-balance")
        self.logout_button = (By.ID, "logout-btn")
    
    def is_welcome_message_displayed(self):
        """Check if welcome message is displayed"""
        try:
            self.wait.until(EC.presence_of_element_located(self.welcome_message))
            return True
        except:
            return False
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_account_balance(self):
        """Get account balance from dashboard"""
        element = self.wait.until(EC.presence_of_element_located(self.account_balance))
        return element.text