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
        # self.author_name = self._question("Author name", force_answer=False, default=team_name)
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

    def _slugify(self, s, delimiter="_"):
        return re.sub("[ ]+", delimiter, s.lower())
