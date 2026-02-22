## Ansible role for [Nginx Proxy Manager v2.14.0](https://github.com/NginxProxyManager/nginx-proxy-manager/tree/v2.14.0)

A simple way to add or delete proxy hosts via Ansible playbook.

## Description

This Ansible role manages Nginx Proxy Manager proxy hosts through its REST API.

## Requirements

- Ansible 2.7 or higher
- Docker and Docker-Compose
- Python `requests` module (`pip install requests`)

Change and update a [docker-compose.yml](https://github.com/DenAV/nginx-proxy-manager-ansible/blob/main/docker/docker-compose_npm.yml) file. Bring up your stack by running docker-compose, further info [here](https://github.com/DenAV/nginx-proxy-manager-ansible/tree/main/docker).

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `npm_api_url` | URL for the NPM REST API | `http://192.168.1.5:81/api` |
| `npm_user` | API authentication username | - |
| `npm_password` | API authentication password | - |
| `npm_access_token` | API authentication token | - |
| `npm_api_domain_name` | Domain name for the proxy host | - |
| `npm_api_host` | Forward hostname/IP | - |
| `npm_api_host_port` | Forward port | `80` |
| `npm_api_ssl_forced` | Force SSL | `False` |
| `npm_api_create_host` | Create proxy host | `False` |

See [`defaults/main.yml`](https://github.com/DenAV/nginx-proxy-manager-ansible/blob/main/roles/npm-management/defaults/main.yml) and [`vars/*.yml`](https://github.com/DenAV/nginx-proxy-manager-ansible/tree/main/roles/npm-management/vars) for all options.

## Example Playbook

### Create a Proxy Host

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

### Create a Proxy Host with Custom Port

```yaml
- name: NPM - create proxy host with custom port
  hosts: localhost
  gather_facts: no

  roles:
    - role: npm-management
      npm_api_domain_name: "app.example.com"
      npm_api_host: "172.16.1.10"
      npm_api_host_port: 8080
      npm_api_ssl_forced: True
      npm_api_create_host: True
```

### Delete a Proxy Host

```yaml
- name: NPM - delete proxy host
  hosts: localhost
  gather_facts: no

  tasks:
    - name: Remove proxy host
      npm_proxy:
        url: "{{ npm_api_url }}"
        token: "{{ npm_access_token }}"
        domain: "site-2.example.com"
        host: "172.16.1.2"
        state: absent
```

## Inventory Example

### hosts.yml

```yaml
all:
  children:
    npm_servers:
      hosts:
        npm-prod:
          ansible_host: 192.168.1.5
        npm-staging:
          ansible_host: 192.168.1.6
```

### group_vars/npm_servers.yml

```yaml
npm_api_url: "http://{{ ansible_host }}:81/api"
npm_user: "admin@example.com"
npm_password: "{{ vault_npm_password }}"
npm_api_ssl_forced: True
```

## Troubleshooting

### Authentication Errors

**Error:** `401 Unauthorized` or `Invalid token`

- Verify `npm_user` and `npm_password` are correct
- Ensure the user has admin privileges in NPM
- Check if the token has expired and regenerate if needed

### Connection Issues

**Error:** `Connection refused` or `timeout`

- Verify NPM is running: `docker ps | grep nginx-proxy-manager`
- Check the API URL port (default: 81)
- Ensure no firewall is blocking the connection

### Certificate Challenges

**Error:** `Certificate validation failed`

- For Let's Encrypt, ensure port 80 is accessible from the internet
- Verify DNS records point to your server
- Check NPM logs: `docker logs nginx-proxy-manager`

### Domain Already Exists

**Error:** `Domain already exists`

- The proxy host may already be configured
- Use `state: absent` first to remove, then recreate
- Check existing hosts in NPM UI

### API Rate Limiting

If making many changes, add delays between tasks:

```yaml
- name: Create proxy host
  npm_proxy:
    # ... options ...
  throttle: 1
```

## License

BSD

## Author

https://github.com/DenAV
