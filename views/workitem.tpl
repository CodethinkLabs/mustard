% if detail == 'list':
  % if item:
    <a class="workitem" href="/{{item.tree.state.identifier}}/work-items#{{path}}">
      {{item.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if item:
    <dt><h2 id="{{path}}">{{item.title}} <span><a href="#{{path}}" onclick="return false">{{path}}</a></span></h2></dt>
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
    % if item.work_items:
      <dl>
        % for p, i in item.sort_work_items(sort_by='DEFAULT'):
          % include workitem path=p, item=i, detail='full'
        % end
      </dl>
    % end
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
