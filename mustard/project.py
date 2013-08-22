# Copyright (C) 2012 Codethink Limited


import mustard


valid_sort_by = set(["title", "location", "name"])


class Project(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)
        self.kind = 'project'
        self.copyright = data.get('copyright', None)
        self.predefined_filters = data.get('predefined-filters', [])
        self.sort_by = data.get('sort-by', 'location')
        if self.sort_by not in valid_sort_by:
            raise mustard.MustardError(
                "Unknown sort-by (%s) in project node. "
                "Possible sort-by options are: %s" % (
                    self.sort_by, ", ".join(valid_sort_by)))
