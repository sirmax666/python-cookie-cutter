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
import subprocess

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
        if not content.endswith('\n'):
            f_out.write('\n')


def _add_header(content, header_template):
    header_content = header_template.read_text()
    return header_content + '\n\n\n' + content


def _create_file(file_name, parameters, location):
    content = ''
    if parameters.get('template'):
        template_name = parameters['template']
        logging.info(f"   - {file_name} :: template :: {template_name}")
        # Get template
        file_template = Path(C._TEMPLATE_FOLDER, template_name)
        template_content = file_template.read_text()
        # Check if there is a header to paste before content
        if parameters.get('header'):
            header_template = Path(C._TEMPLATE_FOLDER, parameters['header'])
            template_content = _add_header(template_content, header_template)
        # Change values of template
        t = Template(template_content)
        content = t.render(**parameters.get('template_string', {}))
    # Generate the File (with Header if applicable)
    _generate_file(content, location / file_name)


def _create_folder_and_files(location, folder, body):
    location = location / folder
    if folder == 'venv':
        if body.get('exe'):
            logging.info(f">>>> Creating VirtualEnv from {body.get('exe')}")
            cmd = f"\"{body.get('exe')}\" \"{location}\""
            subprocess.check_call(cmd, shell=True)
            logging.info(f">>>> Pip Install Requirements.txt")
            pip_exe = location / 'Scripts' / 'pip.exe'
            requirements = location / '..' / 'requirements.txt'
            cmd_pip = f'"{pip_exe}" install -r "{requirements}"'
            subprocess.check_call(cmd_pip, shell=True)
            return
    else:
        logging.info(f">> Creating {folder} @ {str(location)}")
        location.mkdir()

    if body.get('files'):
        for file_name, file_param in body['files'].items():
            _create_file(file_name, file_param, location)

    if body.get('folders'):
        for folder, body_ in body['folders'].items():
            _create_folder_and_files(location, folder, body_)
