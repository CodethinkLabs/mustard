<VirtualHost *:80>
    ServerName xyz.domain.com
    {{ALIAS}}
    DocumentRoot /home/mustard/mustard

    WSGIPassAuthorization On
    WSGIDaemonProcess xyz.domain.com user=mustard group=mustard processes=1 threads=5
    WSGIProcessGroup xyz.domain.com
    WSGIScriptAlias / /home/mustard/mustard/adapter.wsgi
    WSGIApplicationGroup %{GLOBAL}

    <Directory /home/mustard/mustard>
      SetEnv MUSTARD_CONFIG_FILE /home/mustard/.mustard.conf
      SetEnv MUSTARD_AUTH codethink
      SetEnv MUSTARD_AUTH_SERVER {{AUTH_SERVER}}
      SetEnv MUSTARD_PROJECT_CODE {{PROJECT CODE}}
      SetEnv MUSTARD_SERVER_PATH /home/mustard/mustard/
      SetEnv MUSTARD_PROJECT_PATH /path/to/project/mustard/repo.git
      SetEnv MUSTARD_PLANTUML_JAR /home/mustard/plantuml.jar

      Order deny,allow
      Allow from all
    </Directory>
</VirtualHost>

