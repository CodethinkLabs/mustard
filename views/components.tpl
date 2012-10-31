% if repository.components():
  <h1>Components <span>{{len(repository.components())}}</span></h1>
  <dl>
    % for path, component in repository.components():
      <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % component.title if component.title else ''}}</h2></dt>
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
                    <li><a href="/tags#{{path}}">{{path}}</a></li>
                  % end
                </ul>
              </td>
            </tr>
          % end
          % if component.parent_architecture:
            <tr> 
              % archpath, architecture = component.parent_architecture
              <th>Parent Architecture</th>
              <td><p><a href="/architectures#{{archpath}}">{{archpath}}</a></p></td>
            </tr>
          % end
          % if component.architecture:
            <tr> 
              % archpath, architecture = component.architecture
              <th>Architecture</th>
              <td><p><a href="/architectures#{{archpath}}">{{archpath}}</a></p></td>
            </tr>
          % end
          % if component.covers:
            <tr> 
              <th>Requirements Covered</th>
              <td>
                <ul>
                  % for path, requirement in component.covers.iteritems():
                    <li><a href="/requirements#{{path}}">{{path}}</a></li>
                  % end
                </ul>
              </td>
            </tr>
          % end
        </table>
      </dd>
    % end
  </dl>
% end

% rebase layout repository=repository
