% if detail == 'list':
  % if item:
    <a class="workitem" href="/{{item.repository.state.identifier}}/work-items#{{path}}">{{item.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if item:
    <dt><h2 id="{{path}}">{{item.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if item.description:
          <tr>
            <th>Description</th>
            <td>{{!item.description}}</td>
          </tr>
        % end
        % if item.tags:
          <tr>
            <th>Tags</th>
            <td>
              <ul>
                % for path, tag in item.tags.iteritems():
                  <li>
                    % include tag path=path, tag=tag, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        % if item.parents:
          <tr>
            <th>Parents</th>
            <td>
              <ul>
                % for path, element in item.parents.iteritems():
                  <li>
                    % include element path=path, element=element, detail='list'
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
