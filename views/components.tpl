% if repository.components():
  % components = repository.components()
  % with_work_items = [y for x,y in components if y.work_items]
  <h1>Components <span>{{len(with_work_items)}} of {{len(components)}} with work items</span></h1>
  <dl>
    % for path, component in repository.components():
      % include component path=path, component=component, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
