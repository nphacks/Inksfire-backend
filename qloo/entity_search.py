from api.llm.perplexity.entity_tag_search_parameters import entity_search_parameters
import urllib.parse

def entity_search(payload_context: str):
    """
    Get parameters and create API links
    """
    parameters = entity_search_parameters(payload_context)

    # print("Parsed Parameters:", parameters)

    base_url = "search?"
    urls = []

    for item in parameters.get("api_data", []):
        entity = item.get("entity")
        param_data = item.get("parameters", {})

        # Extract fields from param_data
        types = param_data.get("types", [])
        exists = param_data.get("exists", [])
        popularity = param_data.get("popularity")
        page = param_data.get("page")
        take = param_data.get("take")
        sort_by = param_data.get("sort_by")

        # Create one URL per type
        if not types:
            types = [None]

        for t in types:
            query_params = {
                "query": entity,
                "filter.radius": 10,
                "operator.filter.tags": "union",
                "operator.filter.exclude.tags": "union",
            }

            if t:
                query_params["types"] = t
            if exists:
                query_params["filter.exists"] = ",".join(exists)
            if popularity is not None:
                query_params["filter.popularity"] = popularity
            if page is not None:
                query_params["page"] = page
            if take is not None:
                query_params["take"] = take
            if sort_by:
                query_params["sort_by"] = sort_by

            encoded = urllib.parse.urlencode(query_params, doseq=True)
            final_url = base_url + encoded
            urls.append(final_url)

    # For debugging or later processing
    # for url in urls:
        # print("Generated URL:", url)

    return urls
