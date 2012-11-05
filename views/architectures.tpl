% if repository.architectures():
  % architectures = repository.architectures()
  % archs_with_comps = [(x,y) for x,y in architectures if y.components]
  <h1>Architectures <span>{{len(archs_with_comps)}} of {{len(architectures)}} with components</span></h1>
  <dl>
    % for path, architecture in repository.architectures():
      % include architecture path=path, architecture=architecture, detail='full'
    % end
  </dl>
% end

% rebase layout repository=repository
