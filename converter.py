import json

skip_checked = True


def pretty_print_md(elem_id, elems_dict: dict, depth=0):
    if elem_id not in elems_dict.keys():
        return

    # noinspection PyUnusedLocal
    prefix = ""
    if depth < 4:
        prefix = "#" * (depth + 1) + " "
    else:
        prefix = "    " * (depth - 4)

    try:
        print(prefix + elems_dict[elem_id]["content"])
    except KeyError:
        pass
    for child_id in elems_dict[elem_id]["childs"]:
        pretty_print_md(child_id, elems_dict, depth=depth + 1)


def pretty_print_mm(elem_id, elems_dict: dict, depth=0):
    if elem_id not in elems_dict.keys():
        return

    prefix = "    " * depth

    try:
        print(prefix + elems_dict[elem_id]["content"])
    except KeyError:
        pass
    for child_id in elems_dict[elem_id]["childs"]:
        pretty_print_mm(child_id, elems_dict, depth=depth + 1)


with open('todoist.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    projects = data["projects"]
    tasks = data["items"]
    all_the_data = {0: {
        "content": "Todoist tasks",
        "childs": [],
        "childs_order": []
    }
    }
    projects_ids = []
    for project in projects:
        all_the_data[project["id"]] = {
            "content": project["name"],
            "childs": [],
            "childs_order": []
        }

        project_parent_id = project["parent_id"]
        if project_parent_id is None:
            project_parent_id = 0

        if project_parent_id not in all_the_data.keys():
            all_the_data[project_parent_id] = {"childs": [], "childs_order": []}
        all_the_data[project_parent_id]["childs"].append(project["id"])
        all_the_data[project_parent_id]["childs_order"].append(project["item_order"])

    for task in tasks:
        if task["checked"] and skip_checked:
            continue

        task_parent_id = task["parent_id"]
        if task_parent_id is None:
            task_parent_id = task["project_id"]

        if task_parent_id not in all_the_data.keys():
            all_the_data[task_parent_id] = {"childs": [], "childs_order": []}
        all_the_data[task_parent_id]["childs"].append(task["id"])
        all_the_data[task_parent_id]["childs_order"].append(task["item_order"])

        task_id = task["id"]
        if task_id not in all_the_data.keys():
            all_the_data[task_id] = {"childs": [], "childs_order": []}
        all_the_data[task_id]["content"] = task["content"]


    for _, i in enumerate(all_the_data.keys()):
        try:
            all_the_data[i]["childs"] = [x for _, x in
                                         sorted(zip(all_the_data[i]["childs_order"], all_the_data[i]["childs"]))]
            all_the_data[i]["childs_order"] = sorted(all_the_data[i]["childs_order"])
        except:
            pass

    pretty_print_mm(0, all_the_data)
