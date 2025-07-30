def fetch_tags_from_entity(data):
    entities_used = []
    tags = []
    for entity in data:
        entities_used.append(entity["name"])
        tags.extend(entity.get("tags", []))

    return entities_used, tags

def fetch_tags_from_tags(data):
    tags = []
    for entity in data:
        tags.extend(entity.get("tags", []))

    return tags