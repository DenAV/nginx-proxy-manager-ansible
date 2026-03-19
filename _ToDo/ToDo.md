# TODO — nginx-proxy-manager-ansible

> Last updated: 2026-03-19

## Branching & testing strategy

```
feature/fix-xxx  →  develop  →  main  →  release (tag vX.Y.Z)
                      ↑           ↑
                  lint + unit   lint + unit
```

- **Branches:** `feature/*` or `fix/*` → `develop` → `main`
- **On push/PR to `develop`:** lint (ansible-lint + flake8) + syntax-check + unit tests
- **On PR to `main`:** lint + unit tests
- **After merge to `main`:** create git tag (`vX.Y.Z`) + GitHub Release with changelog
- All P0/P1 fixes go to `develop` first, then PR to `main` after passing CI
- Molecule integration tests are for local use only (NPM container too heavy for GitHub Actions)

---

## P0 — Critical (fix immediately)

- [x] **Bugs in `library/npm_proxy.py`** — [#2](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/2) (CLOSED, PR #17)
  - [x] Fix `module.fail_json("...")` → `module.fail_json(msg="...")` (positional arg will cause an error)
  - [x] Add `timeout=10` to all `requests.get/post/delete` calls
  - [x] Add `try/except` for `requests.exceptions.ConnectionError`, `Timeout`
  - [x] Handle unknown `action` in `build_url()` (currently returns `None` → crash)
  - [x] Remove unused import `from ansible.module_utils.urls import fetch_url`
  - [x] Fix `choices=['absent', 'present']` in DOCUMENTATION to YAML format
  - [x] Fix `search_proxy_host` return type — return `None` or `{}` instead of empty string `""`

- [x] **Typos** — [#3](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/3) (CLOSED, PR #17)
  - [x] `"remowed"` → `"removed"` (npm_proxy.py, lines ~207, 210, 249)
  - [x] `"npm-managenment"` → `"npm-management"` (tasks/main.yml, vars/main.yml)
  - [x] `"IWhether"` → `"Whether"` (README.md, roles/npm-management/README.md)

- [x] **Security: secrets** — [#4](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/4) (CLOSED, PR #23 + git filter-repo)
  - [x] Remove `api_secret.yml` from git history (`git filter-repo`) — purged from 2 commits, force-pushed develop+main
  - [x] Verify `.gitignore` pattern `**/api_secret.yml` works correctly — line 21
  - [x] Add `no_log: true` to task "Create Proxy-Host an NPM" — PR #23

- [x] **Fill in `meta/main.yml`** — [#5](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/5) (CLOSED, PR #24)

- [x] **Add LICENSE file** (MIT) — PR #25

---

## P1 — Important (next sprint)

- [x] **CI/CD: GitHub Actions** — [#6](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/6) (CLOSED, PR #16)
  - [x] Create workflow `.github/workflows/ci.yml` (ansible-lint + flake8 + pytest)
  - [x] Add playbook syntax-check to CI
  - [x] Remove outdated `.travis.yml` (Python 2.7, `sudo: false`)
  - [x] ~~Add `.github/workflows/integration.yml` (Molecule on PR to main)~~ — removed, NPM container too heavy for CI

- [x] **Ansible Role: functionality** — [#7](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/7) (CLOSED, PR #26)
  - [x] Add task for `state: absent` (delete proxy host) in `tasks/main.yml`
  - [x] Remove redundant `npm_api_create_host` flag — use `state: present/absent` instead
  - [x] Add batch operations support (loop over a list of hosts from a YAML file)
  - [x] Increase `timeout: 1` → `timeout: 10` in health-check task
  - [x] Add `retries`/`delay`/`until` to health-check task

- [x] **Configuration** — [#8](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/8) (CLOSED, PR #28)
  - [x] Move `npm_api_url` from `vars/main.yml` to `defaults/main.yml` (remove hardcoded IP `192.168.1.5`)
  - [x] Document overriding via inventory/group_vars/extra_vars

- [x] **Docker Compose** — [#9](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/9) (CLOSED, PR #27)
  - [x] Remove deprecated `version: '3.8'`
  - [x] Add custom network for isolation
  - [x] Add resource limits (`deploy.resources.limits`)
  - [x] Add logging configuration
  - [x] Remove `certificate.js` override and `${PWD}/internal/` volume mount (see below)
  - [x] Remove `LE_MAIL` environment variable from docker-compose

- [ ] **Swagger UI service in docker-compose** — [#21](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/21) (PR #38)
  - [x] Add `swagger-ui` service to `docker/docker-compose_npm.yml`
  - [ ] Verify Swagger UI loads the NPM schema successfully (needs live test)
  - [x] Update wiki API Reference page

- [x] **Deployment Guide wiki page (Hetzner Cloud + Azure ACI)** — [#22](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/22) (CLOSED)
  - [x] Hetzner CX22 + Docker CE: full `hcloud` CLI commands, firewall, docker-compose
  - [x] Azure ACI: `az` CLI commands, storage mount, YAML deployment file
  - [x] Comparison table, Ansible inventory examples

- [x] **Add `letsencrypt_email` to `npm_proxy.py` (replaces certificate.js hack)** — [#15](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/15) (CLOSED, PR #28)
  - [x] Add `letsencrypt_email` parameter to module `argument_spec`
  - [x] Pass `meta: {letsencrypt_email, letsencrypt_agree: true}` in create-host API request when `ssl_forced=True`
  - [x] Add `npm_api_letsencrypt_email` variable to role defaults
  - [x] Delete `docker/internal/certificate.js` (1235-line full-file override is no longer needed)
  - [x] Update docker-compose: remove `${PWD}/internal/certificate.js` volume mount and `LE_MAIL` env var

- [x] **Module timeout and batch split** — [#35](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/35) (CLOSED, PR #36)
  - [x] Increase module timeout: 30s default, 120s for SSL operations
  - [x] Split batch tasks: non-SSL parallel, SSL sequential (`throttle: 1`)
  - [x] Rename `api_secret.yml.example` → `api_secret.example` (prevent `include_vars` conflict)
  - [x] Improve error messages: include HTTP status code and response body

---

## P2 — Improvements (long-term)

- [ ] **Testing** — [#10](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/10)
  - [x] Add code coverage with Codecov (pytest-cov, CI upload, badge)
  - [ ] Add Molecule tests for the role (removed from CI — NPM container too heavy for GitHub Actions)
  - [x] Unit tests for `npm_proxy.py` — 24 tests passing, 59% coverage
  - [x] Add pre-commit hooks (ansible-lint, flake8, trailing whitespace)

- [ ] **GitOps** — [#11](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/11)
  - [ ] Declarative state: `proxy_hosts.yml` file with a list of hosts, role converges to it
  - [ ] Support environments (dev/staging/prod) with separate inventories and vars
  - [ ] Tagging/release strategy (semantic versioning)
  - [ ] Move `_ToDo/` to GitHub Issues

- [x] **Swagger UI Docker setup for live NPM API** — [#20](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/20) (CLOSED, PR #19)

- [x] **Documentation** — [#12](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/12) (CLOSED, PR #32)
  - [x] Add `state: absent` example to README
  - [x] Add `host_port` usage example
  - [x] Add inventory example (host groups, group_vars)
  - [x] Add troubleshooting section (wiki Troubleshooting page, linked from README)
  - [x] Remove placeholder text from `roles/npm-management/README.md`
  - [x] Remove AI-generated commentary from `library/README.md`
  - [x] Update NPM version (2.10.3 → current 2.11.x)

- [ ] **Packaging & structure** — [#13](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/13)
  - [ ] Convert to Ansible Collection
  - [ ] Replace `requests` with `fetch_url` (native Ansible, no external dependencies)
  - [x] Add `Makefile` with `lint`, `test`, `deploy` targets
  - [x] Add `.editorconfig`, `CHANGELOG.md`
  - [x] Add GitHub Issues/PR templates (`.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`)
  - [x] Add `CODEOWNERS`
  - [ ] Add Dependabot / Renovate for Docker image tags

- [x] **`.gitignore`** — [#14](https://github.com/DenAV/nginx-proxy-manager-ansible/issues/14) (CLOSED, PR #29)
  - [x] Reformat — one entry per line (currently many entries are merged into single lines)
