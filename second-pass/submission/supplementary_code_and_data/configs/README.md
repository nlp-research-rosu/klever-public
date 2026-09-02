# Pinned configuration (reviewer-facing copies)

These files pin every tool, prompt, skill-bundle, toolchain, and
audit-campaign version used by the pipeline. They are exact copies of the
files at `src/data/` (where the runners read them); they are duplicated
here so the pinned configuration is visible in one place.

- `klean-toolchain.lock.json` — K framework, pyk/Klean, Lean 4, and Codex
  CLI versions (commit-pinned).
- `klean-audit-tools.lock.json` — SHA-256 hashes of the stage-4/6
  mechanical tool bundle (verify with
  `python3 docker/klean-audit/check_tool_bundle.py --root . --lock
  data/klean-audit-tools.lock.json` from `src/`).
- `audit-campaign.lock.json` — the stage-2 audit campaign pin (audit
  prompt hash, audit image, toolchain versions).
- `kit-skills.lock.json` / `audit-kit-skills.lock.json` — hashes of the
  vendored skill bundles at `src/data/skills/` and
  `src/data/audit-skills/`. (The `source_repository` field is anonymized
  for double-blind review.)
- `humaneval-prompts.lock.json` — hashes of the task inputs at
  `src/data/questions/`.

The frozen K reference semantics itself is at `src/data/reference/src`,
described by `src/data/reference-semantics.md`.
