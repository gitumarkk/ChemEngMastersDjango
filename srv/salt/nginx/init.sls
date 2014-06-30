nginx:
  pkg:
    - name: nginx
    - installed
  service.running:
    - enable: True
    - watch:
        - file: /etc/nginx/nginx.conf

default-nginx:
  file.absent:
    - name: /etc/nginx/sites-enabled/default

nginx.conf:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - user: {{ pillar["user"]}}
    - template: jinja
    - mode: 644
    - require:
        - pkg: nginx


nginx-server-conf:
    file.managed:
        - name: /etc/nginx/conf.d/server.conf
        - source: salt://nginx/server.conf
        - require:
            - pkg: nginx
