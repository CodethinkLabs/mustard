% items = tree.find_all(kind='work-item', sort_by='DEFAULT')
% if items:
  <h1>Work Items</h1>
  <dl>
    % for path, item in items:
      % include workitem path=path, item=item, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
