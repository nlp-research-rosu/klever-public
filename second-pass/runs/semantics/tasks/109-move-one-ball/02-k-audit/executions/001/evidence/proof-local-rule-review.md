# Static soundness decisions for the exhaustive K inventory

The exhaustive declaration/rule list is `k-rule-inventory.md` (962 entries,
SHA-256 recorded in `stage5-inventory.log`). The decisions below use those
entry numbers and the fresh scratch sources.

## Supplied fixed semantics: entries 1-928

All 928 entries are byte-identical to `/reference/reference-semantics`; this is
the selected fixed execution relation in `SUPPLIED_SEMANTICS` mode. They are not
candidate proof extensions. At this selected semantics level they are accepted
as the operational baseline, not reclassified as candidate lemmas. The target
uses only the following slice:

- `syntax.k`: `Module`, `FuncDef`, `Call`, `Name`, `Int`, `Bool`, `Compare`,
  `CmpOp`, `If`, `Return`, `Assign`, `AugAssign`, `Subscript`, and `For`,
  including strict/left-to-right evaluation declarations.
- `core.k`: module/statement sequencing, scopes, name lookup, literals,
  argument evaluation, the builtins scope, and list/sequence constructors.
- `call.k` and `functions.k`: callee/argument evaluation, closure frame
  allocation, parameter binding, return, and frame restoration.
- `controls.k`: assignment, integer `+=`, branching, and the `#loop` protocol.
- `operators.k`, `int.k`, and `bool.k`: comparison and integer addition.
- `builtins.k`: ordinary `len`; `list.k`: ordinary list iteration.
- `subscript.k`: ordinary in-bounds element-zero indexing.

The relevant fixed rules preserve evaluation order, update only the current
function scope, iterate left-to-right, and return through the saved frame. The
program never mutates the input list and performs no heap allocation in the
symbolic claim because a bare read-only `list(ValSeq)` is admitted.

The supplied tree also contains opaque/trusted primitives that are not
reachable from this target: `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
`gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. The assertion
oracle is used only in the independent concrete smoke harness, never by the
positive proof.

Fresh compilation warned about non-exhaustive total-function patterns in
`mapStrVS`, several float helpers, `joinCodes`, and `valSeqAt`. None of the
uncovered shapes is reached by the submitted program on its intended integer
list domain: the only actual `valSeqAt` use is index zero after the empty-list
return, and the proof-local bridge handles that abstract shape. This is a
baseline coverage limitation, not a witnessed false conclusion for this
target.

## Proof-local declarations and rules: entries 929-959

