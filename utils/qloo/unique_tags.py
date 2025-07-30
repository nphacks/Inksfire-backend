def unique_tags(tags_external_search, tags_db_search):
    all_tags = tags_external_search + tags_db_search
    unique_tags = {tag['name']: tag for tag in all_tags}.values()
    return list(unique_tags)
    