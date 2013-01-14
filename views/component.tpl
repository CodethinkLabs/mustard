% if detail == 'list':
  % if component:
    <a class="component" href="/{{component.tree.state.identifier}}/components#{{path}}">
      {{!'<span class="error">☐</span>' if not component.work_items and not component.architecture else '☑'}} {{component.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if component:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not component.work_items and not component.architecture else '☑'}} {{component.title}} <span><a href="#{{path}}" onclick="return false">{{path}}</a></span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td class="description">{{!component.description}}</td>
        </tr>
        % include tags-list element=component
        % include parents-list element=component
        % if component.architecture:
          <tr> 
            % path, architecture = component.architecture
            <th>Architecture</th>
            <td>
              <p>
                % include architecture path=path, architecture=architecture, detail='list'
              </p>
            </td>
          </tr>
        % end
        % if component.interfaces:
          <tr> 
            <th>Interfaces</th>
            <td>
              <ul class="list">
                % for path, interface in component.interfaces.iteritems():
                  <li>
                    % include interface path=path, interface=interface, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        % include requirements-list element=component
        % include work-items-list element=component
        % include tests-list element=component
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
