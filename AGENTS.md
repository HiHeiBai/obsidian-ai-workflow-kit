# Repository Agent Entry

## Deploying for a user

If the user asks to deploy, install, or start using this knowledge vault, read [AI_DEPLOY.md](AI_DEPLOY.md) and follow that workflow. Complete the deployment in a persistent user directory; do not treat a request to use this repository as a request to develop it. New deployments default to the complete Chinese vault.

## Maintaining this repository

- `kit/` is the ready-to-open Chinese vault delivered to users. Its six functional directories and homepage must match the Chinese full installation.
- Maintained templates and runtime live in `src/`. Read `src/00-AI/AGENTS.md` and `docs/release/source-sync-policy.md` for workflow and ownership rules.
- Change templates in `src/`, then run `python3 scripts/build_kit.py`. Do not independently maintain generated `kit/` files.
- Use `python3 src/00-AI/scripts/kb.py` for source commands. Installed CLI paths remain unchanged.
- Run CI checks from `.github/workflows/ci.yml`, including `python3 scripts/build_kit.py --check`, both languages and install modes, and legacy upgrades.
- Repository-root files are developer resources. Only the contents of `kit/` belong in a new Chinese user vault.
