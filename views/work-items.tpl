% if repository.work_items():
  % items = repository.work_items()
  % completed_items = [(x,y) for x,y in items if 'tags/completed' in y.tags]
  <h1>Work Items <span>{{len(completed_items)}} of {{len(items)}} completed ({{round(100 * len(completed_items)/float(len(items)), 1)}}%)</span></h1>
  <dl>
    % for path, item in items:
      % include workitem path=path, item=item, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
