# ansible-nginx-proxy-manager

A simple way to add or delete proxy hosts via Ansible playbook.

## Requirements

```bash
pip install requests
```

## Module Options

| Parameter | Required | Choices | Default | Comments |
|-----------|----------|---------|---------|----------|
| url | Yes | | | URL for the Nginx Proxy Manager REST API |
| token | Yes | | | Token to authenticate against the API |
| domain | Yes | | | Domain name for the proxy host |
| host | Yes | | | Forward hostname/IP |
| host_port | No | | 80 | Forward port |
| ssl_forced | No | True/False | True | Force SSL redirect |
| state | No | present, absent | present | Create (present) or remove (absent) a proxy host |

## Examples

### Create a Proxy Host

```yaml
- name: Create proxy host
  npm_proxy:
    url: "http://192.168.0.1:81/api"
    token: "{{ npm_access_token }}"
    domain: "domain_name.example.com"
    host: "172.32.0.1"
    ssl_forced: True
    state: present
```

### Create a Proxy Host with Custom Port

```yaml
- name: Create proxy host on port 8080
  npm_proxy:
    url: "http://192.168.0.1:81/api"
    token: "{{ npm_access_token }}"
    domain: "app.example.com"
    host: "172.32.0.2"
    host_port: 8080
    ssl_forced: True
    state: present
```

### Delete a Proxy Host

```yaml
- name: Delete proxy host
  npm_proxy:
    url: "http://192.168.0.1:81/api"
    token: "{{ npm_access_token }}"
    domain: "domain_name.example.com"
    host: "172.32.0.1"
    state: absent
```