| Inventory | Source | Class and decision |
|---:|---|---|
| 929 | `verification.k:9` | Syntax/function name for the loop body. Acceptable definitional summary. |
| 930 | `verification.k:10-14` | Exact AST transcription of lines 9-12 of `solution.py`; it does not replace execution. Sound. |
| 931 | `verification.k:16` | Syntax/function name for the full body. Acceptable definitional summary. |
| 932 | `verification.k:17-28` | Exact AST transcription of the regenerated `solution.mpy` body. Sound as a definition; the byte-identical translation and concrete full-module execution independently support the transcription. |
| 933 | `verification.k:30` | Syntax/function name for the closure. Acceptable definitional summary. |
| 934 | `verification.k:31-32` | Constructs the one-argument closure in module scope zero, matching fixed `FuncDef` loading for this top-level capture-free function. Sound. |
| 935 | `verification.k:37` | Fresh `intVals(IntSeq)` constructor. It is an abstract list-sequence representation, not a fixed-semantics `vCons` list and has no bridge-free connection theorem. Material real-input pinning gap; the declaration alone asserts no false equation. |
| 936 | `verification.k:43-44` | Empty iterator bridge. Truthful under the intended `intVals` interpretation, but no fixed-semantics connection theorem exists because the representation is fresh. Evidence gap, not a witnessed false conclusion. |
| 937 | `verification.k:45-47` | Nonempty iterator bridge. It yields the head and recursively encoded tail, matching left-to-right list iteration under the intended interpretation. Same missing universal connection theorem as entry 936. |
| 938 | `verification.k:49-52` | Empty-list `len` bridge returns zero. Truthful under the intended interpretation; same representation-connection gap. |
| 939 | `verification.k:53-56` | **Unsound over-broad operational bridge.** It returns `1` for every nonempty encoded list under an arbitrary continuation. For `intVals(iCons(10,iCons(20,.IntSeq)))`, Python and the fixed concrete `vCons` semantics return `2`; the extended theory proves `1` and even proves the observable false comparison `len(...) == 1`. The opposite result `2` gets stuck at `1`. See `stage5-len-bridge-final.log`. |
| 940 | `verification.k:60-62` | Index-zero bridge returns the encoded head. Truthful for nonempty encoded integer lists, but lacks the same bridge-free representation theorem. |
| 941 | `verification.k:67` | `addDrop` function/total declaration. The following equation covers all three integer arguments. Sound. |
| 942 | `verification.k:68-69` | Adds exactly one iff `C < P`; ordinary integer mathematics. Sound. |
| 943 | `verification.k:71` | `scanDrops` total declaration. All intended integer `vCons` and `intVals` cases are covered. Non-integer `ValSeq` heads are outside the claim and not equated; narrower off-domain coverage gap only. |
| 944 | `verification.k:72` | Empty concrete sequence base case. Sound. |
| 945 | `verification.k:73-74` | Concrete integer-head recursion consumes one constructor and applies `addDrop`. Sound and descending. |
| 946 | `verification.k:75` | Empty encoded sequence base case. Sound. |
| 947 | `verification.k:76-77` | Encoded integer-head recursion consumes one `iCons`. Sound and descending. |
| 948 | `verification.k:79` | `scanLast` total declaration. Intended integer cases are covered; non-integer `ValSeq` is an off-domain coverage limitation. |
| 949 | `verification.k:80` | Empty concrete sequence returns the prior value. Sound. |
| 950 | `verification.k:81-82` | Concrete recursion retains the most recent element and descends. Sound. |
| 951 | `verification.k:83` | Empty encoded sequence returns the prior value. Sound. |
| 952 | `verification.k:84-85` | Encoded recursion retains the most recent element and descends. Sound. |
| 953 | `verification.k:87` | `circularDrops` total declaration. Fully defined in terms of the preceding folds on the intended integer domain. |
| 954 | `verification.k:88-89` | Counts linear strict descents and the last-to-first wrap descent. Sound. |
| 955 | `verification.k:91` | `moveOneBallSpec` total declaration. The main claim uses only `intVals(IntSeq)`, whose empty/nonempty constructors are covered; arbitrary non-integer `vCons` heads are an unused coverage limitation. |
| 956 | `verification.k:92` | Empty concrete sequence maps to true. Sound. |
| 957 | `verification.k:93-94` | Nonempty concrete integer sequence tests circular descents `< 2`. Sound. |
| 958 | `verification.k:95` | Empty encoded sequence maps to true. Sound. |
| 959 | `verification.k:96-97` | Nonempty encoded integer sequence tests circular descents `< 2`. Sound. |

There are no proof-local simplification rules, `[functional]` declarations, or
opaque result functions. The five priority rules are entries 936-940. Entry
939 is the only rule for which a concrete false-conclusion witness is asserted;
entries 935-940 otherwise have the narrower missing-connection evidence gap
described above.

## Reachability claims: entries 960-962

| Inventory | Claim decision |
|---:|---|
| 960 | The nonempty loop-induction claim matches the real `#loop` control point after `current` is already bound. It preserves `arr` and `first`, folds `drops`, and sets `previous` and `current` to the final element. It is a valid circularity under the extended `intVals` theory. |
| 961 | The loop-entry claim matches the real nonempty loop point before `current` exists. One fixed semantic iteration creates the binding, after which entry 960 applies. Valid under the extended theory. |
| 962 | The entry claim is result-constraining: it returns `moveOneBallSpec`, not a free variable or implication. Its closure body is the submitted body, but its quantified input is the fresh `list(intVals(IS))`, not the supplied semantics' real `list(vCons(...))`, and closure depends on the unsound entry-939 bridge. It therefore does not establish the required theorem about the real program on real lists. |
