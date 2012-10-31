% if detail == 'list':
  <a href="/requirements#{{path}}">{{requirement.title}} <span>{{path}}</span></a>
% elif detail == 'full':
  <dt><h2 id="{{path}}">{{requirement.title}} <span>{{path}}</span></h2></dt>
  <dd>
    <table cellspacing="0" cellpadding="0">
      <tr>
        <th>Description</th>
        <td>{{!requirement.description}}</td>
      </tr>
      % if requirement.tags:
        <tr>
          <th>Tags</th>
          <td>
            <ul>
              % for path, tag in requirement.tags.iteritems():
                <li>
                  %include tag path=path, tag=tag, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
      % if requirement.parent_requirements:
        <tr>
          <th>Parent Requirements</th>
          <td>
            <ul>
              % for path, other in requirement.parent_requirements.iteritems():
                <li>
                  % include requirement path=path, requirement=other, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
      % if requirement.sub_requirements:
        <tr>
          <th>Subrequirements</th>
          <td>
            <ul>
              % for path, other in requirement.sub_requirements.iteritems():
                <li>
                  % include requirement path=path, requirement=other, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
      % if requirement.covered_by:
        <tr>
          <th>Covered By</th>
          <td>
            <ul>
              % for path, element in requirement.covered_by.iteritems():
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
