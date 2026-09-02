# Is the `#ret`/`#pop` split necessary? — no, it buys a *local* loop invariant, not provability

This folder is a self-contained probe, same shape as [`../lstack-probe`](../lstack-probe/INVESTIGATION.md).
Every claim below is in a `.k` file here; the results reproduce by `kompile`-ing the two
semantics once and running `kprove` on each `spec-*.k`.

```sh
cd verification/humaneval/reference/notes/ret-probe
kompile verif-split.k    --backend haskell --main-module RET --syntax-module RET --output-definition vs-kompiled
kompile verif-combined.k --backend haskell --main-module RET --syntax-module RET --output-definition vc-kompiled
# then, capped (see memory cap-kprove-memory):
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 600 kprove spec-combined.k --definition vc-kompiled --spec-module COMBINED-SPEC --depth 2000
```

## The question

The real semantics returns from a function in **two** steps (see
[`../../src/mpy-functions.k`](../../src/mpy-functions.k)):

```k
rule <k> V:Val ~> #ret ~> _ => #pop </k>             // #ret: stash the value, DISCARD the frame body (~> _)
     <ret> noRet => retV(V) </ret>
rule <k> #pop => V ~> CONT </k>                        // #pop: restore the caller frame (reads <stack>)
     <ret>   retV(V) => noRet </ret>
     <stack> ListItem(frame(CONT:K, _)) => .List ... </stack>
```

Earlier I justified the split by appealing to *locality*: I claimed a **combined** one-step
return — `ret(V) ~> _ => V ~> CONT` popping the caller frame directly — would *jam* kprove,
because the loop invariant would then have to mention the **symbolic `<stack>`** and the prover
chokes on it. The user pushed back: *"if we wrote the claim a particular way, that would still be
doable without the `#ret ~> #pop` thing?"* This probe checks exactly that, the same way the
lstack one did.

## The setup — one early-return-from-loop, two return models

[`verif-split.k`](verif-split.k) and [`verif-combined.k`](verif-combined.k) are **identical**
except for how `ret` returns. The program is the smallest thing that returns *out of the middle of
a loop*: `callAny(S)` pushes a caller frame and runs `loop(S) ~> endcall`; `loop` walks the list
and **early-returns `ret(1)`** at the first positive element, otherwise recurses, otherwise (empty)
falls through to `endcall` which returns `0`. The summary is `anyPos(S)` — `1` if any element is
positive, else `0` — declared `[function, total]`.

- **split** ([`verif-split.k`](verif-split.k)): `ret(V) ~> _ => #pop` (stash in `<ret>`), then a
  separate `#pop => V ~> CONT` pops `<stack>`.
- **combined** ([`verif-combined.k`](verif-combined.k)): `ret(V) ~> _ => V ~> CONT` pops `<stack>`
  in a single rule — no `#pop`, no `<ret>`.

## The experiments (this IS the table, and where it comes from)

Each row is one `spec-*.k` file; "result" is `kprove ... | grep -c '^#Top'`, saved next to it.

| # | file | return model | loop invariant reduces to… | names `<stack>`? | result |
| --- | --- | --- | --- | --- | --- |
| 1 | [`spec-split.k`](spec-split.k) | split | `#pop`, value in `<ret>` | **no** | **#Top** ([out](split-local.out)) |
| 2 | [`spec-split2.k`](spec-split2.k) | split | `anyPos(S) ~> CONT` (pops frame) | yes | **#Top** ([out](split-popping.out)) |
| 3 | [`spec-combined.k`](spec-combined.k) | **combined** | `anyPos(S) ~> CONT` (pops frame) | yes | **#Top** ([out](combined.out)) |

Read the rows:

- **Row 3 is the answer.** The combined one-step return — the formulation I claimed "jams on the
  symbolic stack" — **proves**, with a loop invariant that pops `frame(CONT)` off a *symbolic*
  `<stack>` (`CONT` a variable, plus a symbolic tail `...`). So "combined jams" was **false**, the
  same category of mistake as ["the side cell jams on counters"](../lstack-probe/INVESTIGATION.md).
- **Row 1 vs Row 2** shows what the split actually buys. With the split you *may* write the loop
  invariant **local**: `#loop(...) ~> #endcall => #pop`, touching only `<k>` and `<ret>`, never
  naming `<stack>` (row 1). Or you may write it stack-popping (row 2). Both prove. The combined
  model has only the stack-popping option (row 3) — there is no `#pop` marker to stop at.

So the split is a **modularity convenience, not a provability requirement**. All three close.

## What the split actually buys — and what it doesn't

The kernel of truth in "locality": with the split, the **loop invariant is stack-agnostic.** It
ends at the `#pop` *marker* and stashes the result in `<ret>`; it says nothing about `<stack>`,
`frame`, or the caller's continuation `CONT`. The frame restore is one extra rewrite (`#pop`)
that the **entry** claim discharges, where the stack is **concrete** (`.List` with one known
frame). This is the 3-below-zero shape and every proof in this repo uses it.

What is *not* true is the strong form I asserted — that the combined return is unprovable or that
it "jams." Row 3 refutes it directly. A frame-popping invariant over a symbolic `<stack>` is
perfectly within kprove's reach: matching `ListItem(frame(CONT:K)) => .List ...` against a
symbolic stack binds `CONT` and the tail as ordinary unification variables; no decision procedure
is forced, nothing is undefined, nothing stalls.

## The probe bug that nearly produced a third wrong "why"

The split spec *first* failed — and the failure looked deep: the reached state was
`<k> #pop ~> _DotVar2 ... </k>` and the refuted side-condition was `#Not(_DotVar1 #Equals
_DotVar3)`, two anonymous K-cell-tail variables. It was tempting to spin a story about "the split
leaks a stray continuation." The real cause was a **one-token bug in the probe**: I had written

```k
rule <k> ret(V:Int) ~> _ => #pop ... </k>     // WRONG: ~> _ AND a trailing ...
```

The real rule has **no** trailing `...` (`V:Val ~> #ret ~> _ => #pop`). With *both* `~> _` and
`...`, K can no longer read `_` as "the whole rest of the computation" — it demotes `_` to a
single `KItem` and lets `...` capture a separate tail variable. That tail (`_DotVar2`) is pure
noise the early-return path then fails to discharge in the circularity. Deleting the `...` — making
the probe match the real semantics — flips row 1 from FAIL to **#Top**. The lesson is the lstack
lesson again: *a proof that fails for a formulation reason looks exactly like a deep obstruction;
always reduce to a probe that matches the real rules before believing the "why."*

## Bottom line

The `#ret`/`#pop` split is **not** required for the early-return-from-loop proof to go through —
the combined one-step return proves with a stack-popping loop invariant
([`spec-combined.k`](spec-combined.k), #Top). What the split genuinely provides is a **local,
stack-agnostic loop invariant** (reduce to the `#pop` marker, value in `<ret>`, frame restored
later by the entry where the stack is concrete) — cleaner and the reason the real semantics keeps
it, but a convenience, not a necessity.

> A return can pop the caller frame in one rule or in two; both prove. The two-step `#ret`/`#pop`
> split exists so the **loop invariant never has to mention `<stack>`**, not because a one-step
> return is unprovable.
