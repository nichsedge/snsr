# Upgrade & publish `snsr` so changes reach all users

Use this prompt after merging code changes that should reach end users (who install via `pip install snsr` or `uvx snsr`). PyPI is the single source of truth — until a new version is published, users will keep getting the old code.

## Preconditions

- Working tree is clean (`git status` shows no uncommitted changes), or all intended changes are already committed.
- You are on `main` and up to date with `origin/main`.
- PyPI credentials are available: either `UV_PUBLISH_TOKEN` env var, `~/.pypirc`, or interactive login.
- `uv` is installed.

If any precondition fails, stop and tell the user instead of guessing.

## Steps

1. **Decide the version bump.** Read the current `version` from `pyproject.toml`. Default to a **patch** bump (e.g. `0.1.6` → `0.1.7`). Bump **minor** if user-facing CLI flags or behavior changed; bump **major** only if the user explicitly asks. If unsure, ask the user before publishing.

2. **Update `pyproject.toml`.** Edit only the `version = "..."` line.

3. **Sync the lockfile.** Run `uv lock` so `uv.lock` reflects the new version (it pins the local project).

4. **Build the distributions.** Run `uv build`. This produces `dist/snsr-<version>-py3-none-any.whl` and `dist/snsr-<version>.tar.gz`. Confirm both files exist and the version string matches.

5. **Sanity-check the wheel.** Install it into a throwaway venv and import the package:
   ```
   uv run --isolated --with dist/snsr-<version>-py3-none-any.whl python -c "import snsr.cli; print('ok')"
   ```
   If the import fails, fix before publishing — a broken wheel on PyPI cannot be replaced, only yanked.

6. **Publish.** Run `uv publish` (uses `UV_PUBLISH_TOKEN` or `~/.pypirc`). Watch for the `View at: https://pypi.org/project/snsr/<version>/` line.

7. **Commit and tag.** Create one commit with the version bump and lockfile change, then tag it:
   ```
   git add pyproject.toml uv.lock
   git commit -m "Release v<version>"
   git tag v<version>
   git push origin main --tags
   ```

8. **Verify the publish reached users.** Run `uvx --refresh snsr@<version> --help` (or `pip install --upgrade snsr`) and confirm the new version installs cleanly from PyPI.

## Notes

- PyPI rejects re-uploads of an existing version. If `uv publish` fails because the version already exists, bump again rather than trying to overwrite.
- The GitHub Actions workflow at `.github/workflows/publish.yml` is currently commented out; publishing is manual. If you uncomment it later, remove this prompt or rewrite it to describe triggering the workflow instead.
- Do **not** skip the tag step — users and `git log --tags` rely on it to map a commit to a release.
- Never run `git push --force` on `main` or move a published tag.
