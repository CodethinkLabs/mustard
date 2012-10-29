<html>
  <head>
    <title>MUSTARD</title>
  </head>
  <body>
    % requirements = repository.requirements()
    % if requirements:
      <h1>Requirements</h1>
      <dl>
      % for requirement in requirements:
        <dt>{{requirement['path']}}</dt>
        <dd>{{!requirement['description']}}</dd>
      % end
      </dl>
    % end
  </body>
</html>
