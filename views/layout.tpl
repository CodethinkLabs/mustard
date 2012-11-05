<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{{repository.project.title or 'Unnamed MUSTARD Project'}}</title>
    <link rel="stylesheet" type="text/css" href="/public/style.css"/>
    <script type="text/javascript" src="/public/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" src="/public/effects.js"></script>
  </head>
  <body>
    <div id="body">
      <h1><a href="/{{repository.state.identifier}}">{{repository.project.title or 'Unnamed MUSTARD Project'}}</a></h1>
      <div id="nav">
        <ul>
          <li><a href="/{{repository.state.identifier}}/overview">Overview</a></li>
          <li><a href="/{{repository.state.identifier}}/requirements">Requirements</a></li>
          <li><a href="/{{repository.state.identifier}}/architectures">Architectures</a></li>
          <li><a href="/{{repository.state.identifier}}/components">Components</a></li>
          <li><a href="/{{repository.state.identifier}}/interfaces">Interfaces</a></li>
          <li><a href="/{{repository.state.identifier}}/work-items">Work Items</a></li>
          <li><a href="/{{repository.state.identifier}}/tags">Tags</a></li>
        </ul>
      </div>
      <div id="content">
        %include
      </div>
    </div>
  </body>
</html>
