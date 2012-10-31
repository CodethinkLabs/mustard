% if repository.work_items():
  <h1>Work Items <span>{{len(repository.work_items())}}</span></h1>
  <dl>
    % for path, item in repository.work_items():
      <dt><h2 id="{{path}}">{{path}} <span>{{item.title}}</span></h2></dt>
      <dd>
        <table cellspacing="0" cellpadding="0">
          <tr>
            <th>Description</th>
            <td>{{!item.description}}</td>
          </tr>
          % if item.tags:
            <tr>
              <th>Tags</th>
              <td>
                <ul>
                  % for path, tag in item.tags.iteritems():
                    <li><a href="/tags#{{path}}">{{path}}</a></li>
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
