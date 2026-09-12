# Repository Agent Entry

This is the source repository, not an installed Obsidian vault.

- Installable vault templates and runtime: `kit/`.
- Read `kit/00-AI/AGENTS.md` for workflow rules and `docs/release/source-sync-policy.md` for ownership boundaries. Paths in vault rules are relative to the installed vault.
- Run source commands with `python3 kit/00-AI/scripts/kb.py`.
- Verify changes with the CI commands in `.github/workflows/ci.yml`, including both languages and install modes.
- Keep repository-only documentation, tests, and installation tooling out of installed vaults.
