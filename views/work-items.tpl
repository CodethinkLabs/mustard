% if repository.work_items():
  <h1>Work Items <span>{{len(repository.work_items())}}</span></h1>
  <dl>
    % for path, item in repository.work_items():
      % include workitem path=path, item=item, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
