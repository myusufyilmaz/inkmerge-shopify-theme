#!/usr/bin/env python3
"""
IndexNow URL Submission Tool for InkMerge
Instantly notifies search engines about new/updated content
"""
import requests
import json
from typing import List, Dict

INDEXNOW_KEY = "70adf1601b642d499cc11b8f0f0b8a1"
KEY_LOCATION = f"https://www.inkmerge.com/pages/{INDEXNOW_KEY}"
DOMAIN = "www.inkmerge.com"

def submit_single_url(url: str) -> Dict:
    """
    Submit a single URL to IndexNow
    
    Args:
        url: Full URL to submit (e.g., https://inkmerge.com/products/new-product)
    
    Returns:
        dict with status and message
    """
    api_url = f"https://api.indexnow.org/indexnow?url={url}&key={INDEXNOW_KEY}&keyLocation={KEY_LOCATION}"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            return {
                "success": True,
                "status_code": 200,
                "message": f"✅ URL submitted successfully: {url}"
            }
        elif response.status_code == 202:
            return {
                "success": True,
                "status_code": 202,
                "message": f"⏳ URL received, validation pending: {url}"
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": f"❌ Error {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "message": f"❌ Exception: {str(e)}"
        }

def submit_bulk_urls(urls: List[str]) -> Dict:
    """
    Submit multiple URLs to IndexNow (up to 10,000)
    
    Args:
        urls: List of full URLs
    
    Returns:
        dict with status and message
    """
    api_url = "https://api.indexnow.org/IndexNow"
    
    payload = {
        "host": DOMAIN,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls[:10000]  # Max 10,000 URLs
    }
    
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return {
                "success": True,
                "status_code": 200,
                "message": f"✅ {len(urls)} URLs submitted successfully",
                "count": len(urls)
            }
        elif response.status_code == 202:
            return {
                "success": True,
                "status_code": 202,
                "message": f"⏳ {len(urls)} URLs received, validation pending",
                "count": len(urls)
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": f"❌ Error {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "message": f"❌ Exception: {str(e)}"
        }

if __name__ == "__main__":
    # Example usage
    print("🔥 IndexNow Submission Tool\n")
    
    # Test single URL
    test_url = "https://inkmerge.com/"
    print(f"Testing single URL submission: {test_url}")
    result = submit_single_url(test_url)
    print(result['message'])
    
    # Test bulk submission
    print("\nTesting bulk URL submission...")
    test_urls = [
        "https://inkmerge.com/",
        "https://inkmerge.com/collections/all",
        "https://inkmerge.com/pages/free-dtf-application-guide"
    ]
    result = submit_bulk_urls(test_urls)
    print(result['message'])
