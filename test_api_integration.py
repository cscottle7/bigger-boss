#!/usr/bin/env python3
"""
Test script to verify API integration works with real keys
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_serpapi():
    """Test SERPAPI integration"""
    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key:
        return {"error": "SERPAPI_API_KEY not found in environment"}
    
    try:
        response = requests.get('https://serpapi.com/search', {
            'engine': 'google',
            'q': 'SEO tools',
            'api_key': api_key,
            'num': 5
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "SUCCESS",
                "results_count": len(data.get('organic_results', [])),
                "sample_result": data.get('organic_results', [{}])[0].get('title', 'No title') if data.get('organic_results') else 'No results'
            }
        else:
            return {"error": f"SERPAPI returned status {response.status_code}"}
    except Exception as e:
        return {"error": f"SERPAPI test failed: {str(e)}"}

def test_gtmetrix():
    """Test GTMetrix API integration"""
    api_key = os.getenv('GTMETRIX_API_KEY')
    if not api_key:
        return {"error": "GTMETRIX_API_KEY not found in environment"}
    
    try:
        # GTMetrix API v2.0 test
        headers = {'Content-Type': 'application/vnd.api+json'}
        data = {
            'data': {
                'type': 'test',
                'attributes': {
                    'url': 'https://google.com'
                }
            }
        }
        response = requests.post('https://gtmetrix.com/api/2.0/tests', 
            auth=(api_key, ''),
            headers=headers,
            json=data,
            timeout=30,
            verify=False  # Skip SSL verification for testing
        )
        
        if response.status_code in [200, 202]:  # 202 = Accepted/Queued
            data = response.json()
            return {
                "status": "SUCCESS", 
                "test_id": data.get('data', {}).get('id', 'Unknown'),
                "test_state": data.get('data', {}).get('attributes', {}).get('state', 'Unknown'),
                "credits_left": data.get('meta', {}).get('credits_left', 'Unknown')
            }
        else:
            return {"error": f"GTMetrix returned status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": f"GTMetrix test failed: {str(e)}"}

def test_jina():
    """Test Jina AI integration"""
    api_key = os.getenv('JINA_API_KEY')
    if not api_key:
        return {"error": "JINA_API_KEY not found in environment"}
    
    try:
        # Test Jina Reader API
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get('https://r.jina.ai/https://example.com', 
            headers=headers, timeout=10)
        
        if response.status_code == 200:
            content = response.text[:100]  # First 100 chars
            return {
                "status": "SUCCESS",
                "content_preview": content,
                "content_length": len(response.text)
            }
        else:
            return {"error": f"Jina returned status {response.status_code}"}
    except Exception as e:
        return {"error": f"Jina test failed: {str(e)}"}

def main():
    """Run all API tests"""
    print("Testing API Integration...")
    print("=" * 50)
    
    # Test SERPAPI
    print("Testing SERPAPI...")
    serpapi_result = test_serpapi()
    print(f"Result: {json.dumps(serpapi_result, indent=2)}")
    print()
    
    # Test GTMetrix
    print("Testing GTMetrix...")
    gtmetrix_result = test_gtmetrix()
    print(f"Result: {json.dumps(gtmetrix_result, indent=2)}")
    print()
    
    # Test Jina
    print("Testing Jina AI...")
    jina_result = test_jina()
    print(f"Result: {json.dumps(jina_result, indent=2)}")
    print()
    
    # Summary
    print("=" * 50)
    print("SUMMARY:")
    apis = {
        "SERPAPI": "SUCCESS" if "SUCCESS" in str(serpapi_result) else "FAILED",
        "GTMetrix": "SUCCESS" if "SUCCESS" in str(gtmetrix_result) else "FAILED", 
        "Jina AI": "SUCCESS" if "SUCCESS" in str(jina_result) else "FAILED"
    }
    
    for api, status in apis.items():
        print(f"[{status}] {api}")
    
    working_count = sum(1 for status in apis.values() if status == "SUCCESS")
    print(f"\n{working_count}/3 APIs working correctly")
    
    if working_count == 3:
        print("All APIs ready - agents can now use real data!")
    else:
        print("Some APIs need attention before full deployment")

if __name__ == "__main__":
    main()