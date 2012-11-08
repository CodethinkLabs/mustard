% if repository.integration_strategies():
  % strategies = repository.integration_strategies()
  % with_tests = [(x,y) for x,y in strategies if y.tests]
  <h1>Integration Strategies <span>{{len(with_tests)}} of {{len(strategies)}} with tests</span></h1>
  <dl>
    % for path, strategy in strategies:
      % include integration-strategy path=path, strategy=strategy, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
