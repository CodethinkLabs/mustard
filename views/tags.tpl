% tags = tree.find_all(kind='tag', sort_by='DEFAULT')
% if tags:
  <h1>Tags <span>{{len(tags)}}</span></h1>
  <dl>
    % for path, tag in tags:
      % include tag path=path, tag=tag, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
