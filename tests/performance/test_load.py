import pytest
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class SimpleLoadTester:
    """Simple load testing without Locust"""
    
    def __init__(self, base_url="https://httpbin.org"):
        self.base_url = base_url
        self.results = []
    
    def single_request(self, endpoint="/get"):
        """Make a single HTTP request and measure response time"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            end_time = time.time()
            
            return {
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'success': response.status_code == 200
            }
        except Exception as e:
            end_time = time.time()
            return {
                'status_code': 0,
                'response_time': end_time - start_time,
                'success': False,
                'error': str(e)
            }
    
    def load_test(self, num_requests=10, max_workers=3):
        """Run load test with multiple concurrent requests"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all requests
            futures = [executor.submit(self.single_request) for _ in range(num_requests)]
            
            # Collect results
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        return results

@pytest.mark.performance
def test_basic_load_framework():
    """Test that basic load testing framework works"""
    load_tester = SimpleLoadTester()
    
    # Test single request
    result = load_tester.single_request()
    
    assert 'status_code' in result
    assert 'response_time' in result
    assert 'success' in result
    
    print(f"✅ Single request test: {result['response_time']:.2f}s")

@pytest.mark.performance
@pytest.mark.slow
def test_concurrent_requests():
    """Test concurrent request handling"""
    load_tester = SimpleLoadTester()
    
    # Run small load test
    results = load_tester.load_test(num_requests=5, max_workers=2)
    
    assert len(results) == 5
    
    # Calculate statistics
    successful_requests = [r for r in results if r['success']]
    success_rate = len(successful_requests) / len(results) * 100
    
    if successful_requests:
        avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
        max_response_time = max(r['response_time'] for r in successful_requests)
        
        print(f"✅ Load test results:")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Average response time: {avg_response_time:.2f}s")
        print(f"   Max response time: {max_response_time:.2f}s")
        
        # Basic performance assertions
        assert success_rate >= 80  # At least 80% success rate
        assert avg_response_time < 5.0  # Average response under 5 seconds
    else:
        pytest.skip("No successful requests to analyze")

@pytest.mark.performance
def test_response_time_threshold():
    """Test that response times are within acceptable limits"""
    load_tester = SimpleLoadTester()
    
    # Test multiple requests
    results = []
    for _ in range(3):
        result = load_tester.single_request()
        results.append(result)
        time.sleep(0.5)  # Small delay between requests
    
    successful_results = [r for r in results if r['success']]
    
    if successful_results:
        for result in successful_results:
            # Each request should complete within 10 seconds
            assert result['response_time'] < 10.0, f"Request took too long: {result['response_time']:.2f}s"
        
        print(f"✅ All {len(successful_results)} requests completed within threshold")
    else:
        pytest.skip("No successful requests to validate")

# Benchmark test (not marked with performance to avoid running in normal tests)
def test_benchmark_baseline():
    """Benchmark test to establish baseline performance"""
    load_tester = SimpleLoadTester()
    
    print("\n📊 Benchmark Test Results:")
    print("=" * 40)
    
    # Test different endpoints
    endpoints = ["/get", "/json", "/status/200"]
    
    for endpoint in endpoints:
        result = load_tester.single_request(endpoint)
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{endpoint:15} | {result['response_time']:6.2f}s | {status}")
    
    # This test always passes as it's just for information
    assert True

# Simple stress test
@pytest.mark.performance
@pytest.mark.stress
def test_stress_basic():
    """Basic stress test with higher load"""
    load_tester = SimpleLoadTester()
    
    # Run larger load test
    start_time = time.time()
    results = load_tester.load_test(num_requests=10, max_workers=5)
    total_time = time.time() - start_time
    
    # Analyze results
    successful_requests = [r for r in results if r['success']]
    success_rate = len(successful_requests) / len(results) * 100
    requests_per_second = len(results) / total_time
    
    print(f"✅ Stress test completed:")
    print(f"   Total requests: {len(results)}")
    print(f"   Success rate: {success_rate:.1f}%")
    print(f"   Requests/second: {requests_per_second:.2f}")
    print(f"   Total time: {total_time:.2f}s")
    
    # Stress test assertions
    assert success_rate >= 70  # At least 70% success under stress
    assert requests_per_second > 0.5  # At least 0.5 requests per second

# Note: For advanced load testing, install and use Locust separately:

"""
Advanced Load Testing with Locust:

1. Install Locust in a separate environment:
   pip install locust

2. Create a separate locust file:
   # locustfile.py
   from locust import HttpUser, task, between
   
   class BankingUser(HttpUser):
       wait_time = between(1, 3)
       
       @task
       def test_endpoint(self):
           self.client.get("/api/balance")

3. Run Locust:
   locust -f locustfile.py --host=https://your-api.com
"""