# Releasing b5

This document describes how to cut a new release of b5 and publish it to
[PyPI](https://pypi.org/project/b5/).

b5 is developed using b5 itself (see [`build/Taskfile`](build/Taskfile)), so the
release is automated as a task. Every command below has a plain `uv` equivalent
in case you cannot or do not want to use b5.

## Overview

1. Make sure `main` is green and the changelog is up to date.
2. Bump the version, commit, tag and push — automated by `b5 release <version>`.
3. Create a GitHub Release from the new tag.
4. Publishing to PyPI happens automatically via GitHub Actions.

## Versioning

b5 follows [semantic versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).
Breaking changes are marked with `BREAKING:` in the changelog and require a
minor/major bump.

The version number lives in **two** places that must stay in sync:

- `pyproject.toml` &rarr; `[project] version`
- `b5/__init__.py` &rarr; `VERSION`

The `b5 release` task updates both automatically. Keeping them in sync manually
is error-prone — a past release shipped a wrong in-code version number
(see `1.3.5` in the changelog).

## Prerequisites

- A clean checkout of `main` with write access to the
  [`team23/b5`](https://github.com/team23/b5) repository.
- [`uv`](https://docs.astral.sh/uv/) installed.
- Permission to create GitHub Releases (needed to trigger the PyPI publish).

No local PyPI credentials are required: publishing runs in CI via
[trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC), see
[`.github/workflows/release.yml`](.github/workflows/release.yml).

## Step 1 — Prepare the changelog

Ongoing changes are collected under the top `# DEV` heading in
[`CHANGELOG.md`](CHANGELOG.md).

Before releasing, rename that heading to the version you are about to release and
add a fresh `# DEV` section on top for future work:

```markdown
# DEV

* work in progress ;-)

# 1.5.3

* Your release notes here.
```

Commit the changelog (or include it in the release commit — either is fine).

## Step 2 — Run QA

Make sure lint and tests pass before tagging:

```bash
b5 qa          # runs lint + test
# or individually:
b5 lint        # uv run ruff check b5/
b5 test        # uv run pytest b5/

# without b5:
uv run ruff check b5/
uv run pytest b5/
```

CI runs the same checks on every push and pull request
([`lint.yml`](.github/workflows/lint.yml),
[`test.yml`](.github/workflows/test.yml)) across Python 3.10–3.13.

## Step 3 — Bump version, commit, tag and push

```bash
b5 release <version>     # e.g. b5 release 1.5.3
```

This task (see `task:release` in [`build/Taskfile`](build/Taskfile)):

1. Sets the version in `pyproject.toml` via `uv version <version>` (also refreshes `uv.lock`).
2. Rewrites `VERSION` in `b5/__init__.py`.
3. Commits `pyproject.toml`, `uv.lock` and `b5/__init__.py` as `release: 🔖 v<version>`.
4. Creates the git tag `v<version>`.
5. Pushes the commit and the tag.

Doing it manually without b5:

```bash
VERSION=1.5.3
uv version "$VERSION"
sed -i '' "s/^VERSION = .*/VERSION = '${VERSION}'/" b5/__init__.py   # macOS/BSD sed
git add pyproject.toml uv.lock b5/__init__.py
git commit -m "release: 🔖 v${VERSION}" --no-verify
git tag "v${VERSION}"
git push && git push --tags
```

> Note: the tag is `v<version>` (prefixed with `v`), while the PyPI/package
> version is `<version>` (no prefix).

## Step 4 — Create the GitHub Release

Publishing to PyPI is triggered by **publishing a GitHub Release**, not just by
pushing the tag.

1. Go to <https://github.com/team23/b5/releases> and draft a new release.
2. Choose the `v<version>` tag you just pushed.
3. Use the changelog entry for the release notes.
4. Publish the release.

Or with the GitHub CLI:

```bash
gh release create "v${VERSION}" --title "v${VERSION}" --notes-file - <<'EOF'
...release notes...
EOF
```

## Step 5 — Verify the PyPI publish

Publishing the GitHub Release triggers the
[`RELEASE`](.github/workflows/release.yml) workflow, which runs `uv build`
followed by `uv publish`.

- Watch the run under the repository's **Actions** tab.
- Once green, confirm the new version at <https://pypi.org/project/b5/>.

## Manual PyPI publish (fallback)

If the automated workflow is unavailable, you can build and publish locally.
This requires PyPI credentials/token configured for `uv publish`:

```bash
b5 pypi:release      # uv build && uv publish
# or:
uv build
uv publish
```

Prefer the automated GitHub Release flow whenever possible — it avoids handling
PyPI credentials locally.
