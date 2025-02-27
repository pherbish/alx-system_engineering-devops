#!/usr/bin/python3
"""
Script to query a list of all hot posts on a given Reddit subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after="", count=0):
    """
    Recursively retrieves a list of titles of all hot posts
    on a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list, optional): List to store the post titles.
                                    Default is None (initialized inside).
        after (str, optional): Token used for pagination.
                                Default is an empty string.
        count (int, optional): Current count of retrieved posts. Default is 0.

    Returns:
        list: A list of post titles from the hot section of the subreddit.
        Returns None if subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {"User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"}
    params = {"after": after, "count": count, "limit": 100}

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    # Handle invalid subreddits
    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    after = data.get("after")
    count += data.get("dist", 0)

    # Ensure that "children" exists and has posts
    children = data.get("children", [])
    if not children:
        return None if not hot_list else hot_list

    for post in children:
        hot_list.append(post.get("data", {}).get("title", "None"))

    # Recursively fetch more posts if 'after' is not None
    if after:
        return recurse(subreddit, hot_list, after, count)

    return hot_list
