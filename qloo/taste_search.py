from api.llm.perplexity.taste_tag_search_parameters import taste_search_parameters
import urllib.parse

def taste_search(payload_context: str):
    """
    Get parameters and create API links for taste search
    """
    parameters = taste_search_parameters(payload_context)
    urls = []
    base_url = "v2/insights?"

    for item in parameters.get("api_data", []):
        filter_type = item.get("filter_type")
        param_data = item.get("parameters", {})

        query_params = {
            "filter.type": filter_type,
        }

        # Optional fields with custom mappings
        if param_data.get("trends"):
            query_params["bias.trends"] = ",".join(param_data["trends"])
        # if param_data.get("explainability") is not None:
        #     query_params["feature.explainability"] = str(param_data["explainability"]).lower()
        if param_data.get("content_rating"):
            query_params["filter.content_rating"] = param_data["content_rating"]
        if param_data.get("external"):
            query_params["filter.external.exists"] = ",".join(param_data["external"])
        if param_data.get("external_imdb"):
            query_params["filter.external.imdb.rating"] = param_data["external_imdb"]
        if param_data.get("external_rotten_tomatoes"):
            query_params["filter.external.rottentomatoes.rating"] = param_data["external_rotten_tomatoes"]
        if param_data.get("finale_year_max"):
            query_params["filter.finale_year.max"] = param_data["finale_year_max"]
        if param_data.get("finale_year_min"):
            query_params["filter.finale_year.min"] = param_data["finale_year_min"]
        if param_data.get("popularity_max"):
            query_params["filter.popularity.max"] = param_data["popularity_max"]
        if param_data.get("popularity_min"):
            query_params["filter.popularity.min"] = param_data["popularity_min"]
        if param_data.get("publication_year_max"):
            query_params["filter.publication_year.max"] = param_data["publication_year_max"]
        if param_data.get("publication_year_min"):
            query_params["filter.publication_year.min"] = param_data["publication_year_min"]
        if param_data.get("rating_max"):
            query_params["filter.rating.max"] = param_data["rating_max"]
        if param_data.get("rating_min"):
            query_params["filter.rating.min"] = param_data["rating_min"]
        if param_data.get("release_date_max"):
            query_params["filter.release_date.max"] = param_data["release_date_max"]
        if param_data.get("release_date_min"):
            query_params["filter.release_date.min"] = param_data["release_date_min"]
        if param_data.get("release_year_max"):
            query_params["filter.release_year.max"] = param_data["release_year_max"]
        if param_data.get("release_year_min"):
            query_params["filter.release_year.min"] = param_data["release_year_min"]
        if param_data.get("offset"):
            query_params["offset"] = param_data["offset"]
        if param_data.get("page"):
            query_params["page"] = param_data["page"]
        if param_data.get("demographics_age"):
            query_params["signal.demographics.age"] = param_data["demographics_age"]
        if param_data.get("location"):
            query_params["signal.location.query"] = param_data["location"]
        if param_data.get("sort_by"):
            query_params["sort_by"] = param_data["sort_by"]
        if param_data.get("take"):
            query_params["take"] = param_data["take"]

        # Encode and build final URL
        encoded = urllib.parse.urlencode(query_params, doseq=True)
        final_url = base_url + encoded
        urls.append(final_url)

    return urls
