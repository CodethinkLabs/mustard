% verificationcriteria = tree.find_all(kind='verification-criterion', sort_by='title')
% if verificationcriteria:
  <h1>Verification Criteria</h1>
  <dl>
    % for path, criterion in verificationcriteria:
      % include verification-criterion path=path, criterion=criterion, detail='full'
    % end
  </dl>
% end

% rebase layout tree=tree
