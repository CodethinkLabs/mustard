% this_path = path
<hr />
<div class="element">
  % if level < 7:
    <h{{level}} id="{{path}}">{{'.'.join([str(x) for x in index])}}. {{element.title}}</h{{level}}>
  % else:
    <p id="{{path}}"><strong>{{'.'.join([str(x) for x in index])}}. {{element.title}}</strong></p>
  % end

  % if forms.get('%s[description]' % element.kind) and element.description:
    <div class="description">
      {{!element.description}}
    </div>
  % end

  % if forms.get('%s[tags]' % element.kind) and element.tags:
    <p>Tags:</p>
    <ul>
      % for path, tag in element.tags.iteritems():
        % if tag:
          <li><a href="#{{path}}">{{tag.title}}</a></li>
        % else:
          <li>
            % include pathnotfound path=path, detail='list'
          </li>
        % end
      % end
    </ul>
  % end

  % if forms.get('%s[parent]' % element.kind) and element.parent and element.parent[1]:
    % path, parent = element.parent
    <p>Parent:
      % if parent:
        <a href="#{{path}}">{{parent.title}}</a>
      % else:
        % include pathnotfound path=path, detail='list'
      % end
    </p>
  % end

  % if forms.get('%s[mapped-to]' % element.kind) and element.mapped_to:
    <p>Mapped To:</p>
    <ul>
      % for path, el in element.mapped_to.iteritems():
        % if el:
          <li><a href="#{{path}}">{{el.title}}</a></li>
        % else:
          <li>
            % include pathnotfound path=path, detail='list'
          </li>
        % end
      % end
    </ul>
  % end

  % if forms.get('%s[parents]' % element.kind) and element.get_parents():
    <p>Parents:</p>
    <ul>
      % for path, parent in element.get_parents():
        % if parent:
          <li><a href="#{{path}}">{{parent.title}}</a></li>
        % else:
          <li>
            % include pathnotfound path=path, detail='list'
          </li>
        % end
      % end
    </ul>
  % end

  % if forms.get('%s[interfaces]' % element.kind) and element.interfaces:
    <p>Interfaces:</p>
    <ul>
      % for path, el in element.interfaces.iteritems():
        % if el:
          <li><a href="#{{path}}">{{el.title}}</a></li>
        % else:
          <li>
            % include pathnotfound path=path, detail='list'
          </li>
        % end
      % end
    </ul>
  % end

  % if forms.get('%s[vcrits]' % element.kind) and element.integration_strategy[1]:
    % path, strategy = element.integration_strategy
    <p>Integration Strategy:
      % if strategy:
        <a href="#{{path}}">{{strategy.ttile}}</a>
      % else:
        % include pathnotfound path=path, detail='list'
      % end
    </p>
  % end

  % if forms.get('%s[vcrits]' % element.kind) and element.verificationcriteria:
    <p>Verification Criteria:</p>
    <ul>
      % for path, el in element.verificationcriteria.iteritems():
        % if el:
          <li><a href="#{{path}}">{{el.title}}</a></li>
        % else:
          <li>
            % include pathnotfound path=path, detail='list'
          </li>
        % end
      % end
    </ul>
  % end

  % if forms.get('%s[inherited]' % element.kind):
    % inherited_reqs = element.inherited_requirements(sort_by='DEFAULT')
    % if inherited_reqs:
      <p>Inherited Requirements:</p>
      <ul>
        % for path, el in inherited_reqs:
          % if el:
            <li><a href="#{{path}}">{{el.title}}</a></li>
          % else:
            <li>
              % include pathnotfound path=path, detail='list'
            </li>
          % end
        % end
      </ul>
    % end
  % end

  % if forms.get('%s[requirements]' % element.kind):
    % mapped_reqs = element.mapped_requirements(sort_by='DEFAULT')
    % if mapped_reqs:
      <p>Requirements:</p>
      <ul>
        % for path, el in mapped_reqs:
          % if el:
            <li><a href="#{{path}}">{{el.title}}</a></li>
          % else:
            <li>
              % include pathnotfound path=path, detail='list'
            </li>
          % end
        % end
      </ul>
    % end
  % end

  % if forms.get('%s[delegated]' % element.kind):
    % delegated_reqs = element.delegated_requirements(sort_by='DEFAULT')
    % if delegated_reqs:
      <p>Delegated Requirements:</p>
      <ul>
        % for path, el in delegated_reqs:
          % if el:
            <li><a href="#{{path}}">{{el.title}}</a></li>
          % else:
            <li>
              % include pathnotfound path=path, detail='list'
            </li>
          % end
        % end
      </ul>
    % end
  % end

  % if forms.get('%s[used-by]' % element.kind) and element.tagged:
    <p>Used By:</p>
    <ul>
      % for path, el in element.tagged.iteritems():
        % if el:
          <li><a href="#{{path}}">{{el.title}}</a></li>
        % else:
          <li>
            % include pathnotfound path=path, detail='list'
          </li>
        % end
      % end
    </ul>
  % end

  % if forms.get('%s[path]' % element.kind):
    <p>Path: <code>{{this_path}}</code></p>
  % end

  % index = index + [1]
  % level = level + 1
  
  % if element.kind == 'requirement':
    % for path, el in element.sort_subrequirements(sort_by='DEFAULT'):
      % include export-html-element path=path, element=el, index=index, level=level, elements=elements, forms=forms
      % index[-1] += 1
    % end
  % elif element.kind == 'component':
    % for path, el in element.sort_subcomponents(sort_by='DEFAULT'):
      % include export-html-element path=path, element=el, index=index, level=level, elements=elements, forms=forms
      % index[-1] += 1
    % end
  % elif element.kind == 'work-item':
    % for path, el in element.sort_work_items(sort_by='DEFAULT'):
      % include export-html-element path=path, element=el, index=index, level=level, elements=elements, forms=forms
      % index[-1] += 1
    % end
  % end
</div>
