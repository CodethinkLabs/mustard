% if repository.interfaces():
  <h1>Interfaces <span>{{len(repository.interfaces())}}</span></h1>
  <dl>
    % for path, interface in repository.interfaces():
      % include interface path=path, interface=interface, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
