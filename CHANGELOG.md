# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Swagger UI service in docker-compose (#21, PR #38)
- Code coverage with Codecov — 59% baseline (PR #33)
- Codecov configuration for main and develop branches (PR #34)
- Cloud-config for Hetzner server hardening (PR #36)
- Deployment Guide wiki page — Hetzner Cloud + Azure ACI (#22, PR #30, #31)
- OpenAPI 3.1 spec `docs/swagger.yaml` (#19)
- GitHub Actions CI: lint, syntax check, unit tests (#6, PR #16)
- `letsencrypt_email` parameter for automatic SSL certificates (#15, PR #28)
- Batch operations — manage multiple proxy hosts from a YAML list (#7, PR #26)
- `state: absent` support — delete proxy hosts and certificates (#7, PR #26)
- API health-check with retries before token request (#7, PR #26)
- Credential validation via `assert` task (#7, PR #26)
- MIT LICENSE file (PR #25)
- `deploy/` directory with Azure ACI and Hetzner quickstart (PR #31)
- Pre-commit hooks: flake8, ansible-lint, trailing whitespace (#10)
- `.editorconfig` for consistent formatting (#13)
- `CHANGELOG.md` in Keep a Changelog format (#13)
- GitHub issue and PR templates (#13)
- `CODEOWNERS` file (#13)
- `Makefile` with lint, test, and coverage targets (#13)

### Changed

- Module timeout: 30s default, 120s for SSL operations (#35, PR #36)
- Batch tasks split into two phases: non-SSL parallel, SSL sequential with throttle:1 (#35, PR #36)
- `npm_api_ssl_forced` default changed to `false` (#8, PR #28)
- Moved `npm_api_url` from `vars/main.yml` to `defaults/main.yml` (#8, PR #28)
- Docker Compose: removed deprecated `version`, added network, resource limits, logging (#9, PR #27)
- NPM image version updated to 2.11.3
- README fully rewritten with project structure, examples, badge (#12, PR #32)
- Removed Molecule integration workflow from CI (NPM container too heavy for GitHub Actions)

### Fixed

- Module error messages now include HTTP status code and response body (PR #36)
- Renamed `api_secret.yml.example` to `api_secret.example` to prevent `include_vars` conflicts (PR #36)
- `.gitignore` reformatted — one entry per line (#14, PR #29)
- `module.fail_json` positional argument bug (#2, PR #17)
- Timeout and error handling in HTTP requests (#2, PR #17)
- Typos: "remowed", "npm-managenment", "IWhether" (#3, PR #17)
- `meta/main.yml` filled with real metadata (#5, PR #24)

### Security

- Added `no_log: true` to all sensitive tasks (#4, PR #23)
- Removed `api_secret.yml` from git history via `git filter-repo` (#4)
- Removed `certificate.js` override and `LE_MAIL` env var (#15, PR #28)
