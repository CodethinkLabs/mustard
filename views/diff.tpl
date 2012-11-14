% if not 'other_tree' in locals() or not other_tree:
  % include state state=tree.state, detail='full'
% else:
  <h1>Summary of Changes</h1>
  <dl>
    % include state state=other_tree.state, detail='from'
    % include state state=tree.state, detail='to'
    <dt><h2 class="expanded">Changes</h2></dt>
    <dd>
      % diff = tree.state.diff_against(other_tree.state).strip().splitlines()
      % if not diff:
        <p>No changes between {{other_tree.state.sha1}} and {{tree.state.sha1}}.</p>
      % else:
        <pre class="diff">
          % for line in tree.state.diff_against(other_tree.state).splitlines():
            % if line.startswith('+'):
<span class="diff-added">{{line}}</span>
            % elif line.startswith('-'):
<span class="diff-removed">{{line}}</span>
            % else:
{{line}}
            % end
          % end
        </pre>
      % end
    </dd>
  </dl>
% end

% rebase layout tree=tree
