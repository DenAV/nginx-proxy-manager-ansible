# TODO — nginx-proxy-manager-ansible

> Last updated: 2026-02-22

## Branching & testing strategy

```
feature/fix-xxx  →  develop  →  main  →  release (tag vX.Y.Z)
                      ↑           ↑
                  lint + unit   lint + unit + molecule
```

- **Branches:** `feature/*` or `fix/*` → `develop` → `main`
- **On push/PR to `develop`:** lint (ansible-lint + flake8) + syntax-check + unit tests
- **On PR to `main`:** lint + unit tests + Molecule integration tests (NPM in Docker)
- **After merge to `main`:** create git tag (`vX.Y.Z`) + GitHub Release with changelog
- All P0/P1 fixes go to `develop` first, then PR to `main` after passing CI

---

## P0 — Critical (fix immediately)

- [ ] **Bugs in `library/npm_proxy.py`**
  - [ ] Fix `module.fail_json("...")` → `module.fail_json(msg="...")` (positional arg will cause an error)
  - [ ] Add `timeout=10` to all `requests.get/post/delete` calls
  - [ ] Add `try/except` for `requests.exceptions.ConnectionError`, `Timeout`
  - [ ] Handle unknown `action` in `build_url()` (currently returns `None` → crash)
  - [ ] Remove unused import `from ansible.module_utils.urls import fetch_url`
  - [ ] Fix `choices=['absent', 'present']` in DOCUMENTATION to YAML format
  - [ ] Fix `search_proxy_host` return type — return `None` or `{}` instead of empty string `""`

- [ ] **Typos**
  - [ ] `"remowed"` → `"removed"` (npm_proxy.py, lines ~207, 210, 249)
  - [ ] `"npm-managenment"` → `"npm-management"` (tasks/main.yml, vars/main.yml)
  - [ ] `"IWhether"` → `"Whether"` (README.md, roles/npm-management/README.md)

- [ ] **Security: secrets**
  - [ ] Remove `api_secret.yml` from git history (`git filter-repo`)
  - [ ] Verify `.gitignore` pattern `**/api_secret.yml` works correctly
  - [ ] Add `no_log: true` to task "Create Proxy-Host an NPM"

- [ ] **Fill in `meta/main.yml`** with real data (author, license, min_ansible_version, platforms, galaxy_tags)

---

## P1 — Important (next sprint)

- [ ] **CI/CD: GitHub Actions**
  - [ ] Create workflow `.github/workflows/lint.yml` (ansible-lint + flake8)
  - [ ] Add playbook syntax-check to CI
  - [ ] Remove outdated `.travis.yml` (Python 2.7, `sudo: false`)

- [ ] **Ansible Role: functionality**
  - [ ] Add task for `state: absent` (delete proxy host) in `tasks/main.yml`
  - [ ] Remove redundant `npm_api_create_host` flag — use `state: present/absent` instead
  - [ ] Add batch operations support (loop over a list of hosts from a YAML file)
  - [ ] Increase `timeout: 1` → `timeout: 10` in health-check task
  - [ ] Add `retries`/`delay`/`until` to health-check task

- [ ] **Configuration**
  - [ ] Move `npm_api_url` from `vars/main.yml` to `defaults/main.yml` (remove hardcoded IP `192.168.1.5`)
  - [ ] Document overriding via inventory/group_vars/extra_vars

- [ ] **Docker Compose**
  - [ ] Remove deprecated `version: '3.8'`
  - [ ] Add custom network for isolation
  - [ ] Add resource limits (`deploy.resources.limits`)
  - [ ] Add logging configuration
  - [ ] Remove `certificate.js` override and `${PWD}/internal/` volume mount (see below)
  - [ ] Remove `LE_MAIL` environment variable from docker-compose

- [ ] **Add `letsencrypt_email` to `npm_proxy.py` (replaces certificate.js hack)**
  - [ ] Add `letsencrypt_email` parameter to module `argument_spec`
  - [ ] Pass `meta: {letsencrypt_email, letsencrypt_agree: true}` in create-host API request when `ssl_forced=True`
  - [ ] Add `npm_api_letsencrypt_email` variable to role defaults
  - [ ] Delete `docker/internal/certificate.js` (1235-line full-file override is no longer needed)
  - [ ] Update docker-compose: remove `${PWD}/internal/certificate.js` volume mount and `LE_MAIL` env var

---

## P2 — Improvements (long-term)

- [ ] **Testing**
  - [ ] Add Molecule tests for the role
  - [ ] Add unit tests for `npm_proxy.py` (module already has a TODO for this)
  - [ ] Add pre-commit hooks (ansible-lint, flake8, trailing whitespace)

- [ ] **GitOps**
  - [ ] Declarative state: `proxy_hosts.yml` file with a list of hosts, role converges to it
  - [ ] Support environments (dev/staging/prod) with separate inventories and vars
  - [ ] Tagging/release strategy (semantic versioning)
  - [ ] Move `_ToDo/` to GitHub Issues

- [ ] **Documentation**
  - [ ] Add `state: absent` example to README
  - [ ] Add `host_port` usage example
  - [ ] Add inventory example (host groups, group_vars)
  - [ ] Add troubleshooting section (API errors, auth issues, certificate challenges)
  - [ ] Remove placeholder text from `roles/npm-management/README.md`
  - [ ] Remove AI-generated commentary from `library/README.md`
  - [ ] Update NPM version (2.10.3 → current)

- [ ] **Packaging & structure**
  - [ ] Convert to Ansible Collection
  - [ ] Replace `requests` with `fetch_url` (native Ansible, no external dependencies)
  - [ ] Add `Makefile` with `lint`, `test`, `deploy` targets
  - [ ] Add `.editorconfig`, `CHANGELOG.md`, `CONTRIBUTING.md`
  - [ ] Add GitHub Issues/PR templates (`.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`)
  - [ ] Add `CODEOWNERS`
  - [ ] Add Dependabot / Renovate for Docker image tags

- [ ] **`.gitignore`**
  - [ ] Reformat — one entry per line (currently many entries are merged into single lines)
