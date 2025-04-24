import re
import requests
import logging
from typing import Optional

def get_supported_protocol(url: str) -> str:
    """
    Determine the supported protocol (HTTP/HTTPS) for a given URL.
    
    Args:
        url (str): The URL to check
        
    Returns:
        str: 'https', 'http', or 'Unsupported'
    """
    if not re.match(r"^https?://", url):
        url = "http://" + url

    https_url = url.replace("http://", "https://")

    try:
        # Check if the server supports HTTPS
        response = requests.head(https_url)
        if response.status_code < 400:
            return "https"

        # If HTTPS is not supported, check if the server supports HTTP
        response = requests.head(url)
        if response.status_code < 400:
            return "http"

        return "Unsupported"

    except requests.exceptions.RequestException:
        return "http"

def normalize_url(url: str) -> str:
    """
    Normalize a URL by ensuring it has a protocol and removing trailing slashes.
    
    Args:
        url (str): The URL to normalize
        
    Returns:
        str: Normalized URL
    """
    if not url:
        return ""
    
    # Remove trailing slashes
    url = url.rstrip('/')
    
    # Add protocol if missing
    if not re.match(r"^https?://", url):
        url = "http://" + url
        
    return url

def validate_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = requests.head(url, timeout=5)
        return 200 <= result.status_code < 400
    except requests.exceptions.RequestException:
        return False 