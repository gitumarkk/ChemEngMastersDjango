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
