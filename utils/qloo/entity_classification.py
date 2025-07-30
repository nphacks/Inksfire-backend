def classifies_entities(tag):
    parts = tag['entity_id'].split(':')
    entity_classification = parts[2:]  # Skip 'urn' and 'tag'
    return entity_classification