<VirtualHost *:80>
    ServerName xyz.domain.com
    DocumentRoot /home/mustard/mustard

    WSGIPassAuthorization On
    WSGIDaemonProcess mustard user=mustard group=everyone processes=1 threads=5
    WSGIScriptAlias / /home/mustard/mustard/adapter.wsgi
    WSGIAuthUserScript /home/mustard/mustard/auth.wsgi

    <Directory /srv/xyz.domain.com>
      AuthType Basic
      AuthName "XYZ Mustard"
      AuthBasicProvider wsgi
      Require valid-user

      SetEnv MUSTARD_SERVER_PATH /home/mustard/mustard/
      SetEnv MUSTARD_PROJECT_PATH /path/to/the/project/mustard/repo
      SetEnv MUSTARD_PLANTUML_JAR /home/mustard/plantuml.jar

      WSGIProcessGroup mustard
      WSGIApplicationGroup %{GLOBAL}
      Order deny,allow
      Allow from all
    </Directory>
</VirtualHost>

