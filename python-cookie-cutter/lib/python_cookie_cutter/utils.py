# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------
# Team: Datahub
# -----------------------------------------------------------------------------
# Author: Maxime Sirois
# -----------------------------------------------------------------------------
"""Utility Module

Regroups miscellaneous functions

"""
# -----------------------------------------------------------------------------


from datetime import datetime
from jinja2 import Template
import json


def read_json(path):
    with open(path, 'r') as f_in:
        data = json.load(f_in)
    return data


def read_param(path, interface):
    """Read project structure json file

    Read the file and replace the template values inside {{value}}

    Args:
        path (str): Absolute path to the parameter json file.
        interface (object): Interface object containing attributes which are
                            used to replace the template values.
    
    Returns:
        dict: A dictionnary with values replaced.

    Todo:
        * Find a way to make this more dynamical
    """
    with open(path, 'r') as f_in:
        content = f_in.read()
    t = Template(content)
    rendered = t.render(project_name=interface.project_name,
                        project_name_slug=interface.project_name_slug,
                        team_name=interface.team_name,
                        author_name=interface.author_name,
                        max_length=interface.max_length,
                        project_description=interface.project_description)
    return json.loads(rendered)


def now(fmt='%Y-%m-%d %H:%M:%S'):
    """Function that gives the current timestamp

    Current timestamp given by the operating system.

    Args:
        fmt (str): The timestamp format you which to output the timestamp.

    Returns:
        str: The current timestamp
    """
    return datetime.now().strftime(fmt)
