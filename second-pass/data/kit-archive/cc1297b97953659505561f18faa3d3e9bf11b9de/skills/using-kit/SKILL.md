---
name: using-kit
description: 'Use when starting any K-framework program-verification task — proving partial correctness, formalizing a language in K, writing K specs or proofs — or whenever unsure which kit skill applies.'
---

## What this kit proves

This kit proves **partial correctness**: if a program terminates and its
precondition holds, then its postcondition holds at termination.

`kprove` establishes reachability claims by symbolic execution. For a loop, an
invariant claim acts coinductively as a **circularity**: when execution returns
to a matching symbolic loop-head configuration, the prover may apply that claim
instead of unrolling the loop again.

Keep three activities distinct:

- **Verification** — `kprove` exits 0 and prints `#Top` under the supplied theory.
- **Soundness audit** — proof extensions genuinely describe the program and do
  not introduce inconsistent or execution-bypassing reasoning.
- **Validation** — theorem scope, non-vacuity, trust, and independent evidence
  support the intended property.

## Choose the execution path first

Live verification is the default. Use the on-paper fallback only when the user
explicitly requests it or the K toolchain cannot be made available.

Start by checking the general K installer and version manager:

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
command -v kup
```

If `kup` is available, stay on the live path. Install or repair the K package
with `kup install k` when necessary, then confirm the tools with
`kompile --version && kprove --version`. See
[installing-k.md](references/installing-k.md) for setup and
[running-k.md](../shared/running-k.md) for shell and backend commands.

If `kup` is unavailable but an independently installed K toolchain already
runs, stay on the live path. Otherwise offer installation first. Route to
`reasoning-on-paper` only when installation is declined, impossible, or the
user asked for that mode.

## Live workflow

```text
intent → code → semantics → spec → proof → #Top
      → extension audit → adequacy → non-vacuity → evidence → exact-status report

Gate A PASS → continue to adequacy, non-vacuity, evidence, and status
Gate A FAIL → remove/disable offending extension → proving-spec → rebuild → #Top → Gate A
```

The Gate A back-edge is internal iteration within the same agent invocation; it
is not a retry, resume, second prompt, or fresh attempt. Preserve the current
solution and proof artifacts, remove the unsound extension, and continue the
original one-shot workflow until Gate A passes or repair encounters an evidenced
hard blocker. Every Gate A failure takes this back-edge unless an enumerated,
evidenced hard blocker prevents further repair.

| Stage | Artifact | Skill |
|---|---|---|
| Model the program's language | `semantics.k` | `writing-semantics` |
| State the reachability property | `spec.k` | `writing-spec` |
| Make the claims close | `verification.k` and `#Top` | `proving-spec` |
| Check that the proof is honest and route Gate A failures back to construction | `PROOF.md` after status selection | `validating-proof` |

Use `k-proof-technique` when the hard part is deriving an invariant, summary
function, or proof obligation rather than running a pipeline stage.

## On-paper fallback

Use `reasoning-on-paper`. It produces `spec.k`, `verification.k`, and a
natural-language `REASONING.md` trace, all clearly marked `UNCHECKED`. It does
not create `semantics.k` and does not claim a machine-checked proof. On-paper
work inherits its proof-extension obligations through `k-proof-technique` while
remaining `UNCHECKED`.

## Shared references

- [K syntax and operational semantics](../shared/k-syntax.md)
- [K functions, claims, and proof modules](../shared/k-claims.md)
- [Proof-extension soundness contract](../shared/proof-extension-soundness.md)
- [Running the K tools](../shared/running-k.md)
