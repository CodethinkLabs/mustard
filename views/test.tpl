% if detail == 'list':
  % if test:
    <a class="test" href="/{{test.tree.state.identifier}}/tests#{{path}}">{{test.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if test:
    <dt><h2 id="{{path}}">{{test.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if test.description:
          <tr>
            <th>Description</th>
            <td>{{!test.description}}</td>
          </tr>
        % end
        % include tags-list element=test
        % include parents-list element=test
        % include requirements-list element=test
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
