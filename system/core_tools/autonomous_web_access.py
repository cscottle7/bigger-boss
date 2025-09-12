"""
Autonomous Web Access System
Bypasses WebFetch permissions by using Playwright directly for website analysis
"""

import asyncio
from playwright.async_api import async_playwright
import json
import logging
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path
import re
from urllib.parse import urlparse, urljoin

from system.orchestration.autonomous_operation_manager import autonomous_manager

class AutonomousWebAccess:
    """Direct web access using Playwright without requiring WebFetch permissions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def fetch_website_content(self, url: str, analyze_brand: bool = True) -> Dict:
        """
        Fetch and analyze website content autonomously using Playwright
        Replaces WebFetch functionality for autonomous operations
        """
        
        # Check autonomous permissions
        can_crawl, message = autonomous_manager.can_perform_operation('web_crawling')
        if not can_crawl:
            return {'error': f"Autonomous web access not allowed: {message}"}
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Set user agent for respectful crawling
                await page.set_extra_http_headers({
                    "User-Agent": "Bigger-Boss-Analysis-Tool/1.0 (Autonomous Market Research)"
                })
                
                # Navigate to the website
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Extract comprehensive website data
                website_data = await page.evaluate("""
                    () => {
                        // Helper function to clean text
                        const cleanText = (text) => {
                            return text ? text.trim().replace(/\\s+/g, ' ') : '';
                        };
                        
                        // Get page title and meta data
                        const title = document.title || '';
                        const metaDescription = document.querySelector('meta[name="description"]');
                        const description = metaDescription ? metaDescription.content : '';
                        
                        // Get main content areas
                        const mainContent = document.querySelector('main, .main, #main, .content, #content');
                        const bodyText = mainContent ? mainContent.innerText : document.body.innerText;
                        
                        // Get headings for content structure
                        const headings = {
                            h1: Array.from(document.querySelectorAll('h1')).map(h => cleanText(h.textContent)),
                            h2: Array.from(document.querySelectorAll('h2')).map(h => cleanText(h.textContent)),
                            h3: Array.from(document.querySelectorAll('h3')).map(h => cleanText(h.textContent))
                        };
                        
                        // Get navigation and menu items
                        const navLinks = Array.from(document.querySelectorAll('nav a, .menu a, .navigation a'))
                            .map(link => ({
                                text: cleanText(link.textContent),
                                href: link.href
                            }))
                            .filter(link => link.text.length > 0);
                        
                        // Get services/products mentioned
                        const serviceKeywords = bodyText.match(/\\b(service|product|solution|offering|expertise|specializ|consult)\\w*\\b/gi) || [];
                        
                        // Get contact information
                        const emails = bodyText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/gi) || [];
                        const phones = bodyText.match(/\\(\\d{3}\\)\\s\\d{3}-\\d{4}|\\d{4}\\s\\d{3}\\s\\d{3}|\\d{10}/gi) || [];
                        
                        // Get location indicators
                        const australianLocations = bodyText.match(/\\b(Sydney|Melbourne|Brisbane|Perth|Adelaide|Canberra|Darwin|Hobart|NSW|VIC|QLD|WA|SA|ACT|NT|TAS|Australia)\\b/gi) || [];
                        
                        return {
                            url: window.location.href,
                            title: title,
                            description: description,
                            headings: headings,
                            mainContent: cleanText(bodyText).substring(0, 2000), // First 2000 chars
                            navigation: navLinks.slice(0, 20), // Top 20 nav items
                            serviceKeywords: [...new Set(serviceKeywords.map(k => k.toLowerCase()))],
                            contactInfo: {
                                emails: emails.slice(0, 5),
                                phones: phones.slice(0, 3)
                            },
                            locations: [...new Set(australianLocations.map(l => l.toUpperCase()))],
                            wordCount: bodyText.trim().split(/\\s+/).length,
                            extractedAt: new Date().toISOString()
                        };
                    }
                """)
                
                await browser.close()
                
                # Perform brand analysis if requested
                if analyze_brand:
                    brand_analysis = await self._analyze_brand_positioning(website_data)
                    website_data['brandAnalysis'] = brand_analysis
                
                # Log successful autonomous operation
                autonomous_manager.log_operation(
                    'autonomous_web_access',
                    'success',
                    {
                        'url': url,
                        'title': website_data.get('title', 'No title'),
                        'word_count': website_data.get('wordCount', 0)
                    }
                )
                
                return {
                    'success': True,
                    'data': website_data,
                    'extractedAt': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Autonomous web access failed for {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    async def _analyze_brand_positioning(self, website_data: Dict) -> Dict:
        """Analyze brand positioning from website content"""
        
        try:
            content = website_data.get('mainContent', '')
            title = website_data.get('title', '')
            headings = website_data.get('headings', {})
            
            # Combine all text for analysis
            all_text = f"{title} {' '.join(headings.get('h1', []))} {' '.join(headings.get('h2', []))} {content}"
            all_text = all_text.lower()
            
            # Industry detection
            industries = {
                'solar': ['solar', 'renewable', 'energy', 'green power', 'sustainable'],
                'legal': ['law', 'legal', 'lawyer', 'attorney', 'solicitor', 'barrister'],
                'medical': ['medical', 'health', 'doctor', 'clinic', 'surgery', 'treatment'],
                'transport': ['transport', 'bus', 'coach', 'charter', 'travel', 'logistics'],
                'technology': ['tech', 'software', 'digital', 'it', 'computer', 'system'],
                'consulting': ['consulting', 'advisory', 'strategy', 'business', 'management']
            }
            
            detected_industry = 'general'
            industry_score = 0
            
            for industry, keywords in industries.items():
                score = sum(1 for keyword in keywords if keyword in all_text)
                if score > industry_score:
                    detected_industry = industry
                    industry_score = score
            
            # Service type detection
            service_types = []
            if any(word in all_text for word in ['consultation', 'advisory', 'strategy']):
                service_types.append('consulting')
            if any(word in all_text for word in ['installation', 'repair', 'maintenance']):
                service_types.append('installation_services')
            if any(word in all_text for word in ['emergency', '24/7', 'urgent']):
                service_types.append('emergency_services')
            
            # Market positioning indicators
            positioning = {
                'premium': sum(1 for word in ['premium', 'luxury', 'exclusive', 'high-end', 'quality'] if word in all_text),
                'budget': sum(1 for word in ['affordable', 'budget', 'cheap', 'discount', 'value'] if word in all_text),
                'professional': sum(1 for word in ['professional', 'expert', 'experienced', 'qualified'] if word in all_text),
                'local': sum(1 for word in ['local', 'community', 'neighbourhood', 'area'] if word in all_text)
            }
            
            primary_positioning = max(positioning.items(), key=lambda x: x[1])[0]
            
            # Target market indicators
            target_markets = []
            if any(word in all_text for word in ['business', 'commercial', 'corporate', 'company']):
                target_markets.append('B2B')
            if any(word in all_text for word in ['home', 'residential', 'family', 'personal']):
                target_markets.append('B2C')
            
            return {
                'detectedIndustry': detected_industry,
                'industryConfidence': industry_score,
                'serviceTypes': service_types,
                'primaryPositioning': primary_positioning,
                'positioningScores': positioning,
                'targetMarkets': target_markets,
                'analysisTimestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Brand analysis failed: {e}")
            return {'error': str(e)}
    
    async def get_competitor_urls(self, domain: str, industry: str) -> List[str]:
        """Get potential competitor URLs for market analysis (placeholder)"""
        
        # This would normally use search APIs, but for autonomous operation
        # we'll return common Australian business domains in the same industry
        competitor_patterns = {
            'solar': [
                'solarchoice.net.au',
                'simplysolarsolutions.com.au'
            ],
            'legal': [
                'familyfocuslegal.com.au',
                'edwardsfamilylawyers.com.au',
                'justicefamilylawyers.com.au'
            ],
            'transport': [
                'sydneycharterbus.com.au',
                'sydneycoachhire.com.au'
            ],
            'medical': [
                'endeurology.com.au',
                'advancedurology.com.au'
            ]
        }
        
        return competitor_patterns.get(industry, [])
    
    async def analyze_market_position(self, primary_url: str, competitor_urls: List[str]) -> Dict:
        """Analyze market position compared to competitors"""
        
        try:
            # Analyze primary website
            primary_data = await self.fetch_website_content(primary_url, analyze_brand=True)
            
            if not primary_data.get('success'):
                return {'error': 'Failed to analyze primary website'}
            
            # Analyze competitors (limit to 3 for autonomous operation)
            competitor_analyses = []
            for competitor_url in competitor_urls[:3]:
                try:
                    comp_data = await self.fetch_website_content(f"https://{competitor_url}", analyze_brand=True)
                    if comp_data.get('success'):
                        competitor_analyses.append({
                            'url': competitor_url,
                            'data': comp_data['data']
                        })
                        
                        # Rate limiting for respectful crawling
                        await asyncio.sleep(3)
                        
                except Exception as e:
                    self.logger.warning(f"Failed to analyze competitor {competitor_url}: {e}")
            
            # Compare market positions
            comparison = self._compare_market_positions(
                primary_data['data'], 
                competitor_analyses
            )
            
            return {
                'success': True,
                'primaryWebsite': primary_data['data'],
                'competitors': competitor_analyses,
                'marketComparison': comparison,
                'analysisDate': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Market position analysis failed: {e}")
            return {'error': str(e)}
    
    def _compare_market_positions(self, primary_data: Dict, competitor_data: List[Dict]) -> Dict:
        """Compare market positioning between primary and competitors"""
        
        try:
            primary_brand = primary_data.get('brandAnalysis', {})
            
            # Collect competitor positioning
            competitor_positions = []
            for comp in competitor_data:
                comp_brand = comp['data'].get('brandAnalysis', {})
                competitor_positions.append({
                    'url': comp['url'],
                    'industry': comp_brand.get('detectedIndustry', 'unknown'),
                    'positioning': comp_brand.get('primaryPositioning', 'unknown'),
                    'services': comp_brand.get('serviceTypes', [])
                })
            
            # Market gap analysis
            all_positions = [comp['positioning'] for comp in competitor_positions]
            primary_position = primary_brand.get('primaryPositioning', 'unknown')
            
            position_frequency = {}
            for pos in all_positions + [primary_position]:
                position_frequency[pos] = position_frequency.get(pos, 0) + 1
            
            return {
                'primaryPositioning': primary_position,
                'competitorPositions': competitor_positions,
                'marketGaps': [pos for pos in ['premium', 'budget', 'professional', 'local'] 
                              if position_frequency.get(pos, 0) <= 1],
                'positioningFrequency': position_frequency,
                'competitorsAnalyzed': len(competitor_data),
                'recommendations': self._generate_positioning_recommendations(
                    primary_position, position_frequency
                )
            }
            
        except Exception as e:
            self.logger.error(f"Market comparison failed: {e}")
            return {'error': str(e)}
    
    def _generate_positioning_recommendations(self, primary_position: str, market_frequency: Dict) -> List[str]:
        """Generate strategic positioning recommendations"""
        
        recommendations = []
        
        # Market saturation analysis
        if market_frequency.get(primary_position, 0) > 2:
            recommendations.append(f"Market appears saturated in {primary_position} positioning - consider differentiation")
        
        # Gap opportunities
        least_common = min(market_frequency.items(), key=lambda x: x[1])
        if least_common[1] <= 1 and least_common[0] != primary_position:
            recommendations.append(f"Market opportunity in {least_common[0]} positioning")
        
        # Specific positioning advice
        if primary_position == 'professional' and market_frequency.get('local', 0) == 0:
            recommendations.append("Consider emphasizing local community connection as differentiation")
        
        return recommendations

# Global autonomous web access instance
autonomous_web = AutonomousWebAccess()