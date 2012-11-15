% if detail == 'list':
  % if architecture:
    <a class="architecture" href="/{{architecture.tree.state.identifier}}/architectures#{{path}}">
      {{!'<span class="error">☐</span>' if not architecture.components else '☑'}} {{architecture.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if architecture:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not architecture.components else '☑'}} {{architecture.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td class="description">{{!architecture.description}}</td>
        </tr>
        % include tags-list element=architecture
        % if not architecture.toplevel:
          % include parents-list element=architecture
        % end
        <tr>
          <th>Components</th>
          <td>
            % if architecture.components:
              <ul class="list">
                % for path, component in architecture.components.iteritems():
                  <li>
                    % include component path=path, component=component, detail='list'
                  </li>
                % end
              </ul>
            % else:
              <p class="error">No components specified yet.</p>
            % end
          </td>
        </tr>
        <tr>
          <th>Integration</th>
          <td>
            % path, strategy = architecture.integration_strategy
            % if path:
              % include integration-strategy path=path, strategy=strategy, detail='list'
            % else:
              <span class="warning">No integration strategy specified</span>
            % end
          </td>
        </tr>
        % include requirements-list element=architecture
        % include work-items-list element=architecture
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
