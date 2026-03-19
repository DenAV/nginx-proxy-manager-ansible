## Quick Setup

1. Install Docker and Docker Compose

- [Docker Install documentation](https://docs.docker.com/install/)
- [Docker Compose documentation](https://docs.docker.com/compose/)

2. Create an `.env` file to parameterize the image tag.

- Copy the example and edit values:

```bash
cd docker
cp .env.example .env
```

- `.env` contents (example):

```
IMAGE_TAG=2.11.3
```

- `docker-compose_npm.yml` uses this variable:

```yml
services:
  app:
    image: 'jc21/nginx-proxy-manager:${IMAGE_TAG:-2.11.3}'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - npm-data:/data
      - npm-letsencrypt:/etc/letsencrypt
```

3. Bring up your stack by running (from the `docker` directory)

```bash
# Docker Compose V2
docker compose -f docker-compose_npm.yml up -d

# or legacy Docker-Compose
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

5. Swagger UI (API docs)

The compose file includes a Swagger UI service that loads the NPM API schema automatically:

- [http://127.0.0.1:8080](http://127.0.0.1:8080) — interactive API explorer

> **Note:** Swagger UI fetches the schema from NPM internally via the Docker network (`http://app:81/api/schema`). If you access the "Try it out" feature from your browser, requests go to `http://app:81` which is only reachable inside Docker. To execute API calls from Swagger UI, change `API_URL` in the compose file to `http://127.0.0.1:81/api/schema` (or your server's external address).
