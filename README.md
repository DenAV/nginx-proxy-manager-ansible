## Ansible role for [Nginx Proxy Manager v2.10.3](https://github.com/NginxProxyManager/nginx-proxy-manager/tree/v2.10.3).
a simple way to add a new proxy host via ansible playbook.
Checked for version v2.10.3.

Description
-----------
module: nginx-proxy-manager-ansible
description: a simple way to add a new proxy host or to delete via ansible playbook

Requirements
------------

This role requires Ansible 2.7 or higher, Docker and Docker-Compose.

Change and update a [docker-compose.yml](https://github.com/DenAV/nginx-proxy-manager-ansible/blob/main/docker/docker-compose_npm.yml) file. Bring up your stack by running docker-compose, further info [here](https://github.com/DenAV/nginx-proxy-manager-ansible/tree/main/docker).

Role Variables
--------------

- `npm_api_url` - IP for the Nginx Proxy Manager REST API. Default to `http://192.168.1.5:81/api`.
- `npm_user` - User to authenticate the Nginx Proxy Manager REST API.
- `npm_password` - Password to authenticate the Nginx Proxy Manager REST API.
- `npm_access_token` - Tokens are required to authenticate against the API.

- `npm_api_domain_name` - Domain Names are required to create the Proxy host.
- `npm_api_host` - Forward Hostname / IP are required to create the Proxy host.
- `npm_api_ssl_forced` - Is SSL Forced? Default is `False`.
- `npm_api_create_host` - Whether to create (present), or no a proxy host. Default is `False`.

See the [`defaults/main.yml`](https://github.com/DenAV/nginx-proxy-manager-ansible/blob/main/roles/npm-management/defaults/main.yml) or [`vars/*.yml`](https://github.com/DenAV/nginx-proxy-manager-ansible/tree/main/roles/npm-management/vars) file listing all possible options which you can be passed to a runner registration command.

Example Playbook
----------------

```yaml
- name: NPM - create proxy host
  hosts: localhost
  gather_facts: no

  roles:
    - role: npm-management
      npm_api_domain_name: "site-2.example.com"
      npm_api_host: "172.16.1.2"
      npm_api_ssl_forced: True
      npm_api_create_host: True

```

Linting
-------

- Install dev tools:

```bash
pip install -r requirements-dev.txt
# or on Windows
py -m pip install -r requirements-dev.txt
```

- Run Ansible lint:

```bash
ansible-lint .
```

- Run Python lint for the custom module:

```bash
flake8 library/npm_proxy.py
```

Secrets Management (Vault)
--------------------------

- Store API credentials in an encrypted vault file at `roles/npm-management/vars/api_secret.yml`.
- Create and edit the vault file:

```bash
ansible-vault create roles/npm-management/vars/api_secret.yml
# add:
# ---
# npm_user: npm-manager@example.com
# npm_password: changeme
```

- Run playbooks with your vault password:

```bash
ansible-playbook pl_npm-management.yml --ask-vault-pass
# or
ansible-playbook pl_npm-management.yml --vault-password-file .vault-pass
```

- An example (unencrypted) template is provided at `roles/npm-management/vars/api_secret.yml.example`.

API Reference (Swagger)
------------------------

The full NPM REST API spec is available at [`docs/swagger.yaml`](docs/swagger.yaml) (OpenAPI 3.1).

**View interactively** — pick any option:

```bash
# Option 1 — Swagger UI in Docker (recommended)
docker run --rm -p 8080:8080 \
  -e SWAGGER_JSON=/spec/swagger.yaml \
  -v $(pwd)/docs:/spec \
  swaggerapi/swagger-ui

# Then open http://localhost:8080

# Option 2 — online editor
# Paste the file contents into https://editor.swagger.io
```

The spec includes a module coverage matrix showing which endpoints are currently supported by `npm_proxy.py`.
