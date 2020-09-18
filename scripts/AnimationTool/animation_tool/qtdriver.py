import os


def get_view_path(view_name):
    ui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../designer/" + view_name + ".ui")
    return ui_path


def get_resource(resource_name):
    resource_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/" + resource_name)
    return resource_path
