% if detail == 'list':
  % if interface:
    <a class="interface" href="/{{interface.tree.state.identifier}}/interfaces#{{path}}">{{interface.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if interface:
    <dt><h2 id="{{path}}">{{interface.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td>{{!interface.description}}</td>
        </tr>
        % include tags-list element=interface
        % include parents-list element=interface
        % include requirements-list element=interface
        % include work-items-list element=interface
        % include tests-list element=interface
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
