% if detail == 'list':
  % if strategy:
    <a class="strategy" href="/{{strategy.tree.state.identifier}}/integration-strategies#{{path}}">
      {{!'<span class="error">☐</span>' if not strategy.tests else '☑'}} {{strategy.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if strategy:
    <dt><h2 id="{{path}}">{{!'<span class="error">☐</span>' if not strategy.tests else '☑'}} {{strategy.title}} <span>{{path}}</span></h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td class="description">{{!strategy.description}}</td>
        </tr>
        % if strategy.tags:
          <tr>
            <th>Tags</th>
            <td>
              <ul>
                % for path, tag in strategy.tags.iteritems():
                  <li>
                    % include tag path=path, tag=tag, detail='list'
                  </li>
                % end
              </ul>
            </td>
          </tr>
        % end
        <tr> 
          <th>Parent</th>
          <td>
            <p>
              % path, architecture = strategy.parent
              % if path:
                % include architecture path=path, architecture=architecture, detail='list'
              % else:
                <span class="error">No parent specified</span>
              % end
            </p>
          </td>
        </tr>
        <tr>
          <th>Requirements</th>
          <td>
            % inherited_reqs = strategy.inherited_requirements(sort_by='title')
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
            % if strategy.mapped_here:
              <div class="expandable">
                <h3>Requirements Mapped Here</h3>
                <ul>
                  % for path, requirement in strategy.mapped_here.iteritems():
                    <li>
                      % include requirement path=path, requirement=requirement, detail='list'
                    </li>
                  % end
                </ul>
              </div>
            % end
            % delegated_reqs = strategy.delegated_requirements(sort_by='title')
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
        <tr>
          <th>Tests</th>
          <td>
            % if strategy.tests:
              <ul>
                % for path, test in strategy.tests.iteritems():
                  <li>
                    % include test path=path, test=test, detail='list'
                  </li>
                % end
              </ul>
            % else:
              <p class="error">No tests specified.</p>
            % end
          </td>
        </tr>
      </table>
    </dd>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
