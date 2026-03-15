# npm_proxy

Custom Ansible module for managing Nginx Proxy Manager proxy hosts via the REST API.

## Requirements

```bash
pip install requests
```

## Module Parameters

| Parameter | Required | Choices | Default | Description |
|-----------|----------|---------|---------|-------------|
| url | yes | | | NPM REST API base URL |
| token | yes | | | API authentication token |
| domain | yes | | | Domain name for the proxy host |
| host | yes | | | Forward hostname / IP |
| host_port | no | | 80 | Forward port |
| ssl_forced | no | true / false | true | Force SSL |
| letsencrypt_email | no | | "" | Email for Let's Encrypt certificate |
| state | no | present, absent | present | Create or delete the proxy host |

## Examples

```yaml
- name: Create proxy host with SSL
  npm_proxy:
    url: "http://localhost:81/api"
    token: "{{ npm_access_token }}"
    domain: "site.example.com"
    host: "172.16.1.10"
    ssl_forced: true
    letsencrypt_email: "admin@example.com"
    state: present

- name: Delete proxy host
  npm_proxy:
    url: "http://localhost:81/api"
    token: "{{ npm_access_token }}"
    domain: "site.example.com"
    host: "172.16.1.10"
    state: absent
```