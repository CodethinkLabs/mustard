# Copyright (C) 2012 Codethink Limited


import cliapp

import mustard


class Project(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)
        self.kind = 'project'
        self.copyright = data.get('copyright', None)
        self.predefined_filters = data.get('predefined-filters', [])
