import requests
import json
import time
import os

# GTMetrix API Configuration
API_KEY = os.getenv('GTMETRIX_API_KEY')
if not API_KEY:
    raise ValueError("GTMETRIX_API_KEY environment variable is not set")
BASE_URL = 'https://gtmetrix.com/api/2.0'
TARGET_URL = 'https://sydneycoachcharter.com.au/'

def test_gtmetrix_api():
    """Test GTMetrix API connection and start performance test"""
    
    headers = {'Content-Type': 'application/vnd.api+json'}
    data = {
        'data': {
            'type': 'test',
            'attributes': {
                'url': TARGET_URL,
                'location': 7,  # Sydney server
                'browser': 'chrome',
                'generate_video': True,
                'retention': 30
            }
        }
    }
    
    print(f'Starting GTMetrix performance test for: {TARGET_URL}')
    
    try:
        response = requests.post(
            f'{BASE_URL}/tests',
            auth=(API_KEY, ''),
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f'API Response Status: {response.status_code}')
        
        if response.status_code in [200, 202]:
            result = response.json()
            test_id = result.get('data', {}).get('id')
            state = result.get('data', {}).get('attributes', {}).get('state')
            credits = result.get('meta', {}).get('credits_left')
            
            print(f'✓ Test successfully started!')
            print(f'Test ID: {test_id}')
            print(f'Current State: {state}')
            print(f'Credits Remaining: {credits}')
            
            # Save test ID for later retrieval
            with open('gtmetrix_test_id.txt', 'w') as f:
                f.write(test_id)
            
            return test_id
        else:
            print(f'✗ GTMetrix API Error: {response.status_code}')
            print(f'Response: {response.text}')
            return None
            
    except Exception as e:
        print(f'✗ Error: {str(e)}')
        return None

def check_test_status(test_id):
    """Check the status of the GTMetrix test"""
    try:
        response = requests.get(
            f'{BASE_URL}/tests/{test_id}',
            auth=(API_KEY, ''),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            state = result.get('data', {}).get('attributes', {}).get('state')
            print(f'Test Status: {state}')
            return state, result
        else:
            print(f'Error checking status: {response.status_code}')
            return None, None
            
    except Exception as e:
        print(f'Error checking status: {str(e)}')
        return None, None

if __name__ == "__main__":
    # Start the test
    test_id = test_gtmetrix_api()
    
    if test_id:
        print(f'\nTest started with ID: {test_id}')
        print('Waiting 30 seconds before checking status...')
        time.sleep(30)
        
        # Check status
        state, result = check_test_status(test_id)
        
        if state == 'completed':
            print('✓ Test completed! Saving results...')
            with open('gtmetrix_results.json', 'w') as f:
                json.dump(result, f, indent=2)
        else:
            print(f'Test still running. Current state: {state}')
            print('Check status later or wait longer for completion.')