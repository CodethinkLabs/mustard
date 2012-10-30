# Copyright (C) 2012 Codethink Limited


import cliapp

import mustard


class ElementFactory(object):
    
    def create(self, data):
        if data['kind'] == 'requirement':
            return mustard.requirement.Requirement(data)
        elif data['kind'] == 'tag':
            return mustard.tag.Tag(data)
        else:
            raise cliapp.AppException('Unknown element: %s' % data)
