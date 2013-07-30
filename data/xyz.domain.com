<VirtualHost *:80>
    ServerName xyz.domain.com
    {{ALIAS}}

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
</VirtualHost>

<VirtualHost *:443>
    ServerName xyz.domain.com
    {{ALIAS}}
    DocumentRoot /home/mustard/mustard

    SSLEngine on
    SSLCipherSuite ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP

    SSLCertificateFile {{SSL CERT PATH}}/{{SSL CERT NAME}}.crt
    SSLCertificateKeyFile {{SSL CERT PATH}}/{{SSL CERT NAME}}.key
    SSLCertificateChainFile {{SSL CERT PATH}}/{{SSL CERT NAME}}.ca-bundle
    SSLCACertificateFile {{SSL CERT PATH}}/{{SSL CERT NAME}}.ca-bundle

    WSGIPassAuthorization On
    WSGIDaemonProcess xyz.domain.com user=mustard group=mustard processes=1 threads=5
    WSGIProcessGroup xyz.domain.com
    WSGIScriptAlias / /home/mustard/mustard/adapter.wsgi
    WSGIApplicationGroup %{GLOBAL}

    <Directory /home/mustard/mustard>
      SetEnv MUSTARD_CONFIG_FILE /home/mustard/.mustard.conf
      SetEnv MUSTARD_AUTH codethink
      SetEnv MUSTARD_AUTH_SERVER {{AUTH SERVER}}
      SetEnv MUSTARD_PROJECT_CODE {{PROJECT CODE}}
      SetEnv MUSTARD_SERVER_PATH /home/mustard/mustard/
      SetEnv MUSTARD_PROJECT_PATH /path/to/project/mustard/repo.git
      SetEnv MUSTARD_PLANTUML_JAR /home/mustard/plantuml.jar

      Order deny,allow
      Allow from all
    </Directory>
</VirtualHost>

