% if detail == 'list':
  <a href="/work-items#{{path}}">{{path}} <span>{{work_item.title}}</span></a>
% elif detail == 'full':
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
                <li>
                  % include tag path=path, tag=tag, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
    </table>
  </dd>
% end
