def get_combined_tag_names(tag_data: dict) -> str:
    tags = tag_data.get("selected_tags", [])
    tag_names = [tag.get("name", "") for tag in tags if "name" in tag]
    return ", ".join(tag_names)


def merge_evaluated_tags(original_tags, evaluation):
    eval_map = {t.tag_name: t.evaluated for t in evaluation.tags}

    selected_tags = original_tags.get("selected_tags", [])

    for tag in selected_tags:
        tag_name = tag.get("name")
        if tag_name in eval_map:
            tag["evaluated"] = eval_map[tag_name]

    return original_tags