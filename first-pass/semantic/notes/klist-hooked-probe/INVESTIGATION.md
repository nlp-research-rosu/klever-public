# Can K's BUILTIN hooked `List` replace our hand-rolled `ValSeq`?

Question (user, 2026-07-11): we hand-rolled `ValSeq` and keep writing concat lemmas for it
(assoc/unit, the "iCons things", now shared in `lemmas/list.k`) — would the builtin `List` give
us those for free from the standard library? **Verdict: NO for the corpus. The stdlib ships
ZERO List simplification rules; the prover performs no constructor narrowing on hooked Lists
(kills the for-each genre); the casts.k trick itself DOES transplant to index-style access
(idx2 #Top) but the declare-then-guard domain discipline diverges on it (idx3 timeout). Keep
`ValSeq`; the handful of shared concat lemmas is the entire price of an inductable container.**

(The earlier `notes/klist-probe` answered a different question — element-SORT refinement and
hooked-List subsorting, both dead ends. This probe uses the builtin `List` directly, elements
cast per-use, no subsorts.)

```sh
cd verification/humaneval/reference/notes/klist-hooked-probe
kompile verif-klist.k --backend haskell --main-module VERIF-KLIST --syntax-module VERIF-KLIST --output-definition verif-klist-kompiled
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 500 kprove spec-<leg>.k --definition verif-klist-kompiled --spec-module SPEC-<LEG>-SPEC --depth 2000
```

## What the standard library actually provides

Checked `include/kframework/builtin/domains.md` (K v7.1.x):

- **Map**: a rich `[simplification]` module (update/lookup/in_keys/#Ceil) — we already use it
  (`MAP-SYMBOLIC`).
- **Set**: a partial `SET-KORE-SYMBOLIC [symbolic,haskell]` module.
- **List: NOTHING.** Zero `[simplification]` rules. The symbolic story is only (a) the
  `assoc, unit(.List)` attributes on concat (builtin syntactic flattening) and (b)
  `smtlib(smt_seq_*)` tags that the current pipeline does not exploit.

## The legs

Round 1 — structural folds (the for-each genre):

| leg | claim shape | result | failure mode |
| --- | --- | --- | --- |
| [consume](spec-consume.k) | k-cell fold `#sum(L:List)` + circularity, summary `sumL` | **FAIL** | stuck at STEP 0 — a symbolic `L:List` never narrows against `ListItem(I) L'` / `.List`; no rule applies, zero branches |
| [build](spec-build.k) | append accumulation `<out> L => L ListItem(N) </out>`, summary `buildL(N)` | **FAIL** | flattening itself WORKS (stuck config displays flat `L ListItem(N) buildL(N -Int 1)`), but the final implication cannot fold `buildL(N)` inside the concat — target `L buildL(N)` never meets it |
| [cast](spec-cast.k) | Val elements, guarded `{V}:>Int` fold under `allIntL(L)` | **FAIL** | same step-0 narrowing wall as consume (the cast layer is never even reached) |

Round 2 — the user's actual question ([verif-klist-idx.k](verif-klist-idx.k)): a semantic List
OF VALS accessed by INDEX through a totalized `getTotal(L, I)` (the RV `#getIntsTotal` pattern)
plus `projectIntTotal` per element — the casts.k trick one level up, no container narrowing
(the circularity case-splits the INDEX against the opaque `size(L)`):

| leg | claim shape | result | reading |
| --- | --- | --- | --- |
| [idx](spec-idx.k) | first cut with `isInt(getTotal(L,I))` in the SEMANTICS rule guard | **FAIL** (design error) | a proof-layer predicate in a semantics guard stalls rule selection — remainder branch stuck; production never guards semantics on domain facts |
| [idx2](spec-idx2.k) | semantics reads `projectIntTotal(getTotal(L, I))` unconditionally; junk-tolerant summary `sumFrom`, no domain premise | **#Top** | THE TRICK TRANSPLANTS: totalized access + element cast + index-recursive summary all work on a symbolic builtin List |
| [idx3](spec-idx3.k) | declare-then-guard summary `sumFromG` + `allIntFrom(L, I)` premise (production style) | **TIMEOUT** (500s, no output) | the domain predicate cannot feed the guards efficiently: index-recursive `allIntFrom` has no structural anchor — on ValSeq, `allInt` unfolds exactly once per vCons narrowing; here its speculative unfolding (`I+k <Int size(L)` undecided) blows up |

Needed beyond stdlib for round 2: `size(L) >= 0` lemmas (stdlib lacks them), the `#Ceil(L[I])`
characterization (faithful to LIST.get's negative-index wrap), the two orientation bridges.

## The lemma ledger (what switching would actually eliminate vs add)

- ELIMINATED: the concat family — `lemmas/list.k` (3 rules) + `lemmas/str.k` (2) — one-line,
  one-time, already shared.
- KEPT (morphed): the element bridges (`lemmas/subscript.k`, keyed on getTotal instead of
  valSeqAt), the casts layer, sort-length.
- ADDED: size non-negativity, the getTotal cast layer, likely List-equality decomposition.
- LOST: the entire structural (for-each) proof genre — no narrowing (round 1) — plus the
  declare-then-guard discipline for index proofs (idx3). The 964 per-question structural
  summaries would all need index-style rewrites with a weaker (junk-tolerant) property form.

## Reading

- Our whole proof method — loop-invariant circularities discharged by structural narrowing
  (`VS = vCons(V, R)` / `.ValSeq` case-split) — has NO analog on the hooked List: the backend
  treats it as a normalized collection, not a free constructor sort, so there is no exhaustive
  split to offer the prover.
- The one thing the builtin would buy (assoc/unit flattening, i.e. deleting our two concat
  lemmas) is real but tiny — and the `build` leg shows even that path stalls at the
  implication stage when a recursive summary sits inside the concat.
- The element-level cast trick (`projectIntTotal` / `{V}:>Int` under `isInt`) is
  container-independent — it was never the blocker; the container's narrowing is.
- Consistent with the ecosystem: KEVM's WordStack etc. are hand-rolled cons lists for exactly
  this reason; RV's kasmer verification uses user lists + a totalization layer, not builtin
  Lists, for proof-side data.
