import os
import requests
import zipfile
import shutil
from pathlib import Path

def download_correct_chromedriver():
    """Download the correct ChromeDriver for Chrome 137"""
    
    print("🔧 Fixing ChromeDriver download issue...")
    
    # Your Chrome version
    chrome_version = "137.0.7151.122"
    major_version = chrome_version.split('.')[0]  # 137
    
    print(f"Chrome version detected: {chrome_version}")
    print(f"Looking for ChromeDriver version: {major_version}")
    
    # Create downloads directory
    download_dir = Path("chromedriver_download")
    download_dir.mkdir(exist_ok=True)
    
    # ChromeDriver download URL for version 137
    chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/win64/chromedriver-win64.zip"
    
    try:
        print(f"📥 Downloading ChromeDriver from: {chromedriver_url}")
        
        # Download the zip file
        response = requests.get(chromedriver_url, stream=True)
        response.raise_for_status()
        
        zip_path = download_dir / "chromedriver.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Download completed!")
        
        # Extract the zip file
        print("📂 Extracting ChromeDriver...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
        
        # Find the chromedriver.exe file
        chromedriver_exe = None
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                if file == 'chromedriver.exe':
                    chromedriver_exe = os.path.join(root, file)
                    break
            if chromedriver_exe:
                break
        
        if chromedriver_exe:
            # Copy to project root
            project_chromedriver = "chromedriver.exe"
            shutil.copy2(chromedriver_exe, project_chromedriver)
            print(f"✅ ChromeDriver copied to: {os.path.abspath(project_chromedriver)}")
            
            # Clean up download directory
            shutil.rmtree(download_dir)
            
            return project_chromedriver
        else:
            print("❌ chromedriver.exe not found in downloaded files")
            return None
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def test_manual_chromedriver():
    """Test the manually downloaded ChromeDriver"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        print("\n🧪 Testing manually downloaded ChromeDriver...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Use the manual ChromeDriver
        service = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test navigation
        driver.get("https://example.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Manual ChromeDriver test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Manual ChromeDriver test failed: {e}")
        return False

def main():
    """Main function to fix ChromeDriver"""
    print("🛠️  ChromeDriver Manual Setup Tool")
    print("=" * 40)
    
    # Step 1: Download correct ChromeDriver
    chromedriver_path = download_correct_chromedriver()
    
    if chromedriver_path:
        # Step 2: Test it
        test_success = test_manual_chromedriver()
        
        if test_success:
            print("\n🎉 SUCCESS! ChromeDriver is now working correctly.")
            print("\n Next steps:")
            print("1. Run your tests again:")
            print("   pytest tests/ui/test_login.py::TestLogin::test_page_elements_exist -v")
            print("\n2. The framework will now use the manual ChromeDriver")
        else:
            print("\n❌ Manual setup failed. Please try alternative solutions.")
    else:
        print("\n❌ Could not download ChromeDriver. Please try manual download:")
        print("1. Go to: https://googlechromelabs.github.io/chrome-for-testing/")
        print("2. Download ChromeDriver for version 137")
        print("3. Extract chromedriver.exe to your project folder")

if __name__ == "__main__":
    main()