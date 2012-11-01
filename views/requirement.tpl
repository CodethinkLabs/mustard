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
      % if requirement.mapped_to:
        <tr>
          <th>Mapped To</th>
          <td>
            <ul>
              % for path, element in requirement.mapped_to.iteritems():
                <li>
                  % include element path=path, element=element, detail='list'
                </li>
              % end
            </ul>
          </td>
        </tr>
      % end
      % include links element=requirement
    </table>
  </dd>
% end
