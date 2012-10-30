# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Architecture(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.components = {}
        
        self.satisfies = {}
        for ref in data.get('satisfies', []):
            self.satisfies[ref] = None
