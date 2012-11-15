% if detail == 'list':
  % if item:
    <a class="workitem" href="/{{item.tree.state.identifier}}/work-items#{{path}}">
      {{!'<span class="error">☐</span>' if not 'tags/completed' in item.tags else '☑'}} {{item.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if item:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not 'tags/completed' in item.tags else '☑'}} {{item.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if item.description:
          <tr>
            <th>Description</th>
            <td class="description">{{!item.description}}</td>
          </tr>
        % end
        % include tags-list element=item
        % include parents-list element=item
        % include requirements-list element=item
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
