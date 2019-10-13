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
from pathlib import Path
import re
import yaml


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
    p = Path(path)
    content = p.read_text()
    t = Template(content)
    rendered = t.render(**interface.__dict__)

    if p.suffix.lower() == '.json':
        data = json.loads(rendered)
    elif p.suffix.lower() in ['.yml', '.yaml']:
        data = yaml.load(rendered, Loader=yaml.FullLoader)
    else:
        raise ValueError("Wrong Parameter File Format")
    return data


def now(fmt='%Y-%m-%d %H:%M:%S'):
    """Function that gives the current timestamp

    Current timestamp given by the operating system.

    Args:
        fmt (str): The timestamp format you which to output the timestamp.

    Returns:
        str: The current timestamp
    """
    return datetime.now().strftime(fmt)


def slugify(s, delimiter="_"):
    return re.sub("[ ]+", delimiter, s.lower())
