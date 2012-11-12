<h1>Project Description</h1>
% if tree.project.description:
  {{!tree.project.description}}
% else:
  <p>Welcome to your new MUSTARD project. MUSTARD stands for</p>
  <ul>
    <li><strong>M</strong>apped</li>
    <li><strong>U</strong>nified</li>
    <li><strong>S</strong>ystem for</li>
    <li><strong>T</strong>racking</li>
    <li><strong>A</strong>rchitecture,</li>
    <li><strong>R</strong>equirements and</li>
    <li><strong>D</strong>esign.</li>
  </ul>
  <p>It's got to be the easiest way to track the requirements and architecture of a project that you will find.</p>
  <p>Please create a <tt>project.yaml</tt> file to add a title and description.</p>
% end

% rebase layout tree=tree
