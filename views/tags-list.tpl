% if element.tags:
  <tr>
    <th>Tags</th>
    <td>
      <ul class="list">
        % for path, tag in element.tags.iteritems():
          <li>
            % include tag path=path, tag=tag, detail='list'
          </li>
        % end
      </ul>
    </td>
  </tr>
% end
