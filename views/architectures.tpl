% if repository.architectures():
  <h1>Architectures <span>{{len(repository.architectures())}}</span></h1>
  <dl>
    % for path, architecture in repository.architectures():
      <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % architecture.title if architecture.title else ''}}</h2></dt>
      <dd>
        <table cellspacing="0" cellpadding="0">
          <tr>
            <th>Description</th>
            <td>{{!architecture.description}}</td>
          </tr>
          % if architecture.tags:
            <tr>
              <th>Tags</th>
              <td>
                <ul>
                  % for path, tag in architecture.tags.iteritems():
                    <li><a href="/tags#{{path}}">{{path}}</a></li>
                  % end
                </ul>
              </td>
            </tr>
          % end
          % if architecture.for_component:
            % path, component = architecture.for_component
            <tr>
              <th>Parent Component</th>
              <td><p><a href="/components#{{path}}">{{path}}</a></p></td>
            </tr>
          % end
          % if architecture.components:
            <tr>
              <th>Components</th>
              <td>
                <ul>
                  % for path, component in architecture.components.iteritems():
                    <li><a href="/components#{{path}}">{{path}}</a></li>
                  % end
                </ul>
              </td>
            </tr>
          % end
          % if architecture.covers:
            <tr>
              <th>Requirements Covered</th>
              <td>
                <ul>
                  % for path, requirement in architecture.covers.iteritems():
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
