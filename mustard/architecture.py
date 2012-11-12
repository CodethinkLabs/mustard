# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Architecture(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.components = {}
        self.integration_strategy = (None, None)
        self.toplevel = data.get('toplevel', False)

        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None
