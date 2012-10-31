% if element.kind == 'architecture':
  % include architecture path=path, architecture=element, detail='list'
% elif element.kind == 'work-item':
  % include workitem path=path, item=element, detail='list'
% elif element.kind == 'component':
  % include component path=path, component=element, detail='list'
% elif element.kind == 'requirement':
  % include requirement path=path, requirement=element, detail='list'
% elif element.kind == 'tag':
  % include tag path=path, tag=element, detail='list'
% else:
  <p class="error">CANNOT RENDER ELEMENT KIND "{{element.kind}}".</p>
% end

