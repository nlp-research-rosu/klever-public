VALIDATED

## What is proven

Under the supplied `MPY` semantics, loading the translated `encode` definition
into a fresh module scope and calling it on any modeled string `str(CS)`
terminates at the claim's destination with:

```k
str(
  replaceC(
    replaceC(
      replaceC(
        replaceC(
          replaceC(
            replaceC(
              replaceC(
                replaceC(
                  replaceC(
                    replaceC(mapSwap(CS), 97, 99),
                    101, 103),
                  105, 107),
                111, 113),
              117, 119),
            65, 67),
          69, 71),
        73, 75),
      79, 81),
    85, 87))
```

The claim also fixes the normal final control state: environment `0`, module
binding installed, scope location `1`, empty heap and stack, `noRet`, `NoExc`,
and exit code `0`. This is a partial-correctness result in the Kit sense.

For ASCII English letters, `mapSwap` changes lowercase to uppercase and
uppercase to lowercase. The ten `replaceC` applications then implement
`a/e/i/o/u -> c/g/k/q/w` in each case. Their replacement characters are all
consonants, so later replacements cannot shift a character twice. Thus:

- lowercase vowels become `C/G/K/Q/W`;
- uppercase vowels become `c/g/k/q/w`;
- consonants only change case;
- spaces and other non-letter ASCII characters are unchanged.

This is the prompt's requested operation and agrees with both prompt examples.

## Formal claim

`SPEC.encode` in `spec.k` has no precondition. Its program boundary includes:

1. `#loadAll` of the exact translated `FuncDef`;
2. installation of `encode` in the module scope;
3. ordinary lookup of `Name("encode")`;
4. argument binding, execution of the complete function body, return, and
   frame restoration.

The result and every reference-semantics configuration cell are constrained on
the destination. There are no source loops, so no circularity or loop-invariant
claim is required.

`solution.mpy` has SHA-256
`fc50d53a7c774d8a12149ad71f3ab5988849f3623c8c83d72d4ed772e3c8f630`.
`prove.sh` regenerates it and rejects a different term before building either
backend. The exact `FuncDef` was structurally audited against the term embedded
in `spec.k`.

## Proof-extension inventory

There are no proof-local extensions.

- `verification.k` only requires the supplied
  `reference-semantics/semantics.k` and imports `MPY`.
- It declares no syntax, functions, totality attributes, equations,
  simplification rules, ordinary rewrites, priorities, concrete rules,
  operational bridges, trusted primitives, or auxiliary claims.
- `spec.k` contains only the target reachability claim.
- `mapSwap` and `replaceC` are definitions in the fixed supplied semantics,
  not proof-local summaries. The program reaches them through the semantics'
  normal method-call, function-call, binding, and return rules.

Consequently, the proof-extension contract has no extension rows to classify,
and the operational-bridge context and result-bearing-abstraction procedures
are not applicable.

## Reproduction commands and actual outputs

The complete executed command sequence is in `prove.sh`; its combined output is
preserved in `prove-run.log`.

Translation and identity:

```bash
python3 py2mpy.py solution.py > solution.mpy
sha256sum solution.mpy
```

Actual result: exit `0`; SHA-256
`fc50d53a7c774d8a12149ad71f3ab5988849f3623c8c83d72d4ed772e3c8f630`.
The AST comparison between `solution.py` and the function copied into
`smoke.py` printed:

```text
smoke-function-identity: PASS
```

Independent differential check:

```bash
python3 differential.py
```

Actual output and exit:

```text
differential: checked=151742 mismatches=0
Exit: 0
```

Concrete LLVM build and execution:

```bash
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual result: both commands exited `0`. `kompile` emitted warnings from the
unchanged supplied semantics. `krun` ended with:

```text
<k> .K </k>
<heap> .Map </heap>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

Symbolic Haskell build and positive proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result:

```text
kompile exit: 0
kprove output: #Top
kprove exit: 0
```

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, with `WarnStuckClaimState`. The residual in
`vacuity.log` requires equality between the correct final
`replaceC(..., 85, 87)` and the deliberately false
`replaceC(..., 85, 88)`.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1`, with `WarnStuckClaimState`. The mutation changes the
body's final `.replace("U", "W")` to `.replace("U", "X")` in both exact body
occurrences while leaving the original postcondition unchanged. The residual
shows the computed final `replaceC(..., 85, 88)` cannot establish the required
`replaceC(..., 85, 87)`.

The complete runner invocation:

```bash
./prove.sh
```

Actual result: exit `0`, one positive `#Top`, vacuity mutation exit `1`, and
body mutation exit `1`.

