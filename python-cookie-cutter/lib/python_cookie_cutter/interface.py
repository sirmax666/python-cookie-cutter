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
        # project_name = self._question("Project name")
        # project_name_slug = self._slugify(project_name)
        # team_name = self._question("Team name")
        # author_name = self._question("Author name", force_answer=False, default=team_name)
        # max_length = self._question("PEP8 Maximum Line Length", ftype=int)
        # project_description = self._question("Project description")
        # FOR TESTING:
        project_name = 'Mega Big Code'
        project_name_slug = "mega_big_code"
        team_name = "Datahub"
        author_name = "Maxime Sirois"
        max_length = 80
        project_description = "Just a fake project description"

        setattr(self, 'project_name', project_name)
        setattr(self, 'project_name_slug', project_name_slug)
        setattr(self, 'team_name', team_name)
        setattr(self, 'author_name', author_name)
        setattr(self, 'max_length', int(max_length))
        setattr(self, 'project_description', project_description)
        setattr(self, 'location', location)

    def _slugify(self, s):
        return re.sub("[ ]+", "_", s.lower())
