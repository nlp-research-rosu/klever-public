# Target-path static review

The exhaustive machine-generated inventory is `k-rule-inventory.tsv`. It has
929 records: every local `syntax`, `configuration`, `context`, `rule`, and
`claim` directive in the supplied semantics tree, `verification.k`, and
`spec.k`. `reference-semantics/semantics.k` and `verification.k` have zero such
directives; they only assemble/import modules. The spec has one claim.

No `[simplification]` rule or `[functional]` declaration occurs. There are 22
`[function,total,symbol(...),no-evaluators]` declarations. They are the MD5,
float, and sorting primitives listed in the inventory; none occurs in the
target claim, its program body, or a rule selected by its execution. The 32
`[concrete]` rules and every rule in `MPY-CONCRETE` are also absent from the
Haskell definition imported by `VERIFICATION`.

## Program syntax mapping

| Submitted constructor | Declaration | Execution rules |
|---|---|---|
| `Module(Stmts)` | `syntax.k:61` | `core.k:124-127` loads/sequences the module; `functions.k:14-16` binds the exact `FuncDef` closure. The entry claim starts after this deterministic setup and pins its resulting binding. |
| `FuncDef`, `Params`, `Return` | `syntax.k:50,53,56-60` | `functions.k:14-16,63-90` creates the closure, binds the sole parameter, implements `Return`, pops the frame, and restores cells. |
| `Call` | `syntax.k:28` | `call.k:20-21` evaluates callee before arguments; `core.k:189-191` evaluates arguments left-to-right; `call.k:24,31,69-74` dispatches the lower method, ordinary builtins, and user closure. |
| `Name` | `syntax.k:12` | `core.k:130-154` follows the pinned current/parent/builtins scope chain. The priority-40 cell rule is disabled because these scopes contain no `$cells` binding. |
| `Attribute` | `syntax.k:29` | strict receiver evaluation plus `call.k:16` yields a bound method; the exact `"lower"` equation is `methods.k:19`. |
| `str(CS)` | `core.k:13-16,18-25,38-39` | Already a `Val`/`KResult`; the claim does not use the ASCII-only `Str(String)` literal loader. |
| `lower` result | `methods.k:10,140-143,154-156` | `mapLower` structurally recurses. `lowerC` maps ASCII `A`–`Z` by `+32` and uses the disjoint `owise` identity case. |
| `set` result | `set.k:8,11-27`; `builtins.k:41` | `dedupCodes`/`dedupFrom` structurally recurse, with complementary `codeIn` and `notBool codeIn` guards; `snocCode` terminates structurally. |
| `len` result | `builtins.k:17,20-26`; `core.k:227-229` | Exact `setV` branch yields `isLen`; `isLen` structurally recurses to an integer. |

## Exact execution path and state/control audit

1. `Call(Name("count_distinct_characters"), str(CS))` takes the generic
   `Call` route. No priority interception matches this syntax.
2. Lookup in scope 0 yields the exact `closureVal`; the argument is already a
   value. The closure rule allocates scope 1, pushes the empty continuation and
   caller environment, and binds `"string"` to `str(CS)`.
3. Nested calls perform normal lookup of `"len"` and `"set"` through scope 1,
   scope 0, then the fixed `builtinsScope`. Receiver lookup finds the parameter;
   `Attribute` produces `boundMethodV(str(CS),"lower")`.
4. The exact lower equation produces `str(mapLower(CS))`; the exact set
   equation produces `setV(dedupCodes(mapLower(CS)))`; the exact len branch
   produces `isLen(dedupCodes(mapLower(CS)))`.
5. `Return` sets `retV`, discards only the remaining callee body/end marker,
   and `#pop` returns the value into the saved empty continuation while removing
   scope 1 and restoring `env`, `scopeLoc`, `stack`, and `ret`. No rule on this
   path reads or writes `heap`, `heapLoc`, `exc`, or `exit-code`.

The higher-priority reference/cell/dereference alternatives are syntactically
or guard-disjoint on the exact initial state. Builtin fold routes are
name-disjoint from `"len"` and `"set"`; their `[owise]` fallback is the intended
route. Lowercase and dedup guards are complementary, and all recursion descends
on an `IntSeq`. There is no priority overlap that selects a different result,
no totality hole for the target algebra, and no opaque result-bearing value.

## Supplied-model boundary

The only target-relevant mismatch with CPython is fixed in the supplied,
read-only semantics: `lowerC` can map one input code to only one output code and
implements only ASCII `A`–`Z`. For U+0130, the fixed model maps `[304]` to
`[304]`, so the claim result is 1; CPython maps `"İ"` to `[105,775]`, so both
trusted canonical and submitted Python return 2. This is a model-vs-CPython
behavior/representation gap, not a candidate rewrite or a narrowed
precondition. The target theorem quantifies over every `CS:IntSeq`.

Review of every off-path inventory record found no rule that can be selected
from the target precondition to introduce a false target conclusion. The
supplied subset has deliberately opaque and partial behavior for unrelated
features (floats, sorting, MD5, and unsupported Python cases), but those symbols
have no dependency on this claim and cannot influence its value or control.
