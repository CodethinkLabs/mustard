% if detail == 'list':
    <a href="/components#{{path}}">{{path}} <span>{{component.title}}</span></a>
% elif detail == 'full':
  <dt><h2 id="{{path}}">{{path}} <span>{{component.title}}</span></h2></dt>
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
                <li>
                  % include tag path=path, tag=tag, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
      % if component.parent_architecture:
        <tr> 
          % path, architecture = component.parent_architecture
          <th>Parent Architecture</th>
          <td>
            <p>
              % include architecture path=path, architecture=architecture, detail='list'
            </p>
          </td>
        </tr>
      % end
      % if component.architecture:
        <tr> 
          % path, architecture = component.architecture
          <th>Architecture</th>
          <td>
            <p>
              % include architecture path=path, architecture=architecture, detail='list'
            </p>
          </td>
        </tr>
      % end
      % if component.covers:
        <tr> 
          <th>Requirements Covered</th>
          <td>
            <ul>
              % for path, requirement in component.covers.iteritems():
                <li>
                  % include requirement path=path, requirement=requirement, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
    </table>
  </dd>
% end
