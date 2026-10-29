# Contributing to Le Petit Atelier

Thank you for looking. Every repo here is one project of an open workshop in Akaroa, New Zealand.

- **Questions, ideas, a build of your own:** open an issue in the project's repo and pick the form that fits (something
  is wrong, an idea, I built this, a question), or write to bonjour@lepetitatelier.nz. A person reads every issue,
  usually within a week; safety reports first.
- **Changes:** fork, branch, pull request. Say what you changed and why, in plain language. Automatic checks run on
  every pull request: big files (STL, STEP, 3MF, images, PDFs) must go through [Git LFS](https://git-lfs.com), and
  links between files must work. If a check fails, its message says how to fix it.
- **Third-party designs** stay pristine in `upstream/`; changes go in `mods/` and are listed in `IMPROVEMENTS.md`.
- **Licences:** each repo states its own (usually CERN-OHL-S v2 for hardware, CC BY-SA 4.0 for docs, GPL-3.0 or MIT for
  firmware). By contributing you agree your work is published under the same licence.
- **Never commit** secrets, personal details, or photos of people without their consent.
- **Be kind:** [how we behave](CODE_OF_CONDUCT.md). Security or safety problem: [SECURITY.md](SECURITY.md).

## For the team: how the automation works

| What | Where |
|---|---|
| Issue forms, pull request checklist, code of conduct, security, support | this repo, `.github/` and root: GitHub uses them for every repo that has none of its own |
| Triage: shared labels, type and `safety` labels, labels from the files a PR touches, welcome for newcomers | `.github/workflows/triage.yml`, called by each repo's `.github/workflows/community.yml` |
| PR checks: Git LFS and broken links | `.github/workflows/pr-checks.yml` running `tools/pr_checks.py` (run it locally: `python3 tools/pr_checks.py origin/main`) |
| Labels | `labels.tsv`; `tools/sync-labels.sh` pushes them to every repo (new repos also get them on their first issue) |
| Library updates | each repo's `.github/dependabot.yml`: monthly, grouped; security fixes as soon as they're known |
| New repo | from [project-template](https://github.com/lepetitatelier/project-template): it already has `community.yml` and `dependabot.yml` |

Everything new and open: [issues needing a look](https://github.com/issues?q=org%3Alepetitatelier+is%3Aopen+label%3Aneeds-triage)
· [open pull requests](https://github.com/pulls?q=org%3Alepetitatelier+is%3Aopen+is%3Apr) · [safety](https://github.com/issues?q=org%3Alepetitatelier+is%3Aopen+label%3Asafety).
