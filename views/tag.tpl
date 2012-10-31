% if detail == 'list':
  <a href="/tags#{{path}}">{{path}} <span>{{tag.title}}</span></a>
% elif detail == 'full':
    <dt><h2 id="{{path}}">{{path}} <span>{{tag.title}}</span></h2></dt>
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
                  <li><a href="/{{element.kind}}s#{{path}}">{{path}}</a></li>
                % end
              </ul>
            </td>
          </tr>
        % end
      </table>
    </dd>
% end
