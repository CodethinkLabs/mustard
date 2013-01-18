% strategies = tree.find_all(kind='integration-strategy', sort_by='DEFAULT')
% if strategies:
  % with_criteria = [(x,y) for x,y in strategies if y.verificationcriteria]
  <h1>Integration Strategies <span>{{len(with_criteria)}} of {{len(strategies)}} with verification criteria</span></h1>
  <dl>
    % for path, strategy in strategies:
      % include integration-strategy path=path, strategy=strategy, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
