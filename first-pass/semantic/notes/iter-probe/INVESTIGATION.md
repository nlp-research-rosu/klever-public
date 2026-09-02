# iter-probe — when does kprove narrow a symbolic argument to evaluate an iterator step?

## Question

An iterator protocol `iterNext(iterable) => iterDone | iterYield(elem, rest)` can
unify the for-loop's per-kind (`list`/`tuple`/`str`/`rangeObj`) dispatch. A first
attempt wired it as a plain `[function]` and the loop proof went `#Top=0` (stuck).
Two questions:

1. **where / why** does the plain-function version stick?
2. **when does a function narrow a symbolic argument at all** — is it really "never",
   or does something (e.g. `[total]`) change it?

## Reproduce

Each variant is a self-contained semantics (`verif-<tag>.k`) + claim
(`spec-<tag>.k`); kprove is always capped (see memory `cap-kprove-memory`).
Results are the `spec-<tag>.out` files here.

```sh
cd verification/humaneval/reference/notes/iter-probe
for v in fn:FN rw:RW partial:PARTIAL total:TOTAL nest:NEST sum:SUM suml:SUML; do
  tag=${v%:*}; mod=${v#*:}
  kompile verif-$tag.k --backend haskell \
    --main-module ITER-$mod --syntax-module ITER-$mod --output-definition $tag-kompiled
  systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
    timeout 600 kprove spec-$tag.k --definition $tag-kompiled \
    --spec-module ITER-$mod-SPEC > spec-$tag.out 2>&1
done
```

## Setup — one-variable variants, same claim

Every variant proves the same thing: walk a symbolic list to completion.

```k
claim <k> #drive(<symbolic list>) => .K </k> [all-path]
```

| variant | iterator step | wiring | result |
|---|---|---|---|
| `fn`      | `iterNext(Val) [function]`        | nested as an argument `#step(iterNext(V))` | **STUCK** |
| `rw`      | `iterNext(Val)` `<k>`-cell rewrite | driven `iterNext(V) ~> #step`              | **`#Top`** |
| `partial` | `f(ValSeq) [function]`            | nested as an argument `#step(f(VS))`       | **STUCK** |
| `total`   | `f(ValSeq) [function, total]`     | nested as an argument `#step(f(VS))`       | **`#Top`** |
| `nest`    | `g(Iterable) [function, total]`   | `#step(g(wrap(VS)))` — reach `.K` only      | **`#Top`** |
| `sum`     | `g(Iterable) [function, total]`   | same, but claim asserts `acc == ssum(VS,_)` | **STUCK** |
| `suml`    | `sum` + inversion `[simplification]` lemmas | base lemma fires, step lemma can't  | **STUCK** |

`partial` vs `total` differ in **exactly one token** (`[function]` →
`[function, total]`) — that isolates the `[total]` marking. `fn` vs `partial`
differ only in the argument sort (`Val` + `list(..)` wrapper vs a bare `ValSeq`) —
that shows the sort/wrapper is **not** the cause.

## Answer 1 — where/why the plain `[function]` sticks (`spec-fn.out`, `spec-partial.out`)

kprove's own stuck node (partial variant; `fn` is identical shape):

```text
#Not ( #Exists _X . #Exists R . { f(VS) #Equals iYield(_X, R) } )
#And
#Not ( { iDone #Equals f(VS) } )
#And
  <k> #step( f(VS) ) ~> .K </k>
```

It sticks at the **first driver step**, before any iteration:

1. `f(VS)` is a **partial function on a symbolic argument** whose top constructor
   is a bare variable `VS`. kprove evaluates a `[function]` by **matching** its
   equations (`f(.ValSeq)` needs `.ValSeq`; `f(vCons(X,R))` needs `vCons(..)`). A
   variable matches neither, and — because the function is **not** known total —
   the backend leaves `f(VS)` **uninterpreted** (it may not assume the equations
   are exhaustive/defined, on pain of unsoundness).
2. That opaque term is now the argument of `#step`, whose rules want the
   constructors `iDone` / `iYield(_,_)`. The two `#Not{ … #Equals f(VS) }`
   conjuncts are kprove recording that the uninterpreted `f(VS)` is provably
   **distinct** from both — so no `#step` rule fires.
3. Dead end → `WarnStuckClaimState`.

## Answer 2 — when a function DOES narrow: `[total]` (`spec-total.out`)

Adding `[total]` (nothing else) flips STUCK → `#Top`. A **total** function is known
defined everywhere, so kprove will **reduce `f(VS)` by branching on its value** —
an `iDone` branch and an `iYield(_,_)` branch — enough to drive control flow: the
base branch closes, the step branch reaches `#drive(R)` and re-matches the
`[all-path]` circularity. So for *control flow*:

- a **partial `[function]`** on a bare-variable argument → opaque, **does not reduce** → stuck;
- a **`[total]` function** → kprove **branches on `f(VS)`'s value** to reduce it → proceeds;
- (a function also reduces on a symbolic argument whose **top constructor is
  already concrete**, e.g. `f(vCons(X,R))` with `X,R` symbolic — matching succeeds.)

