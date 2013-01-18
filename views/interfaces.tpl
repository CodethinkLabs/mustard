% interfaces = tree.find_all(kind='interface', sort_by='DEFAULT')
% if interfaces:
  <h1>Interfaces <span>{{len(interfaces)}}</span></h1>
  <dl>
    % for path, interface in interfaces:
      % include interface path=path, interface=interface, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
