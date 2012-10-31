% if repository.components():
  <h1>Components <span>{{len(repository.components())}}</span></h1>
  <dl>
    % for path, component in repository.components():
      % include component path=path, component=component, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
