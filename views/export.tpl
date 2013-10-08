<h1>Export</h1>

<p>Select which elements and fields to include in the exported data.</p>

<form action="{{tree.state.url}}/export" method="post">
  <fieldset>
    <table>
    % index = 0
    % for kind, info in sorted(elements.iteritems(), key=lambda x: x[1]['title-plural']):
      % if index % 2 == 0:
        <tr>
      % end
      <td>
        <h2><input type="checkbox" name="select-{{kind}}"{{' checked="checked"' if info['default'] else ''}} /> {{info['title-plural']}}</h2>
        <p class="fields">
          % for field in info['fields']:
            <input type="checkbox" id="{{kind}}-{{field['name']}}" name="{{kind}}[{{field['name']}}]"{{' checked="checked"' if field['default'] else ''}} /> <label for="{{kind}}-{{field['name']}}">{{field['title']}}</label><br />
          % end
        </p>
      </td>
      % if index % 2 == 1:
        </tr>
      % end
      % index += 1
    % end
    </table>
    <p class="buttons"><input type="submit" value="Export" /></p>
  </fieldset>
</form>

% rebase layout tree=tree
