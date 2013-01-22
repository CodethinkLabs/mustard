% if element.kind in ['component', 'interface', 'integration-strategy', 'verification-criterion']:
  <tr>
    <th>Parent</th>
    <td>
      <p>
        % path, parent = element.parent
        % if path:
          % include element path=path, element=parent, detail='list'
        % else:
          <span class="error">No parent specified</span>
        % end
      </p>
    </td>
  </tr>
% else:
  % if element.parent[0]:
    <tr>
      <th>Parent</th>
      <td>
        <p>
          % path, parent = element.parent
          % include element path=path, element=parent, detail='list'
        </p>
      </td>
    </tr>
  % end
  % if hasattr(element, 'parents'):
    <tr>
      <th>Parents</th>
      <td>
        % if element.parents:
          <ul class="list">
            % for path, parent in element.parents.iteritems():
              <li>
                % include element path=path, element=parent, detail='list'
              </li>
            % end
          </ul>
        % else:
          <p class="error">No parents specified</p>
        % end
      </td>
    </tr>
  % end
% end
