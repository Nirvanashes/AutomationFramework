def generate_project_tree(projects, parent_id=None):
    """
    :param projects:
    :param parent_id:
    :return:
    """
    tree = []
    for project in projects:
        if project.parent_project_id == parent_id:
            formatted_project = {
                "project_name": project.project_name,
                "parent_project_id": project.parent_project_id,
                "id": project.id,
                "is_deleted": project.is_deleted,
                "update_user": project.update_user,
                "create_time": project.create_time,
                "update_time": project.update_time,
                "children": generate_project_tree(projects, project.id)
            }
            tree.append(formatted_project)
    return tree
