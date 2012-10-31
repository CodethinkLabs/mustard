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
                    % if element.kind == 'architecture':
                      % include architecture path=path, architecture=element, detail='list'
                    % elif element.kind == 'work-item':
                      % include workitem path=path, item=element, detail='list'
                    % elif element.kind == 'component':
                      % include component path=path, component=element, detail='list'
                    % elif element.kind == 'requirement':
                      % include requirement path=path, requirement=element, detail='list'
                    % elif element.kind == 'tag':
                      % include tag path=path, tag=element, detail='list'
                    % else:
                      <p class="error">CANNOT RENDER ELEMENT KIND "{{element.kind}}".</p>
                    % end
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
      </table>
    </dd>
% end
