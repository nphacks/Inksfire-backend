def search_type_format(story_types):
    formatted_types = [f"urn:entity:{story_type}" for story_type in story_types]
    return ",".join(formatted_types)