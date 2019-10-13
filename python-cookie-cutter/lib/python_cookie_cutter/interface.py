# -----------------------------------------------------------------------------
# Interface
# -----------------------------------------------------------------------------
# Team: DataHub
# -----------------------------------------------------------------------------
# Author: Maxime Sirois
# -----------------------------------------------------------------------------
"""Interface with the user

Various questions asked to the user regrouped in this class.

Project Name?
Team Name?
Author Name? (If blank, same as Team Name)
Project Description?

"""
# -----------------------------------------------------------------------------


from pathlib import Path
import re


class Interface:
    def __init__(self):
        pass

    def _question(self, text, default=None, force_answer=True, ftype=None):
        answer = ''
        if force_answer:
            while not answer:
                answer = input(text + ': ')
        else:
            answer = input(text + ': ')
            if not answer and default:
                answer = str(default)
        if ftype:
            ftype(answer)
        return answer

    def init_project(self, location):
        # self.project_name = self._question("Project name")
        # self.project_name_slug = self._slugify(project_name)
        # self.team_name = self._question("Team name")
        # self.author_name = self._question("Author name", force_answer=False,
        #                                   default=self.team_name)
        # self.max_length = int(self._question("PEP8 Maximum Line Length", ftype=int))
        # self.project_description = self._question("Project description")
        # self.virtualenv = self._question("Virtualenv executor Path (leave blank for no)",
        #                                  force_answer=False)
        # FOR TESTING:
        self.project_name = 'Mega Big Code'
        self.project_name_slug = "mega_big_code"
        self.team_name = "Datahub"
        self.author_name = "Maxime Sirois"
        self.max_length = 80
        self.project_description = "Just a fake project description"
        self.location = location
        # self.virtualenv = "C:\\Program Files (x86)\\Python36-32\\Scripts\\virtualenv.exe"
        self.virtualenv = ""

    def init_module(self, location):
        location_ = Path(location)
        if not location_.exists():
            raise IOError(2, 'No such path', location)

        # Derive Project name from location
        project_name_slug = location_.name
        target_path = location_ / project_name_slug / 'lib' / project_name_slug

        if not target_path.exists():
            raise IOError(2, 'No such path, please specify the root project folder', location)

        # Set Attributes
        self.project_name_slug = project_name_slug
        self.project_name = self._deslugify(project_name_slug)
        self.team_name = self._question("Team name")
        self.author_name = self._question("Author name", force_answer=False,
                                          default=self.team_name)
        self.module_name = self._question("Module name")
        self.location = target_path

    def _slugify(self, s, delimiter="_"):
        return re.sub("[ ]+", delimiter, s.lower())

    def _deslugify(self, s, delimiter="_"):
        return re.sub(delimiter, " ", s.title())
