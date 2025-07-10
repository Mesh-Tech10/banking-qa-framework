# framework/base_test.py - Updated with manual ChromeDriver support
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import os
import time

class BaseTest:
    """Base class for all tests"""
    
    @classmethod
    def setup_class(cls):
        """Setup that runs once before all tests in a class"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'test_config.yaml')
        with open(config_path, 'r') as file:
            cls.config = yaml.safe_load(file)
    
    def setup_method(self):
        """Setup that runs before each test method"""
        print(f"Starting test: {self._get_test_name()}")
    
    def teardown_method(self):
        """Cleanup that runs after each test method"""
        print(f"Finished test: {self._get_test_name()}")
    
    def _get_test_name(self):
        """Get the current test method name"""
        return self.__class__.__name__

class BaseUITest(BaseTest):
    """Base class for UI tests using Selenium"""
    
    def setup_method(self):
        """Setup browser for UI tests"""
        super().setup_method()
        
        # Setup Chrome browser options
        chrome_options = Options()
        
        # Essential Chrome arguments for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Set window size
        window_size = self.config.get('browser', {}).get('window_size', '1920,1080')
        chrome_options.add_argument(f'--window-size={window_size}')
        
        # Set headless mode if specified
        if self.config.get('browser', {}).get('headless', False):
            chrome_options.add_argument('--headless')
        
        # Try multiple ChromeDriver setup methods
        driver_created = False
        
        # Method 1: Manual ChromeDriver (highest priority)
        manual_driver_path = os.path.join(os.path.dirname(__file__), '..', 'chromedriver.exe')
        if os.path.exists(manual_driver_path):
            try:
                print("🔧 Using manual ChromeDriver...")
                service = Service(manual_driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Manual ChromeDriver successful")
                driver_created = True
            except Exception as e:
                print(f"⚠️ Manual ChromeDriver failed: {e}")
        
        # Method 2: Try webdriver-manager (if manual failed)
        if not driver_created:
            try:
                print("🔧 Trying webdriver-manager...")
                from webdriver_manager.chrome import ChromeDriverManager
                
                # Clear cache and reinstall
                driver_path = ChromeDriverManager().install()
                
                # Verify the downloaded file is actually chromedriver.exe
                if driver_path.endswith('chromedriver.exe') or driver_path.endswith('chromedriver'):
                    service = Service(driver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    print("✅ webdriver-manager successful")
                    driver_created = True
                else:
                    print(f"⚠️ Invalid ChromeDriver path: {driver_path}")
                    
            except Exception as e:
                print(f"⚠️ webdriver-manager failed: {e}")
        
        # Method 3: Try system PATH ChromeDriver
        if not driver_created:
            try:
                print("🔧 Trying system PATH ChromeDriver...")
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✅ System ChromeDriver successful")
                driver_created = True
            except Exception as e:
                print(f"⚠️ System ChromeDriver failed: {e}")
        
        # If all methods failed, provide helpful error
        if not driver_created:
            error_msg = """

❌ ChromeDriver setup failed with all methods!

SOLUTION 1 - Manual Download (Recommended):
1. Run: python manual_chromedriver_setup.py
2. This will download the correct ChromeDriver for your Chrome version

SOLUTION 2 - Manual Steps:
1. Go to: https://googlechromelabs.github.io/chrome-for-testing/
2. Find "Stable" section
3. Download ChromeDriver for Windows (win64)
4. Extract chromedriver.exe to your project folder
5. Run tests again

SOLUTION 3 - Alternative Browser:
1. Install Firefox: https://www.mozilla.org/firefox/
2. Run: pip install geckodriver-autoinstaller
3. Use Firefox tests instead

Your Chrome version: 137.0.7151.122
"""

            raise Exception(error_msg)
        
        # Set implicit wait timeout
        timeout = self.config.get('app', {}).get('timeout', 30)
        self.driver.implicitly_wait(timeout)
        
        # Brief pause to ensure browser is ready
        time.sleep(1)
        print("✅ Browser setup complete")
    
    def teardown_method(self):
        """Close browser after UI tests"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                print("✅ Browser closed successfully")
            except Exception as e:
                print(f"⚠️ Warning: Error closing driver: {e}")
        super().teardown_method()

class BaseAPITest(BaseTest):
    """Base class for API tests"""
    
    def setup_method(self):
        """Setup for API tests"""
        super().setup_method()
        self.api_base_url = self.config.get('app', {}).get('api_base_url', 'https://api.example.com')
        self.session = requests.Session()
        print("✅ API client setup complete")