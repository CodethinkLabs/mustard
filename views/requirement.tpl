% if detail == 'list':
  % if requirement:
    <a class="requirement" href="/{{requirement.tree.state.identifier}}/requirements#{{path}}">
      {{!'<span class="error">☐</span>' if not [x for x in requirement.mapped_to.itervalues() if x.kind == 'component'] else '☑'}} {{requirement.title}} <span>{{path}}</span>
    </a>
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% elif detail == 'full':
  % if requirement:
    <dt>
      <h2 id="{{path}}">
       {{!'<span class="error">☐</span>' if not [x for x in requirement.mapped_to.itervalues() if x.kind == 'component'] else '☑'}} {{requirement.title}}
        <span><a href="#{{path}}" onclick="return false">{{path}}</a></span>
      </h2>
    </dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        <tr>
          <th>Description</th>
          <td class="description">{{!requirement.description}}</td>
        </tr>
        % include tags-list element=requirement
        % include parents-list element=requirement
        <tr>
          <th>Mapped To</th>
          <td>
            % if requirement.mapped_to:
              <ul class="list">
                % for path, element in requirement.mapped_to.iteritems():
                  <li>
                    % include element path=path, element=element, detail='list'
                  </li>
                % end
              </ul>
            % end
            % if not [x for x in requirement.mapped_to.itervalues() if x.kind == 'component']:
              <p class="error">Not mapped to any components yet.</p>
            % end
          </td>
        </tr>
        % include work-items-list element=requirement
        % include verification-criterion-list element=requirement
      </table>
    </dd>
    % if requirement.subrequirements:
      <dl>
	% for p, r in requirement.sort_subrequirements(sort_by='DEFAULT'):
	  % include requirement path=p, requirement=r, detail='full'
	% end
      </dl>
    % end
    
  % else:
    % include pathnotfound path=path, detail=detail
  % end
% end
