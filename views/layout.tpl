<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{{tree.project.title or 'Unnamed Mustard Project'}}</title>
    <link rel="stylesheet" type="text/css" href="{{tree.state.app.base_url}}public/style.css"/>
    <link rel="stylesheet" href="{{tree.state.app.base_url}}public/annotator.min.css">
    <link rel="shortcut icon" type="image/x-icon" href="{{tree.state.app.base_url}}public/favicon.ico"/>
    <script type="text/javascript" src="{{tree.state.app.base_url}}public/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" src="{{tree.state.app.base_url}}public/effects.js"></script>
    <script type="text/javascript" src="{{tree.state.app.base_url}}public/showdown.js"></script>
    <script type="text/javascript" src="{{tree.state.app.base_url}}public/annotator-full.min.js"></script>
  </head>
  <body>
    <div id="body">
      <h1 id="title">
        <a href="{{tree.state.url}}">{{tree.project.title or 'Unnamed Mustard Project'}}</a>
        <form>
          <select id="state">
            % for tag, identifier in tree.state.repository.tags():
              <option{{!' selected="selected" class="active"' if tree.state.identifier == identifier else ''}} value="{{tree.state.app.base_url}}{{identifier}}">{{tag.replace('refs/tags/', 'T ')}}</option>
            % end
            % for branch, identifier in tree.state.repository.branches():
              <option{{!' selected="selected" class="active"' if tree.state.identifier == identifier else ''}} value="{{tree.state.app.base_url}}{{identifier}}">{{branch.replace('refs/heads/', 'B ')}}</option>
            % end
            <option{{!' selected="selected" class="active"' if tree.state.identifier == 'HEAD' else ''}} value="{{tree.state.app.base_url}}HEAD">&gt; HEAD</option>
            % if not tree.state.repository.is_bare():
              <option{{!' selected="selected" class="active"' if tree.state.identifier == 'UNCOMMITTED' else ''}} value="{{tree.state.app.base_url}}UNCOMMITTED">&gt; UNCOMMITTED</option>
            % end
          </select>
        </form>
      </h1>
      <div id="nav">
        <ul>
          <li><a href="{{tree.state.url}}/requirements">Requirements</a></li>
          <li><a href="{{tree.state.url}}/architecture">Architecture</a></li>
          <li><a href="{{tree.state.url}}/interfaces">Interfaces</a></li>
          <li><a href="{{tree.state.url}}/work-items">Work Items</a></li>
          <li><a href="{{tree.state.url}}/tags">Tags</a></li>
          <li id="nav-more">
            <a>More...</a>
            <ul>
              <li><a href="{{tree.state.url}}/overview">Overview</a></li>
              <li><a href="{{tree.state.url}}/integration-strategies">Integration Strategies</a></li>
              <li><a href="{{tree.state.url}}/verification-criteria">Verification Criteria</a></li>
              <li><a href="{{tree.state.url}}/history">History</a></li>
              <li><a href="{{tree.state.url}}/export">Export</a></li>
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
            <input type="button" id="expand-all" name="expand-all" value="[+]" />
          </p>
        </form>
      </div>
      <div id="content">
        %include
      </div>
    </div>
    <p class="center">Mustard &copy; 2012-2014 Codethink Ltd{{!' &#8212; Content &copy; %s' % tree.project.copyright if tree.project.copyright else ''}}</p>
    <script>
      var content = $(document.body).annotator();
      content.annotator('addPlugin', 'Tags');
      content.annotator('addPlugin', 'Filter');
      content.annotator('addPlugin', 'Markdown');
      content.annotator('addPlugin', 'Store', {
        // The endpoint of the store on your server.
        prefix: window.location.protocol + '//' + window.location.hostname + ':5000',

        // Attach the uri of the current page to all annotations to allow search.
        annotationData: {
          'uri': document.URL
        },

        // This will perform a "search" action rather than "read" when the plugin
        // loads. Will request the last 20 annotations for the current url.
        // eg. /store/endpoint/search?limit=20&uri=http://this/document/only
        loadFromSearch: {
          'limit': 2000,
          'uri': document.URL
        }
      });
    </script>  
  </body>
</html>
