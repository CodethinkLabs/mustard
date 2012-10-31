% if repository.architectures():
  <h1>Architectures <span>{{len(repository.architectures())}}</span></h1>
  <dl>
    % for path, architecture in repository.architectures():
      % include architecture path=path, architecture=architecture, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
