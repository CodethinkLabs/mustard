<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{{tree.project.title or 'Unnamed MUSTARD Project'}}</title>
    <link rel="stylesheet" type="text/css" href="/public/style.css"/>
    <link rel="shortcut icon" type="image/x-icon" href="/public/favicon.ico"/>
    <script type="text/javascript" src="/public/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" src="/public/effects.js"></script>
  </head>
  <body>
    <div id="body">
      <h1 id="title">
        <a href="/{{tree.state.identifier}}">{{tree.project.title or 'Unnamed MUSTARD Project'}}</a>
        <form>
          <select id="state">
            % for tag, identifier in tree.state.repository.tags():
              <option{{!' selected="selected"' if tree.state.identifier == identifier else ''}} value="/{{identifier}}">{{tag}}</option>
            % end
            % for branch, identifier in tree.state.repository.branches():
              <option{{!' selected="selected"' if tree.state.identifier == identifier else ''}} value="/{{identifier}}">{{branch}}</option>
            % end
            <option{{!' selected="selected"' if tree.state.identifier == 'HEAD' else ''}} value="/HEAD">HEAD</option>
            <option{{!' selected="selected"' if tree.state.identifier == 'UNCOMMITTED' else ''}} value="/UNCOMMITTED">UNCOMMITTED</option>
          </select>
        </form>
      </h1>
      <div id="nav">
        <ul>
          <li><a href="/{{tree.state.identifier}}/requirements">Requirements</a></li>
          <li><a href="/{{tree.state.identifier}}/architectures">Architectures</a></li>
          <li><a href="/{{tree.state.identifier}}/components">Components</a></li>
          <li><a href="/{{tree.state.identifier}}/interfaces">Interfaces</a></li>
          <li><a href="/{{tree.state.identifier}}/work-items">Work Items</a></li>
          <li><a href="/{{tree.state.identifier}}/tags">Tags</a></li>
          <li id="nav-more">
            <a>More...</a>
            <ul>
              <li><a href="/{{tree.state.identifier}}/overview">Overview</a></li>
              <li><a href="/{{tree.state.identifier}}/integration-strategies">Integration Strategies</a></li>
              <li><a href="/{{tree.state.identifier}}/verification-criteria">Verification Criteria</a></li>
              <li><a href="/{{tree.state.identifier}}/history">History</a></li>
            </ul>
          </li>
        </ul>
      </div>
      <div id="filterbar" class="center">
        <form onsubmit="return false;">
          <p>
            <label for="filter">Filter:</label>
            <input type="text" id="filter" name="filter" placeholder="Search text" autocomplete="off" style="width: 30%;" />
            <input type="button" id="reset-filter" name="reset-filter" value="Reset" />
            % if tree.project.predefined_filters:
            <select id="predefined-filters" name="predefined-filters">
              <option value="">-- Predefined Filters --</option>
              % for filter in tree.project.predefined_filters:
                <option value="{{filter}}">{{filter}}</option>
              % end
            </select>
            % end
            <input type="button" id="unhappy-filter" name="unhappy-filter" value="☐" />
          </p>
        </form>
      </div>
      <div id="content">
        %include
      </div>
    </div>
    <p class="center">Mustard &copy; 2012, 2013 Codethink Ltd{{!' &#8212; Content &copy; %s' % tree.project.copyright if tree.project.copyright else ''}}</p>
  </body>
</html>
