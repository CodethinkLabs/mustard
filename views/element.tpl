% if not element:
  % include pathnotfound path=path, detail='list'
% elif element.kind == 'architecture':
  % include architecture path=path, architecture=element, detail='list'
% elif element.kind == 'work-item':
  % include workitem path=path, item=element, detail='list'
% elif element.kind == 'component':
  % include component path=path, component=element, detail='list'
% elif element.kind == 'requirement':
  % include requirement path=path, requirement=element, detail='list'
% elif element.kind == 'interface':
  % include interface path=path, interface=element, detail='list'
% elif element.kind == 'tag':
  % include tag path=path, tag=element, detail='list'
% elif element.kind == 'test-strategy':
  % include test-strategy path=path, teststrategy=element, detail='list'
% elif element.kind == 'integration-strategy':
  % include integration-strategy path=path, strategy=element, detail='list'
% else:
  <span class="error">[[ Cannot render element: {{element.kind}} ]]</span>
% end

