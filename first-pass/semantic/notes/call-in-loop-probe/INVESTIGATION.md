# Probe A: call-in-loop proof (de-escape rework Task 3)

## Question

Can a REAL user-function call inside a loop body be proven on the unified
semantics with no interception — the historical reason for every
`trusted-callable-interception` trap? Before frame deallocation the answer
was no: each iteration allocated a fresh callee frame and bumped
`scopeLoc`, so the loop invariant's configuration changed shape every
iteration and the circularity never re-applied.

## Probe

`probe.py`: `digsum(k)` (its own numeric while-loop) called from
`total_digsum(n)`'s range-loop — the is_prime shape in miniature.
CPython-checked; krun exit-code 0 with `scopeLoc` wound back to 1 and only
builtins + module scope left (deallocation observed concretely).

## Result: GREEN (first attempt)

`kprove spec.k` → `#Top`, all three claims, no interceptions, no
problem-local rules beyond the two defined summaries (`digAcc`, `tdFold`).

## The template (reused by P10, P32, P39, P59, P94, P107, P108, P145)

1. **Claim 1 — callee loop invariant, FRAMED**: `#while(...)` over
   `<env> L:Int` with `... L |-> (scope(...) => scope(...)) ...` map
   framing and only `<exc>`/`<exit-code>` pinned. Because it is framed
   over any loc and any surrounding map, it fires as a circularity INSIDE
   claim 2's proof, in the callee frame claim 2's call allocates. The
   frame scope lists EXACTLY the callee's live vars (`k`, `s`).
2. **Claim 2 — outer loop invariant, FIXED SHAPE (the load-bearing
   claim)**: `#loop(rangeObj(I, N, 1), Name("i"), ...real
   Call(Name("digsum"), Name("i"))...)` with the ENTIRE `<scopes>` map
   concrete-keyed (`-1` builtins, `0` module scope holding the CONCRETE
   `closureVal` of the callee, `1` the caller frame) and
   `<scopeLoc>` PINNED at 2. Each iteration allocates the callee frame at
   exactly loc 2; `#pop` deletes it (`SC [ 2 <- undef ]` reduces on the
   concrete key) and winds `scopeLoc` back to 2, restoring the claim's
   exact configuration — the circularity re-applies. `<ret> noRet` and
   `<stack> _STK` are restored by `#pop` too.
3. **Claim 3 — entry**: the module program verbatim; the two `FuncDef`s
   build the closures, the call to `total_digsum` allocates frame 1, and
   claim 2 folds the loop; the outer `#pop` deallocates frame 1, leaving
   `out <- tdFold(0, N, 0)` at `<scopeLoc> 1`.

## Why fixed shape (not framed) for claim 2

The callee frame's loc must be CONCRETE. With a framed/abstract scopes
map, allocation happens at a symbolic loc and `SC [ L <- undef ]` cannot
reduce (the matcher cannot decide aliasing against the abstracted rest of
the map) — the proof sticks at `#bindP`/`#pop`. This is the same lesson
as the Task 2 migration: claims pin `<scopeLoc>` (it is an invariant of
any balanced execution now), which makes every allocation loc concrete.

## Summary-shape notes

- `digAcc` uses the reference's pyMod-based `//` and `%` forms — the
  summary atoms must match the semantics' arithmetic atoms syntactically.
- `tdFold`'s step adds `digAcc(I, 0)` — exactly the value claim 1 leaves
  in `s` and `Return` propagates; no bridging lemma needed.
- Both summaries `[function, total]` (they land in scope maps) with
  guarded `[simplification]` rules (base `I >=Int N`, step `I <Int N`).
