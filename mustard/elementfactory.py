# Copyright (C) 2012 Codethink Limited


import cliapp
import markdown
import urllib
import base64

import mustard


class Element(mustard.elementtrie.Trie):

    def __init__(self, data):
        mustard.elementtrie.Trie.__init__(self)
        
        self.kind = data.get('kind', None)
        self.title = data.get('title', None)
        self.set_description(data.get('description', None))
        
        self.parent = data.get('parent', None)
        self.work_items = {}

        self.tags = {}
        for tagref in data.get('tags', []):
            self.tags[tagref] = None

    def set_description(self, text):
        self.description = text
        if self.description:
            self.description = self._resolve_uml(self.description) 
            self.description = markdown.markdown(self.description)

    def _resolve_uml(self, text):
        inside_uml = False
        uml_content = []
        resolved_text = []
        for line in text.splitlines():
            if inside_uml:
                if line.strip() == '@enduml':
                    url = self._generate_uml_image(uml_content)
                    resolved_text.append(url)
                    inside_uml = False
                else:
                    uml_content.append(line.strip())
            else:
                if line.strip() == '@startuml':
                    inside_uml = True
                else:
                    resolved_text.append(line)
        return '\n'.join(resolved_text)

    def _generate_uml_image(self, uml):
        url = '/plantuml/%s' % base64.b64encode("\n".join(uml))
        return '![UML diagram](%s)' % url

class ElementFactory(object):

    def create(self, data):
        if data['kind'] == 'requirement':
            return mustard.requirement.Requirement(data)
        elif data['kind'] == 'tag':
            return mustard.tag.Tag(data)
        elif data['kind'] == 'architecture':
            return mustard.architecture.Architecture(data)
        elif data['kind'] == 'component':
            return mustard.component.Component(data)
        elif data['kind'] == 'work-item':
            return mustard.workitem.WorkItem(data)
        elif data['kind'] == 'interface':
            return mustard.interface.Interface(data)
        else:
            raise cliapp.AppException('Unknown element: %s' % data)
