% if repository.tests():
  % tests = repository.tests()
  <h1>Tests</h1>
  <dl>
    % for path, test in tests:
      % include test path=path, test=test, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
