% items = tree.find_all(kind='work-item', sort_by='title')
% if items:
  % completed_items = [(x,y) for x,y in items if 'tags/completed' in y.tags]
  <h1>Work Items <span>{{len(completed_items)}} of {{len(items)}} completed ({{int(round(100 * len(completed_items)/float(len(items))))}}%)</span></h1>
  <dl>
    % for path, item in items:
      % include workitem path=path, item=item, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
