% requirements = tree.find_all(kind='requirement', sort_by='DEFAULT', top_level=True)
% if requirements:
  % mapped_requirements = []
  % for req in [y for x,y in requirements if y.mapped_to]:
    % if len([x for x in req.mapped_to.itervalues() if x.kind == 'component']) > 0:
      % mapped_requirements.append(req)
    % end
  % end
  <h1>Requirements <span>{{len(mapped_requirements)}} of {{len(requirements)}} mapped to components</span></h1>
  <dl>
    % for path, requirement in requirements:
      % include requirement path=path, requirement=requirement, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
