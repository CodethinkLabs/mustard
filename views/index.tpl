<html>
  <head>
    <title>MUSTARD</title>
    <link rel="stylesheet" type="text/css" href="/public/style.css"/>
    <script type="text/javascript" src="/public/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" src="/public/effects.js"></script>
  </head>
  <body>
    % if repository.requirements():
      <h1>Requirements</h1>
      <dl>
      % for path, requirement in repository.requirements():
        <dt><h2 id="{{path}}">{{path}}</h2></dt>
        <dd>
          <h3>Description</h3>
          {{!requirement.description}}
          % if requirement.tags:
            <h3>Tags</h3>
            <ul>
              % for path, tag in requirement.tags.iteritems():
                <li><a href="#{{path}}">{{path}}</a></li>
              % end
            </ul>
          % end
        </dd>
      % end
      </dl>
    % end
    % if repository.tags():
      <h1>Tags</h1>
      <dl>
        % for path, tag in repository.tags():
          <dt><h2 id="{{path}}">{{path}}</h2></dt>
          <dd>
            <h3>Description</h3>
            {{!tag.description}}
          </dd>
        % end
      </dl>
    % end
  </body>
</html>
