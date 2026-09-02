# Can an Int-refined list sort (`LS:List{Int}`) replace `projectIntTotal`?

The idea (Xiaohong): instead of `VS:ValSeq` + `requires allInt(VS)` + the `projectIntTotal` cast
layer, bind the payload at an Int-refined list sort in the place where a `Val` list is expected,
so every element is `Int` *by sort*. **Verdict: expressible and provable in one specific encoding
(explicit overloads + head-exposed invariants), but adopting it breaks the existing bare-`ValSeq`
proof style — an all-or-nothing migration. Keep `projectIntTotal` for pass-0.** The two prover
gaps to raise with RV are at the bottom.

```sh
cd verification/humaneval/reference/notes/klist-probe
kompile verif-<leg>.k --backend haskell --main-module VERIF-<LEG> --syntax-module VERIF-<LEG> --output-definition verif-<leg>-kompiled
systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
  timeout 500 kprove spec-<row>.k --definition verif-<leg>-kompiled --spec-module <ROW>-SPEC --depth 2000
```

All results below are `kprove … | grep -c '^#Top'`, saved as `<row>.out`. Every row terminates in
seconds. Prover = kprove's legacy kore-exec pipeline, K v7.1.293.

## Why a plain subsort is not enough — the mechanism

The "simple" declaration kompiles ([`verif-subsort.k`](verif-subsort.k)):

```k
syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
syntax IntVs  ::= ".IntVs"  | vCons(Int, IntVs)
syntax ValSeq ::= IntVs
```

but `syntax ValSeq ::= IntVs` only introduces an injection `inj : IntVs → ValSeq` with **no other
properties**. `inj(.IntVs)` and `.ValSeq` are then two *different* empty lists, and every all-int
list exists twice — the model gains a disjoint copy of the refined lists (junk). Both directions
die, verified:

- a claim binding `IS:IntVs` is stuck at step 0 with **zero** branches — no rule (not even nil)
  relates to the foreign injected value ([refined-subsort](refined-subsort.out));
- the ordinary bare `VS:ValSeq` claim **also breaks** the moment the subsort merely exists:
  narrowing `VS` now leaves an uncovered third branch `VS = inj(IntVs)`
  ([len-subsort](len-subsort.out) vs [len-plain](len-plain.out), identical claim, `#Top` on the
  subsort-free [`verif-plain.k`](verif-plain.k)).

`[overload(_)]` on both cons and both nil productions is what *identifies the copies*: kompile
emits the equations

```
inj{IntVs,ValSeq}(.IntVs)          =  .ValSeq
inj{IntVs,ValSeq}(vCons(I, IS))    =  vCons(inj(I), inj(IS))
```

(Maude-style subsort overloading: the same constructor at two levels of precision — one value,
two typings). That makes `IS:IntVs` in a `ValSeq` position mean "the same list, statically known
all-int" — the intended semantics. The implementation detail with consequences: to orient the
equations, kompile keeps the **refined** side as `constructor`s and **demotes the super-sort
cons/nil to `anywhere` symbols** (the canonical form of an all-int list is the injected refined
term). Visible in `verif-overload-kompiled/definition.kore`: `vCons{IntVs}` is
`[constructor]`, `vCons{ValSeq}` is `[anywhere]` + a `symbol-overload` axiom.

## The rows

Working encoding: [`verif-overload.k`](verif-overload.k) — both flavors (user-list `Vals`/`Ints`
and reference-shaped `vCons` `ValSeq`/`IntVs`), **no cast layer at all** (no `projectIntTotal`,
no `#Ceil` lemma, no `allInt`; `applyBin`/`applyCmp` match `Int` only).

