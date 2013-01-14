% if element.kind == 'integration-strategy':
  <tr>
    <th>Test Strategies</th>
    <td>
      % if element.teststrategies:
        <ul class="list">
          % for path, teststrategy in element.teststrategies.iteritems():
            <li>
              % include test-strategy path=path, teststrategy=teststrategy, detail='list'
            </li>
          % end
        </ul>
      % else:
        <p class="error">No test strategies specified.</p>
      % end
    </td>
  </tr>
% else:
  % if element.teststrategies:
    <tr>
      <th>Test Strategies</th>
      <td>
        <ul class="list">
          % for path, teststrategy in element.teststrategies.iteritems():
            <li>
              % include test-strategy path=path, teststrategy=teststrategy, detail='list'
            </li>
          % end
        </ul>
      </td>
    </tr>
  % end
% end
