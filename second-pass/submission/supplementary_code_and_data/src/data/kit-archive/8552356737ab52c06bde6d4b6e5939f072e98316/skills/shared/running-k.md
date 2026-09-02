# Running the K tools

Use this reference for the shell setup, backend choice, build commands, and
success signals shared by the live skills.

## Shell setup

K installed through `kup` normally lives in `~/.nix-profile/bin`. Agent and
other non-interactive shells may not source the Nix profile automatically, so
start every shell session that calls a K tool with:

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
```

If a command is still missing, return to
[installing-k.md](../using-kit/references/installing-k.md).

## Backends

| Backend | Use |
|---|---|
| LLVM | Fast concrete execution with `krun` |
| Haskell | Concrete execution with `krun` and symbolic proof with `kprove` |

Compile a language semantics with LLVM and run a concrete program:

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
kompile --backend llvm semantics.k \
  --main-module SEMANTICS \
  --syntax-module SEMANTICS-SYNTAX \
  --output-definition semantics-kompiled

krun path/to/program --definition semantics-kompiled
```

Compare the final configuration with the expected result before using the
semantics in a specification. Choose the source path and module names that
match the definition being tested.

Compile the proof definition with the Haskell backend:

```bash
export PATH="$HOME/.nix-profile/bin:$PATH"
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module SEMANTICS-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The `--definition` argument names the kompiled directory, not a `.k` source
file. Pass `--syntax-module` when the desired syntax module is not
`<main-module>-SYNTAX`; otherwise `kompile` may infer the wrong module.

## Reading the result

A successful `kprove` run prints:

```text
#Top
```

and exits with status 0. `#Top` is the complete success signal from the
`kprove` binary; output formats from higher-level drivers may differ.

A stuck reachability claim exits non-zero and normally includes
`WarnStuckClaimState` plus a residual configuration. Other failures, such as
parse or backend errors, have different diagnostics—read the actual exit status
and message rather than treating every non-zero result as a stuck claim.

## Diagnostic entry points

- `--dry-run` compiles the program to KORE without running the proof. Use it to
  separate parsing/compilation failures from proof failures.
- `--claims MODULE.label` and `--exclude MODULE.label` select claims. See
  [k-claims.md](k-claims.md#claim-labels) for the two label forms.
- `--depth N` bounds computational proof steps. Use it diagnostically and
  compare residual configurations; see
  [the kprove troubleshooting index](kprove-debug-troubleshoot/index.md).

Run `kprove --help` against the installed toolchain before relying on an
unfamiliar flag.
