#!/usr/bin/env python3
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
