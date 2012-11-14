% if detail == 'list':
  % if item:
    <a class="workitem" href="/{{item.tree.state.identifier}}/work-items#{{path}}">
      {{!'<span class="error">☐</span>' if not 'tags/completed' in item.tags else '☑'}} {{item.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if item:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not 'tags/completed' in item.tags else '☑'}} {{item.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if item.description:
          <tr>
            <th>Description</th>
            <td class="description">{{!item.description}}</td>
          </tr>
        % end
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
        <tr>
          <th>Parents</th>
          <td>
            % if item.parents:
              <ul>
                % for path, element in item.parents.iteritems():
                  <li>
                    % include element path=path, element=element, detail='list'
                  </li>
                % end
              </ul>
            % else:
              <p class="error">No parents specified</p>
            % end
          </td>
        </tr>
        <tr>
          <th>Requirements</th>
          <td>
            % inherited_reqs = item.inherited_requirements(sort_by='title')
            % if inherited_reqs:
              <div class="expandable collapsed">
                <h3>Inherited Requirements</h3>
                <ul>
                  % for path, requirement in inherited_reqs:
                    <li>
                      % include requirement path=path, requirement=requirement, detail='list'
                    </li>
                  % end
                </ul>
              </div>
            % end
            % if item.mapped_here:
              <div class="expandable">
                <h3>Requirements Mapped Here</h3>
                <ul>
                  % for path, requirement in item.mapped_here.iteritems():
                    <li>
                      % include requirement path=path, requirement=requirement, detail='list'
                    </li>
                  % end
                </ul>
              </div>
            % end
            % delegated_reqs = item.delegated_requirements(sort_by='title')
            % if delegated_reqs:
              <div class="expandable collapsed">
                <h3>Delegated Requirements</h3>
                <ul>
                  % for path, requirement in delegated_reqs:
                    <li>
                      % include requirement path=path, requirement=requirement, detail='list'
                    </li>
                  % end
                </ul>
              </div>
            % end
          </td>
        </tr>
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
