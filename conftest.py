import pytest
import yaml
import os

@pytest.fixture(scope="session")
def config():
    # Load test configuration
    config_file = os.path.join(os.path.dirname(__file__), 'config', 'test_config.yaml')
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="function")
def test_data():
    #Provide test data for tests
    return {
        "valid_account": "1234567890",
        "invalid_account": "0000000000",
        "test_amount": 100.00
    }

def pytest_configure(config):
    # Configure pytest
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)

def pytest_runtest_makereport(item, call):
    # Take screenshot on test failure
    if call.when == "call" and call.excinfo is not None:
        # Take screenshot if test fails and it's a UI test
        if hasattr(item.instance, 'driver'):
            screenshot_name = f"reports/screenshots/{item.name}.png"
            item.instance.driver.save_screenshot(screenshot_name)
            print(f"Screenshot saved: {screenshot_name}")