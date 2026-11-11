# Release process

This process covers release preparation and publication. A release requires explicit approval for branch creation, commits, pushes, pull requests, merges, live-server operations, tags, and publication. Preserve existing branch protections; changes to protection require separate approval.

## Branches and scope

| Branch | Purpose |
| --- | --- |
| `main` | Stable release history |
| `develop` | Integration for the next release |
| `feature/<issue>-*`, `fix/<issue>-*`, `chore/<issue>-*` | One issue or independently reviewable change, based on `develop` |
| `hotfix/<issue>-*` | Urgent correction to a published release, based on `main` |

Track changes in issues. Assign the intended issues to a release milestone and use the project board for progress. Agree on the scope, acceptance criteria, dependencies, supported environments, and exclusions before preparing the release. A partial implementation does not complete an issue.

Integrate only the upcoming release into `develop`. Keep work for a later release in its own branch until the current release is published. Create a pull request from each working branch to `develop`; after review and passing checks, use squash merge. Do not develop directly on `main`.

Promote `develop` to `main` with a merge commit, and merge `main` back into `develop` after publication. These merge commits preserve the common history of the long-lived branches. Do not rewrite published history. Repository rules must permit merge commits before using this process; do not bypass a conflicting rule. Resolve existing branch divergence before promotion, preserving changes on both branches.

## Versioning

Use [Semantic Versioning](https://semver.org/) and tags in the form `vMAJOR.MINOR.PATCH`:

- Increment PATCH for backward-compatible fixes.
- Increment MINOR for backward-compatible functionality.
- Increment MAJOR for incompatible changes, including removal of supported environments.

Choose the version based on the complete release scope. Document compatibility changes and migration guidance in release notes. Never move or reuse a published tag; correct a published release with a new version.

## Prepare a release candidate

1. Complete the agreed issue requirements and merge the reviewed changes into `develop`. Keep later-release changes out.
2. Update `CHANGELOG.md` and relevant documentation through `develop`, including the release version, date, compatibility changes, and known limitations. Freeze the release scope.
3. Record the exact `develop` commit SHA as the candidate. Run the repository CI and the agreed module and role checks on the release's supported stack. A newer toolchain alone does not prove compatibility with the existing stack.
4. For new features, critical fixes, and requests from clients or other contributors, test that exact candidate on the dedicated NPM test server. Record the source SHA, image and tool versions, scenarios, expected and observed results, and outcome. Follow the agreed release test matrix for other changes as well. Local mocks and unit tests do not replace live NPM acceptance.
5. Keep credentials, infrastructure details, and detailed reports private. Publish only a safe summary of the evidence. If required acceptance is unavailable or fails, the release is blocked.

If the candidate changes, record the new SHA and repeat affected tests and the final release checks. Obtain separate approval before deploying to or operating the test server.

## Promote and publish

1. Open a pull request from the tested `develop` candidate to `main`. Confirm that CI runs on the PR and passes, review the diff and acceptance evidence, and obtain merge approval.
2. Merge using a merge commit. Verify the resulting `main` tree matches the tested candidate, for example with `git diff --exit-code <candidate-sha> <main-sha>`. If it differs, test the resulting content again before publication. Run the relevant checks on the resulting `main` commit and resolve failures.
3. With explicit approval, create the release tag at that verified `main` commit and publish a GitHub Release with the changelog, compatibility notes, and relevant limitations.
4. Merge `main` back into `develop`, including any release changes. Check and resolve differences before starting the next release. Delete working branches only when their removal is approved.

CI currently runs lint, syntax checks, and unit tests; it does not provide an automated Molecule integration workflow. A green CI run does not by itself establish live NPM compatibility.

## Issues and release tracking

- Use `Backlog` for pending work and `In progress` for active work.
- Keep work in `In review` while a PR is under review or the change is in `develop` but not yet in `main`.
- Use `Done` only after all requirements and acceptance checks are complete, the change is in `main`, and the issue is closed. Use non-closing references such as `Refs #123` in PRs to `develop` to avoid premature closure.
- Close the milestone after the release is published. Issue completion and release publication are separate events.

## Urgent hotfixes

When a published release needs an urgent fix while `develop` contains unfinished work, branch `hotfix/<issue>-*` from `main`. Add a regression test, open a PR to `main`, and perform the checks and acceptance applicable to the fix, including exact-candidate live testing for critical fixes. After approval, squash merge, verify the resulting `main`, and publish a new patch release using the approval and tagging rules above. Merge `main` into `develop` promptly so the fix remains in future releases. Do not include unrelated unreleased work in the hotfix.
