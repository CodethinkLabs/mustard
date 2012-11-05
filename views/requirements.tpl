% if repository.requirements():
  % mapped_requirements = [y for x,y in repository.requirements() if y.mapped_to]
  <h1>Requirements <span>{{len(mapped_requirements)}} of {{len(repository.requirements())}} mapped</span></h1>
  <dl>
    % for path, requirement in repository.requirements():
      % include requirement path=path, requirement=requirement, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
