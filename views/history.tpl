% history = tree.state.history()
<h1>History of {{tree.state.identifier}}</h1>
% if history:
  <p id="history-hint"><em>Select two states to show the changes between them.</em></p>
  <p id="history-actions" style="display:none;">With selected: <input id="diff-selected" type="button" value="Show changes" /></p>
  <table id="history" cellspacing="0" cellpadding="0" width="850">
    <tr>
      <th>Actions</th>
      <th>Subject</th>
      <th>Author</th>
      <th>Merged From</th>
    </tr>
    % for state in history:
      % include state state=state, detail='list'
    % end
  </table>
% end
% rebase layout tree=tree
