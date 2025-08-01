from api.firebase.tags import get_tag_by_id, update_tag_demographics
from api.qloo.qloo import qloo_call
from qloo.demographics_search import demographics_search

def projected_demographics(new_selected_tags):
    age_categories = [
        "24_and_younger", "25_to_29", "30_to_34",
        "35_to_44", "45_to_54", "55_and_older"
    ]
    gender_categories = ["female", "male"]

    age_totals = {cat: 0 for cat in age_categories}
    age_counts = {cat: 0 for cat in age_categories}
    gender_totals = {cat: 0 for cat in gender_categories}
    gender_counts = {cat: 0 for cat in gender_categories}

    for tag in new_selected_tags:
        if tag.get("evaluated"):
            tag_id = tag.get("tag_id")
            try:
                # Try to get tag data from DB
                tag_data = get_tag_by_id(tag_id)
                if not tag_data:
                    print(f"Tag {tag_id} not found in DB.")
                    continue

                demographics = tag_data.get("demographics")

                # If demographics not in DB, fetch from external
                if not demographics:
                    url = demographics_search(tag_id)
                    response = qloo_call(url)

                    demographics_raw = response.get("results", {}).get("demographics", [])
                    if not demographics_raw:
                        print(f"No demographics found for tag_id {tag_id}")
                        continue

                    demographics = demographics_raw[0].get("query", {})
                    update_tag_demographics(tag_id, demographics)  # Save to DB

                age = demographics.get("age", {})
                gender = demographics.get("gender", {})

                for cat in age_categories:
                    if cat in age:
                        age_totals[cat] += age[cat]
                        age_counts[cat] += 1

                for cat in gender_categories:
                    if cat in gender:
                        gender_totals[cat] += gender[cat]
                        gender_counts[cat] += 1

            except Exception as e:
                print(f"Error processing tag_id={tag_id}: {e}")
                continue

    age_avg = {
        cat: (age_totals[cat] / age_counts[cat]) if age_counts[cat] > 0 else 0.0
        for cat in age_categories
    }
    gender_avg = {
        cat: (gender_totals[cat] / gender_counts[cat]) if gender_counts[cat] > 0 else 0.0
        for cat in gender_categories
    }

    print(age_avg, gender_avg)

    return {
        "age": age_avg,
        "gender": gender_avg
    }