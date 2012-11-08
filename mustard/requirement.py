# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Requirement(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.mapped_to = {}
        self.subrequirements = {}
        self.tests = {}
