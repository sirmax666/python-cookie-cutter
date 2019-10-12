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
        project_name = self.interface.project_name_slug
        # Create Project Folder
        cursor_path = Path(location, project_name)
        logger.info(f"Creating Folder @ {str(cursor_path)}")
        cursor_path.mkdir()
        # Iterate through params to create the rest
        # - Create project files
        for file_, param in self.parameters['project_folder']['files'].items():
            logging.info(f"> Generating {file_}")
            file_name = str(file_)
            # match = re.search(r"{{([a-z0-9_ ]+)}}", file_)
            # if match:
            #     template_value = match.group(1)
            #     t = Template(file_)
            #     file_name = t.render(**{template_value: getattr(self.interface, template_value)})
            #     logging.info(f">> Replaced name for {file_name}")

            file_template = Path(C._TEMPLATE_FOLDER, param['template'])
            logging.info(f">> Generate based on template @ {str(file_template)}")
            template_content = file_template.read_text()
            # Replace Optional Content by Mapping of template_string key.
            t = Template(template_content)
            content = t.render(**param.get('template_string', {}))
            self._generate_file(content, cursor_path / file_name)
    
    def _read_template(self, path):
        return path.read_text()

    def _generate_file(self, content, location):
        with open(location, 'w+') as f_out:
            f_out.write(content)
