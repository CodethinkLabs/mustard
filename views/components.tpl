% components = tree.find_all(kind='component', sort_by='DEFAULT', top_level=True)
% if components:
  % with_comps_or_items = [y for x,y in components if y.work_items or y.components]
  <h1>Architecture <span>{{len(with_comps_or_items)}} of {{len(components)}} with subcomponents or work items</span></h1>
  <dl>
    % for path, component in components:
      % include component path=path, component=component, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
