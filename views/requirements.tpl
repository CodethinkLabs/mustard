% if repository.requirements():
  % covered_requirements = [y for x,y in repository.requirements() if y.covered_by]
  <h1>Requirements <span>{{len(covered_requirements)}} of {{len(repository.requirements())}} covered</span></h1>
  <dl>
    % for path, requirement in repository.requirements():
      <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % requirement.title if requirement.title else ''}}</h2></dt>
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
                    <li><a href="/tags#{{path}}">{{path}}</a></li>
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
                    <li><a href="/requirements#{{path}}">{{path}}</a></li>
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
                    <li><a href="/requirements#{{path}}">{{path}}</a></li>
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
  </dl>
% end

% rebase layout repository=repository
