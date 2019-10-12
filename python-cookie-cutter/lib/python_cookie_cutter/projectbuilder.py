# -----------------------------------------------------------------------------
# Builder
# -----------------------------------------------------------------------------
# Team: DataHub
# -----------------------------------------------------------------------------
# Author: Maxime Sirois
# -----------------------------------------------------------------------------
"""Build the project

Takes various actions to build the project from the templates and parameters.

"""
# -----------------------------------------------------------------------------


from jinja2 import Template
import json
import logging
from pathlib import Path
import os
import re

from . import constants as C


logger = logging.getLogger(__name__)


class Builder:
    def __init__(self, interface, parameters):
        self.parameters = parameters
        self.interface = interface

    def start(self):
        self._build_project()
    
    def _build_project(self):
        """
        Build the Project in the target location.
        """
        location = self.interface.location
        for folder, body in self.parameters.items():
            _create_folder_and_files(Path(location), folder, body)


    def _read_template(self, path):
        return path.read_text()


def _generate_file(content, location):
    with open(location, 'w+') as f_out:
        f_out.write(content)


def _create_folder_and_files(location, folder, body):
    location = location / folder
    logging.info(f">> Creating {folder} @ {str(location)}")
    location.mkdir()

    if body.get('files'):
        logging.info("> Generating Files:")
        for file_name, file_param in body['files'].items():
            template_name = file_param['template']
            logging.info(f"   - {file_name} with template {template_name}")
            file_template = Path(C._TEMPLATE_FOLDER, template_name)
            template_content = file_template.read_text()
            t = Template(template_content)
            content = t.render(**file_param.get('template_string', {}))
            _generate_file(content, location / file_name)

    if body.get('folders'):
        for folder, body_ in body['folders'].items():
            _create_folder_and_files(location, folder, body_)












# def _create_folder_and_files(folder, body):
#     logging.info(f">> Creating @ {folder}")
#     if body.get('files'):
#         logging.info("> Generating Files:")
#         for file_name, file_param in body['files'].items():
#             logging.info(f"      - {file_name}")
            
#     if body.get('folders'):
#         for folder, body_ in body['folders'].items():
#             _create_folder_and_files(folder, body_)