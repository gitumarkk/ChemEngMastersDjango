include:
    - requirements
    - nginx
    - django

supervisor:
  pkg:
    - name: supervisor
    - installed

  service.running:
    - enable: True

supervisor.conf:
    file.managed:
        - name: /etc/supervisor/conf.d/django.conf
        - source: salt://supervisor/django.conf

    service.running:
        - enabled: True
        - watch:
            - file: /etc/supervisor/conf.d/django.conf
