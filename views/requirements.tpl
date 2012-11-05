% if repository.requirements():
  % mapped_requirements = []
  % for req in [y for x,y in repository.requirements() if y.mapped_to]:
    % if len([x for x in req.mapped_to.itervalues() if x.kind == 'component']) > 0:
      % mapped_requirements.append(req)
    % end
  % end
  <h1>Requirements <span>{{len(mapped_requirements)}} of {{len(repository.requirements())}} mapped to components</span></h1>
  <dl>
    % for path, requirement in repository.requirements():
      % include requirement path=path, requirement=requirement, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
