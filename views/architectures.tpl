% archs = tree.find_all(kind='architecture', sort_by='title')
% if archs:
  % archs_with_comps = [(x,y) for x,y in archs if y.components]
  <h1>Architectures <span>{{len(archs_with_comps)}} of {{len(archs)}} with components</span></h1>
  <dl>
    % for path, architecture in archs:
      % include architecture path=path, architecture=architecture, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
