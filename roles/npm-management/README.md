## NPM-MANAGEMENT

Ansible role for [Nginx Proxy Manager v2.14.0](https://github.com/NginxProxyManager/nginx-proxy-manager/tree/v2.14.0).

A simple way to add or delete proxy hosts via Ansible playbook.

## Description

This role manages Nginx Proxy Manager proxy hosts through the REST API.

## Requirements

- Ansible 2.7 or higher
- Docker and Docker-Compose
- Python `requests` module

Change and update a [docker-compose.yml](https://github.com/DenAV/nginx-proxy-manager-ansible/blob/main/docker/docker-compose_npm.yml) file. Bring up your stack by running docker-compose, further info [here](https://github.com/DenAV/nginx-proxy-manager-ansible/tree/main/docker).

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `npm_api_url` | URL for the NPM REST API | `http://192.168.1.5:81/api` |
| `npm_user` | API authentication username | - |
| `npm_password` | API authentication password | - |
| `npm_access_token` | API authentication token | - |
| `npm_api_domain_name` | Domain name for the proxy host | `""` |
| `npm_api_host` | Forward hostname/IP | `""` |
| `npm_api_host_port` | Forward port | `80` |
| `npm_api_ssl_forced` | Force SSL | `False` |
| `npm_api_create_host` | Create proxy host | `False` |

See [`defaults/main.yml`](https://github.com/DenAV/nginx-proxy-manager-ansible/blob/main/roles/npm-management/defaults/main.yml) and [`vars/*.yml`](https://github.com/DenAV/nginx-proxy-manager-ansible/tree/main/roles/npm-management/vars) for all options.

## Dependencies

None.

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

## License

BSD

## Author

https://github.com/DenAV
