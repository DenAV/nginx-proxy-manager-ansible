## Quick Setup

1. Install Docker and Docker-Compose

- [Docker Install documentation](https://docs.docker.com/install/)
- [Docker-Compose Install documentation](https://docs.docker.com/compose/install/)

2. change and update to register with the specified e-mail address in docker-compose_npm.yml file similar to this:

```yml
version: '3.8'
services:
  app:
    image: 'jc21/nginx-proxy-manager:2.10.3'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
      - ${PWD}/internal/certificate.js:/app/internal/certificate.js
    environment:
      LE_MAIL: "npm-admin@example.com"
```

3. Bring up your stack by running

```bash
docker-compose -f docker-compose_npm.yml up -d

```

4. Log in to the Admin UI

When your docker container is running, connect to it on port `81` for the admin interface.
Sometimes this can take a little bit because of the entropy of keys.

[http://127.0.0.1:81](http://127.0.0.1:81)

Default Admin User:
```
Email:    admin@example.com
Password: changeme
```

Immediately after logging in with this default user you will be asked to modify your details and change your password.
