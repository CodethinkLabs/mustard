% if repository.tags():
  <h1>Tags <span>{{len(repository.tags())}}</span></h1>
  <dl>
    % for path, tag in repository.tags():
      % include tag path=path, tag=tag, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
