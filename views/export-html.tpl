<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>{{tree.project.title or 'Unnamed Mustard Project'}}</title>
    <link rel="shortcut icon" type="image/x-icon" href="/public/favicon.ico"/>
    <style type="text/css" media="projection,screen,tv">
      hr {
        border: 0em;
        border-bottom: thin solid #999;
      }
      .error {
        color: #ff0000;
      }
    </style>
  </head>
  <body>
    <div id="body">
      <div id="title">
        <h1><a href="/{{tree.state.url}}">{{tree.project.title or 'Unnamed Mustard Project'}}</a></h1>
        <p>{{!tree.project.description}}</p>
      </div>
      <div id="nav">
        <ol>
          % for field, info in sorted(elements.iteritems(), key=lambda x: x[1]['title-plural']):
            % if forms.get('select-%s' % field):
              % kind_elements = tree.find_all(kind=field, top_level=True)
              % if kind_elements:
                <li><a href="#{{info['title-plural'].replace(' ', '-').lower()}}">{{info['title-plural']}}</a></li>
              % end
            % end
          % end
        </ol>
      </div>
      <div id="content">
        % index = [1]
        % level = 3

        % for field, info in sorted(elements.iteritems(), key=lambda x: x[1]['title-plural']):
          % if forms.get('select-%s' % field):
            % kind_elements = tree.find_all(kind=field, sort_by='DEFAULT', top_level=True)
            % if kind_elements:
              <h2 id="{{info['title-plural'].replace(' ', '-').lower()}}">{{str(index[0])}}. {{info['title-plural']}}</h2>
              % kind_index = index + [1]
              % for path, element in tree.find_all(kind=field, sort_by='DEFAULT', top_level=True):
                % include export-html-element path=path, element=element, index=kind_index, level=level, elements=elements, forms=forms
                % kind_index[-1] += 1
              % end
              % index[-1] += 1
            % end
          % end
        % end
      </div>
    </div>
    <hr />
    <p class="center">Mustard &copy; 2012, 2013 Codethink Ltd{{!' &#8212; Content &copy; %s' % tree.project.copyright if tree.project.copyright else ''}}</p>
  </body>
</html>
