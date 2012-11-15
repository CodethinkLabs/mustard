<tr> 
  <th>Requirements</th>
  <td>
    % inherited_reqs = element.inherited_requirements(sort_by='title')
    % if inherited_reqs:
      <div class="expandable secondary">
        <h3>Inherited Requirements</h3>
        <ul class="list">
          % for path, requirement in inherited_reqs:
            <li>
              % include requirement path=path, requirement=requirement, detail='list'
            </li>
          % end
        </ul>
      </div>
    % end
    % if element.kind == 'component':
      % if element.mapped_here or not element.architecture:
        % if element.mapped_here:
          <div class="expandable expanded">
            <h3>Requirements</h3>
            <ul class="list">
              % for path, requirement in element.mapped_here.iteritems():
                <li>
                  % include requirement path=path, requirement=requirement, detail='list'
                </li>
              % end
            </ul>
          </div>
        % else:
          <p class="error">This element either needs an architecture or have requirements mapped to it.</p>
        % end
      % end
    % else:
      % if element.mapped_here:
        <div class="expandable expanded">
          <h3>Requirements</h3>
          <ul class="list">
            % for path, requirement in element.mapped_here.iteritems():
              <li>
                % include requirement path=path, requirement=requirement, detail='list'
              </li>
            % end
          </ul>
        </div>
      % end
    % end
    % delegated_reqs = element.delegated_requirements(sort_by='title')
    % if delegated_reqs:
      <div class="expandable secondary">
        <h3>Delegated Requirements</h3>
        <ul class="list">
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
