% if detail == 'list':
  % if component:
    <a class="component" href="/{{component.repository.state.identifier}}/components#{{path}}">
      {{!'<span class="error">☐</span>' if not component.work_items and not component.architecture else '☑'}} {{component.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if component:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not component.work_items and not component.architecture else '☑'}} {{component.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td>{{!component.description}}</td>
        </tr>
        % if component.tags:
          <tr>
            <th>Tags</th>
            <td>
              <ul>
                % for path, tag in component.tags.iteritems():
                  <li>
                    % include tag path=path, tag=tag, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        % if component.parent:
          <tr> 
            % path, architecture = component.parent
            <th>Parent</th>
            <td>
              <p>
                % include architecture path=path, architecture=architecture, detail='list'
              </p>
            </td>
          </tr>
        % end
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
              <ul>
                % for path, interface in component.interfaces.iteritems():
                  <li>
                    % include interface path=path, interface=interface, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        % if component.mapped_here:
          <tr> 
            <th>Requirements</th>
            <td>
              <ul>
                % for path, requirement in component.mapped_here.iteritems():
                  <li>
                    % include requirement path=path, requirement=requirement, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        % if component.work_items:
          <tr>
            <th>Work Items</th>
            <td>
              <ul>
                % for path, item in component.work_items.iteritems():
                  <li>
                    % include workitem path=path, item=item, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