But note the `[total]` case branches on the step *value*, keeping `VS` itself
symbolic (a value-constraint `f(VS) = iDone`), **not** substituting `VS`'s
structure — which is exactly the gap Answer 3 exposes.

Independently, a **`<k>`-cell rewrite** does substitute structure: reachability
applies rewrite rules by unification-with-branching, so `VS := .ValSeq` / `vCons`
everywhere in the state, regardless of totality.

## Answer 3 — `[total]` narrows the VALUE, not the STRUCTURE (`spec-nest.out`, `spec-sum.out`)

Tempting conclusion from `total`: put iterNext behind a dedicated `Iterable` sort
as `[function, total]`, and it would narrow `iterNext(list(VS))` even though
`iterNext` over `Val` can't be `[total]` (`Val` has non-iterables). The `nest`
variant seemed to confirm it: a `[total]` `g` over `Iterable` with the symbolic
seq nested under `wrap`, driven `#drive(wrap(VS)) => #step(g(wrap(VS)))`, proves
`#Top`.

**But `nest` is too weak** — its claim only reaches `.K` (control flow). A real
loop invariant asserts a *summary* over `VS` (e.g. `total == prefixSum(VS, B)`).
The `sum` variant adds exactly that (`acc == ssum(VS, A)`, `ssum` recursing on
`VS`) and it **STUCKS**, with the same shape the real loop-break failure has:

```text
{ iDone #Equals g(wrap(VS)) }          // base branch kept as a CONSTRAINT on g's value
#Not ( { A #Equals ssum(VS, A) } )     // ...VS still symbolic, so ssum(VS,A) won't reduce
```

(`ssum` is `[total]` here — matching the real `prefixSum` — so this residual is
the *pure* structural obligation. A partial `ssum` instead reports
`#Not ( #Ceil(ssum(VS,A)) #And { A #Equals ssum(VS,A) } )`: an extra
`#Ceil` **definedness** conjunct that is an artifact of the partial marking, not
the real failure. Either way the `A #Equals ssum(VS,A)` half is unprovable.)

So a `[total]` function narrows the **iterator step's value** (`g(wrap(VS)) =
iDone`) but does **not** substitute the **iterable's structure** (`VS = .ValSeq`) —
and to close the base branch kprove would have to *invert* `g(wrap(VS)) = iDone`
into `VS = .ValSeq`, which it does not do. Summary functions recurse on `VS`'s
structure, so they can't reduce → the invariant's implication fails. A `<k>`-cell
rewrite instead *unifies* `VS = vCons(V,R)` / `.ValSeq` structurally, which is
what the summary needs.

Confirmed on the real semantics: refactoring to `iterNext : Iterable [total]`
kompiles and passes execution (21/21) but **fails all three loop proofs**
(loop-break / loop-continue / range-loop) exactly this way. Reverted; the
`<k>`-cell version is the one that proves.

## Answer 4 — can we hand kprove the inversion? Base yes, step no (`spec-suml.out`)

If the only gap is that kprove won't invert `g(wrap(VS)) = iDone` into
`VS = .ValSeq`, supply it as `[simplification]` lemmas. `suml` adds two:

```k
rule ssum(VS,A) => A                 requires g(wrap(VS)) ==K iDone            [simplification]
rule ssum(VS,A) => ssum(R, A +Int X) requires g(wrap(VS)) ==K iYield(X,wrap(R)) [simplification]
```

The **base lemma fires** — its `requires` is *closed* (`g(wrap(VS)) ==K iDone`,
no free vars), kprove discharges it from the path condition, and the base branch
closes. The **step lemma does NOT fire**: its `requires` has **free `X`, `R`**
that must be *solved for* against `g(wrap(VS)) = iYield(X, wrap(VS0))` — kprove
checks a closed `requires`, it does not existentially match a simplification
condition. So it sticks in the step case (`#Not{ ssum(VS,A) == ssum(VS0,A+X) }`).
And you cannot restate the step with a closed `requires` without `head`/`tail(VS)`
— which are functions that are themselves stuck on a symbolic `VS`. The step
*inherently* needs `VS`'s structure, i.e. the very thing a `[total]` function
withholds and a `<k>`-cell rewrite provides for free.

## Takeaway

Two independent ways make kprove narrow a symbolic algebraic argument — a
`<k>`-cell rewrite, or a `[total]` function (a **partial** `[function]` does
neither and sticks). But they are **not** interchangeable for our proofs: only
the `<k>`-cell rewrite **substitutes the structure** of the symbolic iterable, so
only it lets a structural *summary* (prefixSum, …) reduce. A `[total]` function
narrows control flow but leaves the structure as an opaque value-constraint — fine
for reaching `.K`, useless for a summary invariant. That is why the shipped loop
dispatch (`src/mpy-core.k` `<k>`-cell `iterNext`) is the right one, and the
elegant `Iterable`-sort design (which would also unify the aggregators) does not
work here. I over-generalized twice — first "functions never narrow", then
"`nest` proves so `Iterable` works" — and each time a sharper one-variable probe
corrected it.
