# Script to check Chrome and ChromeDriver setup
import os
import subprocess
import sys

def check_chrome_version():
    """Check Chrome browser version"""
    print("🔍 Checking Chrome browser installation...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            try:
                result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True, timeout=10)
                print(f"✅ Chrome found: {result.stdout.strip()}")
                return chrome_path
            except Exception as e:
                print(f"⚠️ Chrome found but version check failed: {e}")
                return chrome_path
    
    print("❌ Chrome browser not found!")
    print("Please install Chrome from: https://www.google.com/chrome/")
    return None

def check_webdriver_manager():
    """Check webdriver-manager installation"""
    print("\n🔍 Checking webdriver-manager...")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ webdriver-manager is installed")
        
        # Try to get ChromeDriver
        print("🔍 Attempting to download/locate ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver located at: {driver_path}")
        
        # Check if the file exists and is executable
        if os.path.exists(driver_path):
            print(f"✅ ChromeDriver file exists: {os.path.getsize(driver_path)} bytes")
            return driver_path
        else:
            print(f"❌ ChromeDriver file does not exist at: {driver_path}")
            return None
            
    except Exception as e:
        print(f"❌ webdriver-manager error: {e}")
        return None

def test_selenium_basic():
    """Test basic Selenium functionality"""
    print("\n🔍 Testing Selenium WebDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Try to create WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test navigation
        driver.get("https://example.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Selenium test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

def main():
    """Main function to run all checks"""
    print("🧪 Banking QA Framework - Chrome Setup Checker")
    print("=" * 50)
    
    # Check Chrome
    chrome_path = check_chrome_version()
    
    # Check webdriver-manager
    driver_path = check_webdriver_manager()
    
    # Test Selenium
    selenium_works = test_selenium_basic()
    
    print("\n📋 SUMMARY:")
    print("=" * 30)
    print(f"Chrome Browser: {'✅ OK' if chrome_path else '❌ NOT FOUND'}")
    print(f"ChromeDriver: {'✅ OK' if driver_path else '❌ NOT FOUND'}")
    print(f"Selenium Test: {'✅ PASSED' if selenium_works else '❌ FAILED'}")
    
    if chrome_path and driver_path and selenium_works:
        print("\n🎉 All checks passed! Your setup should work.")
    else:
        print("\n🔧 Setup issues detected. Please follow the fix instructions below:")
        
        if not chrome_path:
            print("   1. Install Chrome browser from: https://www.google.com/chrome/")
        
        if not driver_path:
            print("   2. Try: pip install --upgrade webdriver-manager")
        
        if not selenium_works:
            print("   3. Try: pip install --upgrade selenium")
            print("   4. Restart your command prompt")

if __name__ == "__main__":
    main()