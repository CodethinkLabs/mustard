% if detail == 'list':
  % if strategy:
    <a class="strategy" href="/{{strategy.tree.state.identifier}}/integration-strategies#{{path}}">
      {{!'<span class="error">☐</span>' if not strategy.verificationcriteria else '☑'}} {{strategy.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if strategy:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not strategy.verificationcriteria else '☑'}} {{strategy.title}} <span><a href="#{{path}}" onclick="return false">{{path}}</a></span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td class="description">{{!strategy.description}}</td>
        </tr>
        % include tags-list element=strategy
        % include parents-list element=strategy
        % include requirements-list element=strategy
        % include verification-criterion-list element=strategy
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