## Gate results

### Gate A — PASS

- A1: The exact program-defined body executes through fixed semantics. The
  translated term is hash-pinned, ordinary binding and lookup are exercised,
  and the material body mutation is rejected.
- A2: No execution is skipped by a proof bridge. The claim constrains the
  result plus environment, scopes, allocation counters, heap, stack, return,
  exception, and exit-code cells.
- A3: Fixed semantics performs receiver evaluation, left-to-right argument
  evaluation, method binding, function binding, return, and frame restoration.
  There is no bridge whose match context could be wider than its justification.
- A4: No proof-local equations or total functions were introduced. Therefore
  there are no new guards, overlap, descent, or totalization obligations.
- A5: The precondition is `true`; for example,
  `CS = iCons(117, .IntSeq)` is realizable and distinguishes final code `87`
  (`W`) from the false code `88` (`X`). The false-postcondition probe exits `1`
  with the expected equality residual.

### Gate B — PASS

- B1: The formal domain is all `IntSeq` string values and therefore does not
  strengthen the prompt's English-letter domain. It also covers spaces, as
  required by the second example.
- B2: The supplied string semantics is ASCII-based. That matches the prompt's
  English-alphabet scope. Python Unicode case behavior is explicitly excluded.
- B3: The postcondition directly uses the fixed semantics' exhaustive
  structural `mapSwap` and `replaceC` equations. The mapping-to-contract
  argument above is equation-level, and independent finite evidence is
  recorded separately rather than presented as a universal proof.
- B4: The implementation, formal claim, and prompt examples agree.

### Gate C — PASS

- C1: The trust ledger below names every unproved boundary and its influence.
  No proof-local opaque or trusted value affects the theorem.
- C2: All claimed tests, mutations, commands, outputs, hashes, and logs exist
  in the current directory and are reproduced by `prove.sh`.
- C3: The K result, conditional trust, empirical evidence, and excluded
  behavior are stated separately.

## Trust boundary

| Component | Status and influence | Dependents | Evidence |
|---|---|---|---|
| K v7.1.293 Haskell reachability engine | Trusted proof checker; affects the universal result | `SPEC.encode` | `#Top`, exit `0` |
| Supplied `MPY` semantics | Fixed trusted execution model; affects value, binding, control, state, and exceptions | all claims and `krun` | untouched source, successful LLVM/Haskell builds, concrete checks |
| `py2mpy.py` and source-to-term correspondence | Outside the K theorem; affects which source AST is claimed | identification of `solution.py` with the embedded program | regeneration, pinned `solution.mpy` hash, AST identity check, body mutation |
| CPython and `differential.py` oracle | Empirical adequacy evidence only; does not close the K proof | Gate B/C evidence | 151,742 checked messages, zero mismatches |

The imported semantics contains opaque facilities for unrelated operations such
as floats, sorting, and MD5. Dependency inspection of `verification.k` and
`spec.k` shows that this program invokes none of them.

## Empirically supported facts

`smoke.py` checks five cases under CPython and the LLVM semantics: the two
prompt examples, all ten vowels in both cases, consonants plus a space, and the
empty string. The K run reaches `.K` with `NoExc` and exit code `0`.

`differential.py` uses an independently written per-character `ord`/`chr`
oracle rather than the proof's nested replacement expression. It exhaustively
checks all messages of lengths zero through three over the 52 ASCII letters
plus space, then checks both prompt examples: 151,742 inputs and zero
mismatches. This is finite validation evidence, not a replacement for the
universal K proof.

## Excluded behavior

- Total correctness or an independent termination theorem is not claimed.
- CPython Unicode case mappings and non-ASCII text are outside the supplied
  ASCII string model.
- Non-string arguments, Python exceptions outside the modeled path, I/O,
  concurrency, and external state are outside the prompt and formal claim.
- Correctness of K itself, the supplied reference semantics, and the
  translator is trusted rather than proved here.
- The negative mutation probes demonstrate discrimination; they are not
  positive target proofs.
