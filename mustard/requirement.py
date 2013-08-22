# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Requirement(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.mapped_to = {}
        self.subrequirements = {}
        self.verificationcriteria = {}

    def sort_subrequirements(self, **kwargs):
        return mustard.sorting.sort_elements(
            self.subrequirements.items(), kwargs)
