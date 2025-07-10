from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """Page Object for Login page"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        # Define page elements (locators)
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-btn")
        self.error_message = (By.CLASS_NAME, "error-message")
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.driver.get("https://demo-bank.com/login")
    
    def enter_username(self, username):
        """Enter username in the username field"""
        element = self.wait.until(EC.presence_of_element_located(self.username_field))
        element.clear()
        element.send_keys(username)
    
    def enter_password(self, password):
        """Enter password in the password field"""
        element = self.wait.until(EC.presence_of_element_located(self.password_field))
        element.clear()
        element.send_keys(password)
    
    def click_login(self):
        """Click the login button"""
        element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        element.click()
        
        # Return dashboard page object after successful login
        from .dashboard_page import DashboardPage
        return DashboardPage(self.driver)
    
    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        try:
            self.wait.until(EC.presence_of_element_located(self.error_message))
            return True
        except:
            return False
    
    def get_error_message(self):
        """Get the error message text"""
        element = self.driver.find_element(*self.error_message)
        return element.text