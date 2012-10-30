# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Component(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.architecture = data.get('architecture', None)
