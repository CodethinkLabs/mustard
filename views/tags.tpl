% if repository.tags():
  <h1>Tags <span>{{len(repository.tags())}}</span></h1>
  <dl>
    % for path, tag in repository.tags():
      <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % tag.title if tag.title else ''}}</h2></dt>
      <dd>
        <table cellspacing="0" cellpadding="0">
          <tr>
            <th>Description</th>
            <td>{{!tag.description}}</td>
          </tr>
        </table>
      </dd>
    % end
  </dl>
% end

% rebase layout repository=repository
