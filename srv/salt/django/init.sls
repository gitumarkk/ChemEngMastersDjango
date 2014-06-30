include:
    - requirements

/srv/venv:
    virtualenv.managed:
        - system_site_packages: False
        - runas: {{ pillar["user"]}}  # Who to run it as
        - requirements: salt://django/requirements.txt
        - require:
            - pkg: python-dev
            - pkg: python-pip
            - pkg: python-virtualenv
            - pkg: libpq-dev

production_settings.py:
    file.managed:
        - name: /srv/ChemEngMastersDjango/masters/production_settings.py
        - source: salt://django/production_settings.py
        - template: jinja  # WHat in the world is the template
