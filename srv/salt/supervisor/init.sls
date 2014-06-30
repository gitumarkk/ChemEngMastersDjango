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
        - name: /etc/supervisor/conf.d/supervisor.conf
        - source: salt://supervisor/supervisor.conf

    service.running:
        - enabled: True
        - watch:
            - file: /etc/supervisor/conf.d/supervisor.conf
