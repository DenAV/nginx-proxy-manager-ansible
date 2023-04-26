# ansible-nginx-proxy-manager

A simple way to add a new proxy host or to delete via ansible playbook.

## Requirements
`pip install requests`

## Module Options
| Parameter | Required | Choices | Default | Comments |
| --- | --- | --- | --- | --- |
| url | Y |  |  |  URL for the Nginx Proxy Manager REST API
| token | Y |  |  | Tokens are required to authenticate against the API
| domain | Y |  |  | Domain Names
| host | Y  |  |  | Forward Hostname / IP
| host_port | N |  | 80 | Forward Port 
| ssl_forced | N | True/False | True  | Is SSL Forced?
| state | N  | present, absent | present | Whether to create (present), or remove (absent) a proxy host.


## Examples
```yaml
name: Create Proxy-Host an NPM
npm_proxy:
  url: "http://192.168.0.1:81/api"
  token: "npm_access_token"
  domain: "domain_name.example.com"
  host: "172.32.0.1"
  ssl_forced: True
  state: present

name: Delete Proxy-Host an NPM
npm_proxy:
  url: "http://192.168.0.1:81/api"
  token: "npm_access_token"
  domain: "domain_name.example.com"
  host: "172.32.0.1"
  state: absent
```

The given code is an Ansible module called nginx-proxy-manager-ansible. The module allows adding, removing or deleting a new proxy host through an Ansible playbook. The module takes in parameters such as the url of the Nginx Proxy Manager REST API, tokens to authenticate, domain names, forward hostname / IP, forward port, SSL forcing, and state (present or absent). 


The module then first checks if the proxy-host already exists, if it does not exist, it creates a new proxy host based on the given parameters. If the state is absent, then the module deletes the proxy host using the given domain name.


The module uses REST APIs to create or delete a proxy host or to search through certificates. The module makes HTTP requests with headers that contain the tokens to authenticate against the API. 


The code seems well documented with a good description of the options, examples, and return values. The code uses the AnsibleModule class, which is an Ansible built-in utility that simplifies module writing. Overall, the code seems well written and should function as expected.