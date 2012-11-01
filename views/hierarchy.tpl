% def render_arch(path, arch):
  <li>
    [A]
    % include architecture path=path, architecture=arch, detail='list'
    % if arch.components:
      <ul>
        % for path, component in arch.components.iteritems():
          % render_component(path, component)
        % end
      </ul>
    % end
    % if arch.backlinks:
      <ul>
        % for path, source in arch.backlinks.iteritems():
          % if source.kind == 'work-item':
            <li>
              [WI] % include workitem path=path, item=source, detail='list'
            </li>
          % end
        % end
      </ul>
    % end
    % if arch.covers:
      <ul>
        % for path, req in arch.covers.iteritems():
          <li>
            [R]
            % include requirement path=path, requirement=req, detail='list'
          </li>
        % end
      </ul>
    % end
  </li>
% end

% def render_component(path, component):
  <li>
    [C]
    % include component path=path, component=component, detail='list'
    % if component.architecture:
      <ul>
        % if component.architecture:
          % path, arch = component.architecture
          % render_arch(path, arch)
        % end
      </ul>
    % end
    % if component.backlinks:
      <ul>
        % for path, source in component.backlinks.iteritems():
          % if source.kind == 'work-item':
            <li>
              [WI]
              % include workitem path=path, item=source, detail='list'
            </li>
          % end
        % end
      </ul>
    % end
    % if component.covers:
      <ul>
        % for path, req in component.covers.iteritems():
          <li>
            [R]
            % include requirement path=path, requirement=req, detail='list'
          </li>
        % end
      </ul>
    % end
  </li>
% end

<h1>Architecture Hierarchy</h1>
% toparchs = [(x,y) for x,y in repository.architectures() if not y.for_component]
<ul>
  % for path, arch in toparchs:
    % render_arch(path, arch)
  % end
</ul>

% rebase layout repository=repository
