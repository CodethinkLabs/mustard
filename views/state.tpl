% if detail == 'list':
  <tr class="row" id="{{state.sha1}}">
    <td>
      <a href="{{state.app.base_url}}/{{state.sha1_url}}">Browse</a>
      % if state.right:
        <a href="{{state.app.base_url}}/diff/{{state.sha1}}~1">Diff</a>
      % else:
        <a href="{{state.app.base_url}}/diff">Diff</a>
      % end
    </td>
    <td>{{state.title if state.title and len(state.title) < 73 else '%s...' % state.title[0:72]}}</td>
    <td><a href="mailto:{{state.author_email}}">{{state.author or ' '}}</a></td>
    <td>
      % if state.right:
        <a href="{{state.app.base_url}}/{{state.right}}/history">{{state.right[0:8]}}...</a>
      % end
    </td>
  </tr>
% elif detail in ['from', 'to']:
  <dt><h2 class="expanded">{{'Between' if detail == 'from' else 'And'}}</h2></dt>
  <dd>
    <table cellspacing="0" cellpadding="0">
      % if state.author:
        <tr>
          <th>Author</th>
          <td><a href="mailto:{{state.author_email}}">{{state.author}}</a></td>
        </tr>
      %end
      % if state.date:
        <tr>
          <th>Date</th>
          <td>{{state.date}}</td>
        </tr>
      % end
      <tr>
        <th>Title</th>
        <td>{{state.title}}</td>
      </tr>
      % if state.body:
        <tr>
          <th>Description</th>
          <td>{{state.body}}</td>
        </tr>
      % end
    </table>
  </dd>
% else:
  <h1>Changes in {{state.sha1}}</h1>
  <dl>
    <dt><h2 class="expanded">Meta Information</h2></dt>
    <dd>
      <table cellspacing="0" cellpadding="0">
        % if state.author:
          <tr>
            <th>Author</th>
            <td><a href="mailto:{{state.author_email}}">{{state.author}}</a></td>
          </tr>
        %end
        % if state.date:
          <tr>
            <th>Date</th>
            <td>{{state.date}}</td>
          </tr>
        % end
        <tr>
          <th>Title</th>
          <td>{{state.title}}</td>
        </tr>
        % if state.body:
          <tr>
            <th>Description</th>
            <td>{{state.body}}</td>
          </tr>
        % end
      </table>
    </dd>
    <dt><h2 class="expanded">Changes</h2></dt>
    <dd>
      % diff = state.diff.strip().splitlines()
      % if not diff:
        <p>No changes introduced in {{state.sha1}}.</p>
      % else:
        <pre class="diff">
          % for line in diff:
            % if line.startswith('+'):
<span class="diff-added">{{line}}</span>
            % elif line.startswith('-'):
<span class="diff-removed">{{line}}</span>
            % else:
{{line}}
            % end
          % end
        % end
      </pre>
    </dd>
  </dl>
% end
