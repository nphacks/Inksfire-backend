import os, requests 

def demographics_tag(tag: str):
    """
    Fetch demographics data for a single tag.
    """
    url = f"{os.getenv('QLOO_LINK')}/v2/insights?filter.type=urn:demographics&signal.interests.tags={tag}"
    headers = {"X-Api-Key": os.getenv('QLOO_API_KEY')}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    if data.get('success') and data.get('results', {}).get('demographics'):
        return data['results']['demographics']
    
    return []
