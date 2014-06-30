include:
    - requirements
    - nginx
    - django

supervisor:
    pkg:
    - name: supervisor
    - installed

    file.managed:
        - name: /etc/supervisor/conf.d/django.conf
        - source: salt://supervisor/django.conf

    service.running:
    - enable: True
    - watch:
        - file: /etc/supervisor/conf.d/django.conf

