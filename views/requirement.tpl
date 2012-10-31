% if detail == 'list':
  <a href="/requirements#{{path}}">{{path}} <span>{{requirement.title}}</span></a>
% elif detail == 'full':
  <dt><h2 id="{{path}}">{{path}} <span>{{requirement.title}}</span></h2></dt>
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
                <li><a href="/{{element.kind}}s#{{path}}">{{path}}</a></li>
              % end
            </ul>
          </td>
        </tr>
      % end
    </table>
  </dd>
% end
