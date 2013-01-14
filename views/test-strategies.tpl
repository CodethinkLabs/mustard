% teststrategies = tree.find_all(kind='test-strategy', sort_by='title')
% if teststrategies:
  <h1>Test Strategies</h1>
  <dl>
    % for path, teststrategy in teststrategies:
      % include test-strategy path=path, teststrategy=teststrategy, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
