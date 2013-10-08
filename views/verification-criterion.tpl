% if detail == 'list':
  % if criterion:
    <a class="verificationcriterion" href="{{criterion.tree.state.url}}/verification-criteria#{{path}}">{{criterion.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if criterion:
    <dt><h2 id="{{path}}">{{criterion.title}} <span><a href="#{{path}}" onclick="return false">{{path}}</a></span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if criterion.description:
          <tr>
            <th>Description</th>
            <td>{{!criterion.description}}</td>
          </tr>
        % end
        % include parents-list element=criterion
        % include tags-list element=criterion
        % include requirements-list element=criterion
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
