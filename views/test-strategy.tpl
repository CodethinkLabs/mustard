% if detail == 'list':
  % if teststrategy:
    <a class="teststrategy" href="/{{teststrategy.tree.state.identifier}}/test-strategies#{{path}}">{{teststrategy.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if teststrategy:
    <dt><h2 id="{{path}}">{{teststrategy.title}} <span><a href="#{{path}}" onclick="return false">{{path}}</a></span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if teststrategy.description:
          <tr>
            <th>Description</th>
            <td>{{!teststrategy.description}}</td>
          </tr>
        % end
        % include tags-list element=teststrategy
        % include parents-list element=teststrategy
        % include requirements-list element=teststrategy
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
