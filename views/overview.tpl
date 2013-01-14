% def render_test_strategy(path, teststrategy):
  <li>
    % include test-strategy path=path, teststrategy=teststrategy, detail='list'
    % if teststrategy.parents:
      <ul>
        % for path, element in teststrategy.parents.iteritems():
          <li>
            % include element path=path, element=element, detail='list'
          </li>
        % end
      </ul>
    % end
  </li>
% end

% def render_integration_strategy(path, strategy):
  <li>
    % include integration-strategy path=path, strategy=strategy, detail='list'
    % if strategy.teststrategies:
      <ul>
        % for path, teststrategy in strategy.teststrategies.iteritems():
          % render_test(path, teststrategy)
        % end
      </ul>
    % end
    % if strategy.mapped_here:
      <ul>
        % for path, req in strategy.mapped_here.iteritems():
          <li>
            % include requirement path=path, requirement=req, detail='list'
          </li>
        % end
      </ul>
    % end
  </li>
% end

% def render_arch(path, arch):
  <li>
    % include architecture path=path, architecture=arch, detail='list'
    % if arch.components:
      <ul>
        % for path, component in arch.components.iteritems():
          % render_component(path, component)
        % end
      </ul>
    % end
    % if arch.integration_strategy[0]:
      <ul>
        % path, strategy = arch.integration_strategy
        % render_integration_strategy(path, strategy)
      </ul>
    % end
    % if arch.work_items:
      <ul>
        % for path, item in arch.work_items.iteritems():
          <li>
            % include workitem path=path, item=item, detail='list'
          </li>
        % end
      </ul>
    % end
    % if arch.mapped_here:
      <ul>
        % for path, req in arch.mapped_here.iteritems():
          <li>
            % include requirement path=path, requirement=req, detail='list'
          </li>
        % end
      </ul>
    % end
  </li>
% end

% def render_component(path, component):
  <li>
    % include component path=path, component=component, detail='list'
    % if component.architecture:
      <ul>
        % if component.architecture:
          % path, arch = component.architecture
          % render_arch(path, arch)
        % end
      </ul>
    % end
    % if component.interfaces:
      <ul>
        % for path, interface in component.interfaces.iteritems():
          <li>
            % include interface path=path, interface=interface, detail='list'
          </li>
        % end
      </ul>
    % end
    % if component.work_items:
      <ul>
        % for path, item in component.work_items.iteritems():
          <li>
            % include workitem path=path, item=item, detail='list'
          </li>
        % end
      </ul>
    % end
    % if component.teststrategies:
      <ul>
        % for path, teststrategy in component.teststrategies.iteritems():
          % render_test(path, teststrategy)
        % end
      </ul>
    % end
    % if component.mapped_here:
      <ul>
        % for path, req in component.mapped_here.iteritems():
          <li>
            % include requirement path=path, requirement=req, detail='list'
          </li>
        % end
      </ul>
    % end
  </li>
% end

<h1>Overview</h1>
% toparchs = [(x,y) for x,y in tree.find_all(kind='architecture', sort_by='title') if not y.parent[0]]
<ul class="hierarchy">
  % for path, arch in toparchs:
    % render_arch(path, arch)
  % end
</ul>

% rebase layout tree=tree
