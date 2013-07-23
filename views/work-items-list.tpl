% if element.kind == 'component':
  <tr>
    <th>Work Items</th>
    <td>
      % if element.work_items:
        <ul class="list">
          % for path, item in element.work_items.iteritems():
            <li>
              % include workitem path=path, item=item, detail='list'
            </li>
          % end
        </ul>
      % else:
        % if element.components:
          <p class="warning">No work items specified.</p>
        % else:
          <p class="error">This element needs components or work items.</p>
        % end
      % end
    </td>
  </tr>
% else:
  % if element.work_items:
    <tr>
      <th>Work Items</th>
      <td>
        <ul class="list">
          % for path, item in element.work_items.iteritems():
            <li>
              % include workitem path=path, item=item, detail='list'
            </li>
          % end
        </ul>
      </td>
    </tr>
  % end
% end
