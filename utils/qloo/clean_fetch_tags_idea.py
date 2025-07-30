def clean_fetch_tags_idea(response_data):
    cleaned_results = []
    all_tag_ids = []
    
    for item in response_data.get("results", []):
        tags = [
            {
                "name": tag.get("name"),
                "tag_id": tag.get("tag_id"),
                "type": tag.get("type")
            }
            for tag in item.get("tags", [])
        ]
        
        cleaned_item = {
            "name": item.get("name"),
            "entity_id": item.get("entity_id"),
            "types": item.get("types", []),
            "description": item.get("properties", {}).get("description"),
            "tags": tags
        }
        
        cleaned_results.append(cleaned_item)
        all_tag_ids.extend([tag['tag_id'] for tag in tags if tag.get('tag_id')])
    
    return {
        "results": cleaned_results,
        "tag_ids": list(set(all_tag_ids))  # Remove duplicates
    }