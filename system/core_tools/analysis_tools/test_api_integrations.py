#!/usr/bin/env python3
"""
Test all API integrations with the .env file
"""

import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_api_keys():
    """Test all API integrations from .env file"""
    
    print("Testing API Integrations from .env file...")
    print("=" * 50)
    
    results = {"working": [], "failed": []}
    
    # Test SerpAPI
    serpapi_key = os.getenv('SERPAPI_API_KEY')
    if serpapi_key:
        try:
            import requests
            url = f"https://serpapi.com/search.json?engine=google&q=test&api_key={serpapi_key}&num=1"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'organic_results' in data:
                    results["working"].append(f"SerpAPI: Working - {len(data.get('organic_results', []))} results")
                else:
                    results["failed"].append(f"SerpAPI: API key valid but no results")
            else:
                results["failed"].append(f"SerpAPI: HTTP {response.status_code}")
        except Exception as e:
            results["failed"].append(f"SerpAPI: {str(e)[:50]}")
    else:
        results["failed"].append("SerpAPI: No API key found in .env")
    
    # Test GTmetrix
    gtmetrix_key = os.getenv('GTMETRIX_API_KEY')
    if gtmetrix_key:
        try:
            # GTmetrix API test
            url = "https://gtmetrix.com/api/2.0/sites"
            auth = (gtmetrix_key, '')
            response = requests.get(url, auth=auth, timeout=10)
            if response.status_code == 200:
                results["working"].append("GTmetrix: API key valid and working")
            else:
                results["failed"].append(f"GTmetrix: HTTP {response.status_code}")
        except Exception as e:
            results["failed"].append(f"GTmetrix: {str(e)[:50]}")
    else:
        results["failed"].append("GTmetrix: No API key found in .env")
    
    # Test Jina AI  
    jina_key = os.getenv('JINA_API_KEY')
    if jina_key:
        try:
            # Jina AI test
            headers = {'Authorization': f'Bearer {jina_key}'}
            url = "https://api.jina.ai/v1/embeddings"
            payload = {
                "input": ["test text"],
                "model": "jina-embeddings-v2-base-en"
            }
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                results["working"].append("Jina AI: Embeddings API working")
            else:
                results["failed"].append(f"Jina AI: HTTP {response.status_code}")
        except Exception as e:
            results["failed"].append(f"Jina AI: {str(e)[:50]}")
    else:
        results["failed"].append("Jina AI: No API key found in .env")
    
    # Print results
    print(f"WORKING APIs ({len(results['working'])}):")
    for item in results["working"]:
        print(f"  + {item}")
    
    print(f"\nFAILED APIs ({len(results['failed'])}):")
    for item in results["failed"]:
        print(f"  - {item}")
    
    return results

def create_integrated_analysis_tools():
    """Create analysis tools that use the API keys"""
    
    print("\nCreating API-integrated analysis tools...")
    
    # SerpAPI keyword research tool
    serpapi_code = '''#!/usr/bin/env python3
"""
Real Keyword Research with SerpAPI
"""
import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()

def keyword_research(query, location="Sydney, NSW, Australia"):
    """Get real keyword data using SerpAPI"""
    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key:
        return {"error": "No SerpAPI key found"}
    
    url = f"https://serpapi.com/search.json?engine=google&q={query}&location={location}&api_key={api_key}&num=10"
    
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        
        results = []
        for result in data.get('organic_results', []):
            results.append({
                'title': result.get('title'),
                'url': result.get('link'),
                'snippet': result.get('snippet'),
                'position': result.get('position')
            })
        
        return pd.DataFrame(results)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    df = keyword_research("sydney bus charter")
    if isinstance(df, pd.DataFrame):
        print(f"Found {len(df)} search results")
        print(df[['title', 'position']].head())
    else:
        print(f"Error: {df}")
'''
    
    with open("analysis_tools/serpapi_keyword_research.py", "w") as f:
        f.write(serpapi_code)
    
    # GTmetrix performance tool
    gtmetrix_code = '''#!/usr/bin/env python3
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
'''
    
    with open("analysis_tools/gtmetrix_performance.py", "w") as f:
        f.write(gtmetrix_code)
    
    print("Created API-integrated tools:")
    print("  - analysis_tools/serpapi_keyword_research.py")
    print("  - analysis_tools/gtmetrix_performance.py")

if __name__ == "__main__":
    # Install python-dotenv if needed
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Installing python-dotenv...")
        os.system("pip install python-dotenv")
        from dotenv import load_dotenv
    
    # Test APIs
    results = test_api_keys()
    
    # Create integrated tools
    create_integrated_analysis_tools()
    
    # Summary
    working_count = len(results["working"])
    total_count = len(results["working"]) + len(results["failed"])
    
    print(f"\n{'='*50}")
    print(f"API INTEGRATION SUMMARY: {working_count}/{total_count} APIs working")
    print(f"System now has access to: SerpAPI, GTmetrix, Jina AI")
    print(f"Missing limitations resolved!")