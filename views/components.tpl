% components = tree.find_all(kind='component', sort_by='title')
% if components:
  % with_arch_or_items = [y for x,y in components if y.work_items or y.architecture]
  <h1>Components <span>{{len(with_arch_or_items)}} of {{len(components)}} with architectures or work items</span></h1>
  <dl>
    % for path, component in components:
      % include component path=path, component=component, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
