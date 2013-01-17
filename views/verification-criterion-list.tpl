% if element.kind == 'integration-strategy':
  <tr>
    <th>Verification Criteria</th>
    <td>
      % if element.verificationcriteria:
        <ul class="list">
          % for path, criterion in element.verificationcriteria.iteritems():
            <li>
              % include verification-criterion path=path, criterion=criterion, detail='list'
            </li>
          % end
        </ul>
      % else:
        <p class="error">No verification criteria specified.</p>
      % end
    </td>
  </tr>
% else:
  % if element.verificationcriteria:
    <tr>
      <th>Verification Criteria</th>
      <td>
        <ul class="list">
          % for path, criterion in element.verificationcriteria.iteritems():
            <li>
              % include verification-criterion path=path, criterion=criterion, detail='list'
            </li>
          % end
        </ul>
      </td>
    </tr>
  % end
% end
