# npm-management

Ansible role for managing [Nginx Proxy Manager](https://nginxproxymanager.com/) proxy hosts via the REST API.

Create, delete, and batch-manage reverse proxy entries with SSL (Let's Encrypt) — no UI interaction required.

## Requirements

- Ansible >= 2.12
- Python >= 3.9
- Docker & Docker Compose
- Nginx Proxy Manager instance (tested with v2.11.x)

Role Variables
--------------

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
- `npm_api_hosts` - List of proxy hosts for batch operations. Default is `[]` (empty, use single host variables instead).

See [`defaults/main.yml`](defaults/main.yml) for all available options.

### Overriding Variables

All variables in `defaults/main.yml` can be overridden via inventory, `group_vars`, `host_vars`, or `--extra-vars`:

```ini
# inventory
[npm:vars]
npm_api_url=http://10.0.0.5:81/api
```

```yaml
# group_vars/npm.yml
npm_api_url: http://10.0.0.5:81/api
npm_api_ssl_forced: true
npm_api_letsencrypt_email: admin@example.com
```

```bash
# extra vars
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
        - domain_name: "old-site.example.com"
          host: "172.16.1.30"
          state: absent
```

## License

[MIT](../../LICENSE)

## Author

[DenAV](https://github.com/DenAV)