| row | claim shape | result |
| --- | --- | --- |
| [bare-refined](spec-bare-refined.k) | bare `IS:Ints` (what you'd naturally write) | **FAIL** — nil discharges as an equation; rule application never case-splits the injected variable against the cons |
| [bare-refined-lbl](spec-bare-refined-lbl.k) | same, behind one neutral step so the circularity can never re-apply | **FAIL** — pins the wall on *rule* application, not a step-0 artifact |
| [headexposed-branch](spec-headexposed-branch.k) | head-exposed `(I:Int, IS:Ints)`, loop-**break** on `x<0` | **#Top** — claim application *does* narrow the injected tail; the break test is `I <Int 0`, decidable with no cast |
| [entry-invariant](spec-entry-invariant.k) | production shape on the `vCons` flavor: bare-variable entry + head-exposed invariant as sibling claims | **#Top** — corrupting the postcondition `+Int 1` fails (non-vacuous) |
| [len-plain](spec-len-plain.k) | cast-free length loop, bare `VS:ValSeq`, subsort-free definition | **#Top** — today's production idiom |
| [len-subsort](spec-len-subsort.k) | same claim, subsort merely declared (no overloads) | **FAIL** — uncovered `VS = inj(IntVs)` branch |
| [len-overload](spec-len-overload.k) | same claim, overloaded definition | **FAIL** — `anywhere`-demotion loses exhaustiveness; stuck on the semantically-empty "not nil, not any cons" remainder |
| [refined-subsort](spec-refined-subsort.k) | `IS:IntVs` on the subsort-only definition | **FAIL** — stuck at step 0, zero branches (disjoint copy) |
| [userlist-headexposed](spec-userlist-headexposed.k) | user lists + subsort, no overload tags | **PARSE ERROR** — sub/super cons pair is a genuine ambiguity; resolving it is the overload tag's job |

The len-* triple is the load-bearing differential: one cast-free claim, three definitions
(plain / +subsort / +subsort+overload), results `#Top` / FAIL / FAIL. **Any** introduction of the
refined sort into the shared semantics — with or without overloads — breaks the bare-`VS:ValSeq`
claims every existing proof uses.

## Dead ends for the ideal notation (`list(VS:ValList{Int})`)

- [`verif-parametric.k`](verif-parametric.k): user-defined parametric sorts —
  `[Error] Compiler: User-defined parametric sorts are currently unsupported: ValList{S}`.
  Same expected-error in K's own regression test (`checks/checkParametricSort.k`), still on
  upstream master (v7.1.337, 2026-07). The manual's "parametric productions" (`syntax {Sort} …`)
  are per-use polymorphic operators (`#if`, `#fun`, brackets), not sort families; the only real
  parametric sort is the special-cased hooked `MInt{Width}` (numeral params, llvm-hooked, each
  instance needs a bare `syntax MInt{64}` declaration).
- [`verif-hooked.k`](verif-hooked.k): domains.md's hooked `List` stamped out at two element sorts
  (wasm-semantics `ListInt [hook(LIST.List)]` is the precedent) + the subsort between them —
  `[Error] Compiler: Cannot add new constructors to hooked sort ListVal`. Hooked sorts cannot
  participate in subsorting; the builtin List can never resolve an element-refined subsort.
- Anonymous in-place `List{Val}` as a production argument: `Could not find sorts: [List{Val}]`.
- Ecosystem data: zero user-defined parametric sorts across all 112 checked-out k-repos.

## Where `projectIntTotal` came from, and what that repo does

Our cast layer is copied (down to the symbol name) from RV's **kasmer-multiversx**:
`kmxwasm/src/kmxwasm/kdist/mxwasm-semantics/ceils-syntax.k` + `ceils.k`. In the big picture that
file is a systematic **totalization layer** covering every partial operation their proofs touch —
`substrBytes`, `replaceAtBytes`, padding, `div/mod/shl/shr/pow/log2`, map lookup, list indexing
(`#getIntsTotal(Ints, Int)`), and the sort projections `projectIntTotal`/`projectBytesTotal`.
The pattern per operation: a `definedX(…)` total Boolean (the definedness domain), an abstract
twin `XTotal [function, total, no-evaluators]` (often smtlib-hooked), a
`#Ceil(X(…)) => definedX(…) #And …` simplification, and `X ⇄ XTotal` bridge rules. Notably they
have a user-list `Ints` and still access it through totalized accessors — RV's own production
verification on current K uses the cast-layer architecture, not sort refinement. Our `lemmas.k`
is a small faithful instance of that design.

## Bottom line

The refinement idea *can* be made to work on this K version — explicit `[overload]` tags + the
subsort + head-exposed invariants (claim application narrows the injected variable; rule
application does not) — and in that shape it deletes the whole per-problem cast layer, branches
included. But the tags demote the super-sort constructors, and even the bare subsort poisons the
sort's inhabitants, so **either** form of the declaration breaks the existing bare-`VS:ValSeq`
claims (len-* differential). On today's prover this is a full-corpus migration plus llvm/krun
revalidation, for a notation win — while the cast layer is also what RV itself ships. Keep
`projectIntTotal`; the enablers worth raising with RV: (1) narrowing of injected variables
against overloaded constructors during *rule* application, (2) exhaustiveness / remainder
discharge modulo overloads (and modulo plain subsort injections).
