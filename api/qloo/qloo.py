import os, requests 

def qloo_call(url: str):
    url = f"{os.getenv('QLOO_LINK')}/{url}"
    print(url)
    headers = {"X-Api-Key": os.getenv('QLOO_API_KEY')}
    response = requests.get(url, headers=headers)
    return response.json()