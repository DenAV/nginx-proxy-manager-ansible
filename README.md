# Ansible Role — Nginx Proxy Manager

[![CI — Lint & Unit Tests](https://github.com/DenAV/nginx-proxy-manager-ansible/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/DenAV/nginx-proxy-manager-ansible/actions/workflows/ci.yml)

Ansible role and custom module for managing [Nginx Proxy Manager](https://nginxproxymanager.com/) proxy hosts via the REST API. Create, delete, and batch-manage reverse proxy entries with SSL (Let's Encrypt) — no UI interaction required.

## Features

- Create and delete proxy hosts via NPM API
- Batch operations — manage multiple hosts from a single YAML list
- Automatic SSL certificate provisioning (Let's Encrypt)
- Ansible Vault integration for secure credential storage
- Cloud deployment manifests (Hetzner Cloud, Azure ACI)
- CI/CD with GitHub Actions (lint, unit tests, Molecule integration tests)

**Full documentation:** [Wiki](https://github.com/DenAV/nginx-proxy-manager-ansible/wiki)

## Requirements

- Ansible >= 2.12
- Python >= 3.9
- Docker & Docker Compose
- Nginx Proxy Manager instance (tested with v2.11.x)

## Project Structure

```
nginx-proxy-manager-ansible/
├── library/
│   └── npm_proxy.py           # Custom Ansible module (NPM API client)
├── roles/
│   └── npm-management/        # Main role (tasks, defaults, vars, meta)
├── deploy/
│   ├── azure/npm-aci.yaml     # Azure ACI deployment manifest
│   └── hetzner/               # Hetzner Cloud quickstart
├── docker/
│   └── docker-compose_npm.yml # Docker Compose for NPM
├── docs/
│   └── swagger.yaml           # NPM REST API spec (OpenAPI 3.1)
├── tests/
│   └── test_npm_proxy.py      # Unit tests (pytest)
├── molecule/
│   └── default/               # Molecule integration tests
├── .github/workflows/
│   ├── ci.yml                 # CI: lint + syntax + unit tests
│   └── integration.yml        # Integration: Molecule + Docker
├── pl_npm-management.yml      # Main playbook
└── requirements-dev.txt       # Dev dependencies
```

## Quick Start

1. Start NPM with Docker Compose:

```bash
cd docker
docker compose -f docker-compose_npm.yml up -d
```

2. Run the playbook:

```bash
ansible-playbook pl_npm-management.yml --ask-vault-pass
```

## Role Variables

- `npm_api_url` - NPM REST API base URL. Default is `http://localhost:81/api`.
- `npm_user` - User to authenticate the Nginx Proxy Manager REST API.
- `npm_password` - Password to authenticate the Nginx Proxy Manager REST API.
- `npm_access_token` - Tokens are required to authenticate against the API.

- `npm_api_domain_name` - Domain Names are required to create the Proxy host.
- `npm_api_host` - Forward Hostname / IP are required to create the Proxy host.
- `npm_api_host_port` - Forward Port. Default is `80`.
- `npm_api_ssl_forced` - Is SSL Forced? Default is `false`.
- `npm_api_letsencrypt_email` - Email for Let's Encrypt certificate requests. Default is `""` (empty).
- `npm_api_state` - Whether to create (`present`) or remove (`absent`) a proxy host. Default is `present`.
- `npm_api_hosts` - List of proxy hosts for batch operations. Default is `[]`.

See [`defaults/main.yml`](roles/npm-management/defaults/main.yml) for all available options.

### Overriding Variables

All variables in `defaults/main.yml` can be overridden via inventory, `group_vars`, `host_vars`, or `--extra-vars`:

**Inventory:**
```ini
[npm:vars]
npm_api_url=http://10.0.0.5:81/api
```

**group_vars:**
```yaml
# group_vars/npm.yml
npm_api_url: http://10.0.0.5:81/api
npm_api_ssl_forced: true
npm_api_letsencrypt_email: admin@example.com
```

**Extra vars (highest precedence):**
```bash
ansible-playbook pl_npm-management.yml \
  --extra-vars "npm_api_url=http://10.0.0.5:81/api"
```

## Example Playbook

```yaml
- name: NPM - create proxy host
  hosts: localhost
  gather_facts: no

  roles:
    - role: npm-management
      npm_api_domain_name: "site-2.example.com"
      npm_api_host: "172.16.1.2"
      npm_api_ssl_forced: true
      npm_api_letsencrypt_email: "admin@example.com"
      npm_api_state: present

```

### Delete a proxy host

```yaml
- name: NPM - delete proxy host
  hosts: localhost
  gather_facts: no

  roles:
    - role: npm-management
      npm_api_domain_name: "site-2.example.com"
      npm_api_host: "172.16.1.2"
      npm_api_state: absent

```

### Batch operations

```yaml
- name: NPM - manage multiple proxy hosts
  hosts: localhost
  gather_facts: no

  roles:
    - role: npm-management
      npm_api_hosts:
        - domain_name: "site-a.example.com"
          host: "172.16.1.10"
          ssl_forced: true
          letsencrypt_email: "admin@example.com"
          state: present
        - domain_name: "site-b.example.com"
          host: "172.16.1.20"
          host_port: 8080
          state: present

```

## Linting

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

## Secrets Management (Vault)

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

## API Reference (Swagger)

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

## Deployment Guide

For step-by-step cloud deployment instructions see the [Deployment Guide](https://github.com/DenAV/nginx-proxy-manager-ansible/wiki/Deployment-Guide) wiki page, covering:

- **Hetzner Cloud** — CX22 VM + Docker CE (from EUR 3.49/month)
- **Azure Container Instances** — serverless container (~USD 35/month)
- Ansible inventory examples for both providers

Cloud-specific manifests are in the [`deploy/`](deploy/) directory.

## License

[MIT](LICENSE)
