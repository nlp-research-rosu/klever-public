# Ground claim witnesses

## Loop claim

One satisfiable instance of the loop claim in `/candidate/spec.k:9` is:

- `M = whole(.Music)`, `L = 1`, `B = 0`
- `S = str(iCons(111, .IntSeq))`
- `N = str(.IntSeq)`, `P = parent(0)`, `A = .ValSeq`
- `<k>` starts with
  `#loop(musicIter(whole(.Music)), Name("note"), parseMusicLoopBody)`
- scope 1 binds `music_string` to `S`, `beats` to `ref(0)`, and `note` to
  `N`; heap location 0 contains `list(.ValSeq)`.

The destination binds `note` to `str(iCons(111, .IntSeq))` and changes heap
location 0 to `list(vCons(4, .ValSeq))`. Under the intended informal encoding,
the corresponding Python input is `"o"`; both trusted canonical and generated
Python return `[4]`.

## Entry claim

The entry claim has no explicit `requires`; its sort and exact-cell patterns are
its precondition. A formal satisfying instance is `M = .Music` with the exact
clean initial configuration written in `/candidate/spec.k:33-48`. Under the
intended informal encoding this is the empty input, and both Python
implementations return `[]`.

A second useful instance is `M = whole(.Music)`, informally corresponding to
`"o"`; both Python implementations return `[4]`.

The formal terms `str(musicCodes(.Music))` and
`str(musicCodes(whole(.Music)))` are not fixed-semantics encodings of `""` and
`"o"`: `musicCodes` has no equations. That bridge is assumed by the proof-only
split rule.

## Fixed-semantics state counterexample

`/audit-output/evidence/ground-o.mpy` executes the exact translated function and
then calls it on the valid input `"o"` using only the fixed supplied concrete
semantics. The final state in `stage4_bridge_witness.log` has:

```text
<heap>
  0 |-> list(vCons(4, .ValSeq))
  1 |-> list(vCons(str(iCons(111, .IntSeq)), .ValSeq))
</heap>
<heapLoc> 2 </heapLoc>
```

The entry claim instead concludes an exact heap with only location 0 and
`<heapLoc> 1 </heapLoc>`. The candidate's priority-35 split bridge preempts the
fixed priority-40 split rule, skips allocation of location 1, and therefore
enables that false final-state conclusion.
