#!/usr/bin/python3
"""
Script to print hot posts on a given Reddit subreddit.
"""

import requests


def top_ten(subreddit):
    """Print the titles of the 10 hottest posts on a given subreddit."""
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    
    params = {
        "limit": 10
    }
    
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    # Handle invalid subreddits by checking for non-200 status codes
    if response.status_code != 200:
        print("None")
        return
    
    data = response.json().get("data", {})
    children = data.get("children", [])

    # If there are no posts, print "None"
    if not children:
        print("None")
        return

    # Print titles of the first 10 hot posts
    for post in children:
        print(post.get("data", {}).get("title", "None"))
