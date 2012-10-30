<html>
  <head>
    <title>MUSTARD</title>
    <link rel="stylesheet" type="text/css" href="/public/style.css"/>
    <script type="text/javascript" src="/public/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" src="/public/effects.js"></script>
  </head>
  <body>
    <div id="body">
      <h1>{{repository.project.title}}</h1>
      {{!repository.project.description}}
      % if repository.requirements():
        % satisfied_requirements = [y for x,y in repository.requirements() if y.satisfied_by]
        <h1>Requirements <span>{{len(satisfied_requirements)}} of {{len(repository.requirements())}} satisfied</span></h1>
        <dl>
        % for path, requirement in repository.requirements():
          <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % requirement.title if requirement.title else ''}}</h2></dt>
          <dd>
            <h3>Description</h3>
            {{!requirement.description}}
            % if requirement.tags:
              <h3>Tags <span>{{len(requirement.tags)}}</span></h3>
              <ul>
                % for path, tag in requirement.tags.iteritems():
                  <li><a href="#{{path}}">{{path}}</a></li>
                % end
              </ul>
            % end
            % if requirement.satisfied_by:
              <h3>Satisfied By <span>{{len(requirement.satisfied_by)}}</span></h3>
              <ul>
                % for path, element in requirement.satisfied_by.iteritems():
                  <li><a href="#{{path}}">{{path}}</a></li>
                % end
              </ul>
            % end
          </dd>
        % end
        </dl>
      % end
      % if repository.architectures():
        <h1>Architectures <span>{{len(repository.architectures())}}</span></h1>
        <dl>
          % for path, architecture in repository.architectures():
            <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % architecture.title if architecture.title else ''}}</h2></dt>
            <dd>
              <h3>Description</h3>
              {{!architecture.description}}
              % if architecture.components:
                <h3>Components <span>{{len(architecture.components)}}</span></h3>
                <ul>
                  % for path, component in architecture.components.iteritems():
                    <li><a href="#{{path}}">{{path}}</a></li>
                  % end
                </ul>
              % end
              % if architecture.satisfies:
                <h3>Requirements Satisfied <span>{{len(architecture.satisfies)}}</span></h3>
                <ul>
                  % for path, requirement in architecture.satisfies.iteritems():
                    <li><a href="#{{path}}">{{path}}</a></li>
                  % end
                </ul>
            </dd>
          % end
        </dl>
      % end
      % if repository.components():
        <h1>Components <span>{{len(repository.components())}}</span></h1>
        <dl>
          % for path, component in repository.components():
            <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % component.title if component.title else ''}}</h2></dt>
            <dd>
              <h3>Description</h3>
              {{!component.description}}
              % if component.architecture:
                % archpath, architecture = component.architecture
                <h3>Parent Architecture</h3>
                <p><a href="#{{archpath}}">{{archpath}}</a></p>
              % end
              % if component.satisfies:
                <h3>Requirements Satisfied <span>{{len(component.satisfies)}}</span></h3>
                <ul>
                  % for path, requirement in component.satisfies.iteritems():
                    <li><a href="#{{path}}">{{path}}</a></li>
                  % end
               </ul>
              % end
            </dd>
          % end
        </dl>
      % end
      % if repository.tags():
        <h1>Tags <span>{{len(repository.tags())}}</span></h1>
        <dl>
          % for path, tag in repository.tags():
            <dt><h2 id="{{path}}">{{path}}{{!'<span> %s</span>' % tag.title if tag.title else ''}}</h2></dt>
            <dd>
              <h3>Description</h3>
              {{!tag.description}}
            </dd>
          % end
        </dl>
      % end
    </div>
  </body>
</html>
