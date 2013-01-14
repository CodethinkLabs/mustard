# Copyright (C) 2012 Codethink Limited


import cliapp
import collections
import markdown
import urllib
import base64
import zlib

import mustard


class Element(object):

    def __init__(self, data):
        self.kind = data.get('kind', None)
        self.title = data.get('title', None)
        self.set_description(data.get('description', None))
        self.parent = (data.get('parent', None), None)
        self.work_items = {}
        self.children = {}

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
                    uml_content = []
                    inside_uml = True
                else:
                    resolved_text.append(line)
        return '\n'.join(resolved_text)

    def _generate_uml_image(self, uml):
        url = '/plantuml/%s' % base64.urlsafe_b64encode(
                zlib.compress("\n".join(uml)))
        return '[![UML diagram](%s)](%s)' % (url, url)
        
    def get_parents(self):
        parents = []
        if hasattr(self, 'parent'):
            if self.parent[1]:
                parents.append(self.parent)
        if hasattr(self, 'parents'):
            for path, parent in self.parents.iteritems():
                if parent:
                    parents.append((path, parent))
        return parents

    def get_children(self):
        raise NotImplementedError   
    
    def inherited_requirements(self, **kwargs):
        results = set()
        queue = collections.deque()
        queue.extend(self.get_parents())
        while queue:
            path, element = queue.popleft()
            if hasattr(element, 'mapped_here'):
                for ref, req in element.mapped_here.iteritems():
                    results.add((ref, req))
            queue.extend(element.get_parents())
        return mustard.sorting.sort_elements(results, kwargs)

    def mapped_requirements(self, **kwargs):
        results = set()
        for ref, req in self.mapped_here.iteritems():
            results.add((ref, req))
        return mustard.sorting.sort_elements(results, kwargs)
    
    def delegated_requirements(self, **kwargs):
        results = set()
        queue = collections.deque()
        queue.extend(self.get_children())
        while queue:
            path, element = queue.popleft()
            if hasattr(element, 'mapped_here'):
                for ref, req in element.mapped_here.iteritems():
                    results.add((ref, req))
            queue.extend(element.get_children())
        return mustard.sorting.sort_elements(results, kwargs)


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
        elif data['kind'] == 'integration-strategy':
            return mustard.integration.IntegrationStrategy(data)
        elif data['kind'] == 'test-strategy':
            return mustard.test.TestStrategy(data)
        elif data['kind'] == 'project':
            return mustard.project.Project(data)
        else:
            raise cliapp.AppException('Unknown element: %s' % data)
