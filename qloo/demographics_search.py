import urllib.parse

def demographics_search(tag_id: str):
    """
    Create API links
    """
    return f"v2/insights?filter.type=urn:demographics&signal.interests.tags={tag_id}"
