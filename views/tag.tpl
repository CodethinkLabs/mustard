% if detail == 'list':
  % if tag:
    <a class="tag" href="/{{tag.repository.state.identifier}}/tags#{{path}}">{{tag.title}} <span>{{path}}</span></a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if tag:
    <dt><h2 id="{{path}}">{{tag.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td class="description">{{!tag.description}}</td>
        </tr>
        % if tag.tagged:
          <tr>
            <th>Used By</th>
            <td>
              <ul>
                % for path, element in tag.tagged.iteritems():
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
