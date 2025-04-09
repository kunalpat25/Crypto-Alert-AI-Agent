# profile_change_detector.py
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def load_profile_cache():
    """Load cached profile data from file"""
    cache_file = "profile_cache.json"
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading profile cache: {e}")
    
    return {}

    """Save profile cache to file"""
def save_profile_cache(cache):
    cache_file = "profile_cache.json"
    
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        logger.error(f"Error saving profile cache: {e}")

def detect_profile_changes(username, current_name, current_image_url):
    """
    Detect if a user has changed their profile name or image.
    Returns a dictionary with change information or None if no changes.
    """
    cache = load_profile_cache()
    
    # Initialize if user not in cache
    if username not in cache:
        cache[username] = {
            "name": current_name,
            "image_url": current_image_url,
            "last_updated": datetime.now().isoformat()
        }
        save_profile_cache(cache)
        return None
    
    changes = {}
    user_cache = cache[username]
    
    # Check for name change
    if user_cache["name"] != current_name:
        changes["name_change"] = {
            "old": user_cache["name"],
            "new": current_name
        }
        user_cache["name"] = current_name
    
    # Check for image change (simple URL comparison)
    if user_cache["image_url"] != current_image_url:
        changes["image_change"] = {
            "old": user_cache["image_url"],
            "new": current_image_url
        }
        user_cache["image_url"] = current_image_url
    
    # Update last checked timestamp
    user_cache["last_updated"] = datetime.now().isoformat()
    
    # Save updated cache
    save_profile_cache(cache)
    
    return changes if changes else None
