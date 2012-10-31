% if element.links:
  <tr>
    <th>Links</th>
    <td>
      <ul>
        % for path, linked in element.links.iteritems():
          <li>
            % include element path=path, element=linked, detail='list'
          </li>
        % end
      </ul>
    </td>
  </tr>
% end
% if element.backlinks:
  <tr>
    <th>Backlinks</th>
    <td>
      <ul>
        % for path, linking in element.backlinks.iteritems():
          <li>
            % include element path=path, element=linking, detail='list'
          </li>
        % end
      </ul>
    </td>
  </tr>
% end
