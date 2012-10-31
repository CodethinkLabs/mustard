% if detail == 'list':
  <a href="/tags#{{path}}">{{tag.title}} <span>{{path}}</span></a>
% elif detail == 'full':
    <dt><h2 id="{{path}}">{{tag.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td>{{!tag.description}}</td>
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
      % include links element=tag
      </table>
    </dd>
% end
