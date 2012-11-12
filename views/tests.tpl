% tests = tree.find_all(kind='test', sort_by='title')
% if tests:
  <h1>Tests</h1>
  <dl>
    % for path, test in tests:
      % include test path=path, test=test, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
