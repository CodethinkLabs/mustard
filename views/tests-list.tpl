% if element.kind == 'integration-strategy':
  <tr>
    <th>Tests</th>
    <td>
      % if element.tests:
        <ul class="list">
          % for path, test in element.tests.iteritems():
            <li>
              % include test path=path, test=test, detail='list'
            </li>
          % end
        </ul>
      % else:
        <p class="error">No tests specified.</p>
      % end
    </td>
  </tr>
% else:
  % if element.tests:
    <tr>
      <th>Tests</th>
      <td>
        <ul class="list">
          % for path, test in element.tests.iteritems():
            <li>
              % include test path=path, test=test, detail='list'
            </li>
          % end
        </ul>
      </td>
    </tr>
  % end
% end
