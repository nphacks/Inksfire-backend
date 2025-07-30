from models.tags import TagsSearchQuery

def suggest_tags_payload(request: TagsSearchQuery): 
    payload_search_string = ''
    payload_context = ''
    if request.searchString != '':
        payload_search_string = payload_search_string + f"The user search direction is: {request.searchString} "
    else:
        payload_search_string = payload_search_string + f"The user has given no search directions, so determine based on story context."

    payload_context = "\n The context for search:"
    
    if request.idea != '':
        payload_context = payload_context + f"The idea of the story is: {request.idea} "
    
    if request.genres != '':
        payload_context = payload_context + f"The genre/s of the story is/are: {request.genres} "

    if request.story_types != '':
        payload_context = payload_context + f"The type of the story is/are: {request.story_types} "

    if request.target_age != '':
        payload_context = payload_context + f"The age of target audience of the story is: {request.target_age} "

    if request.target_gender != '':
        payload_context = payload_context + f"The gender demographics for target audience of the story is: {request.target_gender} "
    
    return payload_search_string, payload_context