def filter_tag_types(tags: list[dict]) -> list[dict]:
    """
    Remove tags with unwanted types and return top 100.

    Args:
        tags (list[dict]): List of tag dictionaries.

    Returns:
        list[dict]: Filtered list of up to 100 tags.
    """
    filtered = [
        tag for tag in tags
        if tag.get("type") not in [
            "urn:tag:wikipedia_category:wikidata",
            "urn:tag:streaming_service:media"
        ]
    ]
    return filtered[:100]
