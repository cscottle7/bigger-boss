#!/usr/bin/env python3
"""
Real Performance Testing with GTmetrix API
"""
import os
from dotenv import load_dotenv
import requests
import time
import json

load_dotenv()

def test_website_performance(url):
    """Test website performance using GTmetrix API"""
    api_key = os.getenv('GTMETRIX_API_KEY')
    if not api_key:
        return {"error": "No GTmetrix API key found"}
    
    # Start test
    test_url = "https://gtmetrix.com/api/2.0/tests"
    auth = (api_key, '')
    
    data = {
        'url': url,
        'location': 'sydney',
        'browser': 'chrome'
    }
    
    try:
        # Submit test
        response = requests.post(test_url, auth=auth, data=data, timeout=30)
        if response.status_code != 200:
            return {"error": f"Failed to start test: {response.status_code}"}
        
        test_data = response.json()
        test_id = test_data['data']['id']
        
        print(f"Test started with ID: {test_id}")
        print("Waiting for test completion...")
        
        # Wait for completion (simplified - in production would poll properly)
        time.sleep(30)  # GTmetrix tests take time
        
        # Get results
        result_url = f"https://gtmetrix.com/api/2.0/tests/{test_id}"
        result_response = requests.get(result_url, auth=auth)
        
        if result_response.status_code == 200:
            return result_response.json()
        else:
            return {"error": f"Failed to get results: {result_response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = test_website_performance("https://sydneycoachcharter.com.au")
    if "error" not in result:
        print("Performance test successful!")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {result['error']}")
