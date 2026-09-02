# Exhaustive local K inventory

Source hashes are in `01_provenance_integrity.log`. Line numbers below refer to
the scratch copies, which are byte copies of the candidate source.

## Declarations and attributes

`semantic.k` has these syntax productions:

| Lines | Sort | Productions | Use and disposition |
|---|---|---|---|
| 8 | `PyModule` | `Module(Stmts)` | Used by `solution.mpy`; modeled by S01. |
| 9 | `Stmts` | separatorless `List{Stmt,""}` | Used for the module and function body; modeled by S02–S04. |
| 11–13 | `Stmt` | `FuncDef`, `Expr`, `Return` | `FuncDef` and `Return` are used; `Expr` is unused by the submitted term. |
| 15 | `Params` | one string parameter | Used and exactly matched by S01. |
| 17–24 | `Expr` | `Str`, `Int`, `Bool`, `Name`, `BinOp`, `Attribute`, `Call`, `ListComp` | Every production occurs in the submitted term. |
| 26 | `CompFor` | target, iterable, predicate | Used in the submitted comprehension. |
| 36–41 | `Value` | `VInt`, `VBool`, `VText`, `VChar`, `VChars`, `VList` | Six internal value constructors, all marked `[constructor]`; `VBool` is not dynamically needed for this exact term. |
| 43–54 | `KItem` | `exec`, `eval`, `discard`, `finish`, `binLeft`, `binRight`, `doOrd`, `doChr`, `doJoin`, `comp`, `compTail`, `prepend` | Twelve internal control constructors. |

`verification.k` adds:

| Lines | Sort | Productions and attributes | Coverage |
|---|---|---|---|
| 6–7 | `Chars` | `nil`, `cons(Int,Chars)`, both `[constructor]` | Inductive and exhaustive for modeled character sequences. |
| 10 | `Int` | `decodeCode(Int) [function,total]` | One unconditional equation V01. |
| 13 | `Chars` | `decodeSpec(Chars) [function,total]` | Disjoint/exhaustive base and constructor equations V02–V03. |
| 17 | `Int` | `encodeCode(Int) [function,total]` | One unconditional equation V04. |
| 20 | `Chars` | `encodeSpec(Chars) [function,total]` | Disjoint/exhaustive base and constructor equations V05–V06. |
| 24 | `Bool` | `isLowerCode(Int) [function,total]` | One unconditional equation V07. |
| 27 | `Bool` | `allLower(Chars) [function,total]` | Disjoint/exhaustive base and constructor equations V08–V09. |

There are no local `[functional]`, `[simplification]`, `[concrete]`,
`[priority]`, `[owise]`, or opaque declarations. There are no priority rules.
The only local non-default attributes are the eight constructor markings
(six `Value` productions, two `Chars` productions, with a single attribute on
each production) and six pairs of `[function,total]` attributes.

## Configuration

Lines 56–63 define exactly five cells beneath `<m>`:

- `<k>` starts with `$PGM:PyModule`.
- `<s>` is the modeled entry argument binding and starts as `nil`.
- `<ch>` is the comprehension-variable binding and starts as `0`.
- `<input>` is initialized from `$INPUT:Chars`.
- `<result>` starts as `.K`.

There is no heap, call stack, output, exception, or allocation cell. For the
submitted straight-line single-function subset this is sufficient, but it is
not a general Python configuration.

## Ordinary semantic rules

Each local operational rule in `semantic.k` is listed once:

| ID / lines | Rule | Static judgment |
|---|---|---|
| S01 / 66–68 | Exact one-function `Module(FuncDef("decode_shift",Params("s"),BODY))` loads `<input>` into `<s>` and starts `exec(BODY)`. | Sound as the declared entry-harness convention for this exact module. It omits general Python definition lookup and call frames, but it does not synthesize the result and it executes `BODY`. |
| S02 / 70 | `exec(.Stmts) => .K`. | Correct end of statement sequence. |
| S03 / 71 | Expression statement: evaluate, discard, continue. | Correct left-to-right control for the modeled form; unused by the submitted term. |
| S04 / 72 | Return: evaluate and `finish`, dropping following statements. | Correct abrupt return for the single entry frame. |
| S05 / 74 | Discard a completed `Value`. | Correct for expression statements; unused by the submitted term. |
| S06 / 75–76 | `finish` consumes `<k>` and installs the value into an initially empty result cell. | Correct for the single-frame entry harness and constrains the observable result. |
| S07 / 78 | Integer literal to `VInt`. | Direct literal semantics. |
| S08 / 79 | Boolean literal to `VBool`. | Direct literal semantics; the submitted `Bool(true)` is pattern-matched by S25. |
| S09 / 80 | Empty string to `VChars(nil)`. | Correct abstract contents for the submitted empty join receiver; the receiver is in fact matched syntactically by S23. |
| S10 / 81 | Nonempty string to `VText(S)`, guarded away from empty. | Disjoint from S09 and correct for `"a"`, the only dynamically evaluated text literal. |
| S11 / 82–83 | `Name("s")` reads `<s>` as `VChars`. | Correct binding for the exact source and S01. |
| S12 / 84–85 | `Name("ch")` reads `<ch>` as `VChar`. | Correct comprehension binding for the exact source. |
| S13 / 87–88 | Begin binary expression by evaluating the left operand. | Matches Python left-before-right evaluation. |
| S14 / 89–90 | After the left value, evaluate the right and save the left. | Preserves evaluation order and operand identity. |
| S15 / 91 | Right `J` plus saved left `I` gives `I +Int J`. | Correct. |
| S16 / 92 | Right `J` minus saved left `I` gives `I -Int J`. | Correct operand order. |
| S17 / 93 | Right `J` modulo saved left `I` gives `I modInt J`. | Correct for the used positive divisor 26; K Euclidean modulo agrees with Python `%` there. |
| S18 / 95 | Exact syntactic `ord` call evaluates its argument. | Correct for the unshadowed builtin in this source. |
| S19 / 96 | `ord` of modeled input character returns its code. | Correct by the `VChar` representation. |
| S20 / 97 | `ord` of `VText(S)` uses K `ordChar`. | Correct for the used one-character text `"a"`; depends on the K STRING hook. |
| S21 / 99 | Exact syntactic `chr` call evaluates its argument. | Correct for the unshadowed builtin in this source. |
| S22 / 100 | `chr` of `VInt(C)` produces `VChar(C)`. | Correct on the intended lowercase domain, where `C` is 97–122. It does not model Python's out-of-Unicode-range exception. |
| S23 / 102–103 | Exact `Attribute(Str(""),"join")` call evaluates its list argument. | Correct for this source's unshadowed empty-string join call. |
| S24 / 104 | Joining `VList(CS)` gives `VChars(CS)`. | Correct because every list element is a modeled character and the separator is empty. |
| S25 / 108–111 | Exact one-generator/unfiltered list comprehension over `s` starts `comp(X,E,CS)`; guard fixes iterable name to `"s"`. | Correct for the submitted `CompFor(Name("ch"),Name("s"),Bool(true))`. |
| S26 / 113 | Empty comprehension input gives an empty list. | Correct base case. |
| S27 / 114–117 | For `cons(C,CS)`, save old `<ch>`, bind `C`, evaluate the element, then continue; guard fixes target to `"ch"`. | Correct one-iteration binding and order. |
| S28 / 118–120 | After a character element, restore saved `<ch>`, recursively process the tail, then prepend the element. | Correct restoration and order; all other cells and the trailing continuation are framed. |
| S29 / 121 | Prepend the saved head to the recursively produced list. | Correct list order. |

Overlap review: S09/S10 are disjoint by the nonempty guard; S11/S12,
S15/S16/S17, S19/S20, and S26/S27 have distinct constructors or literals.
The statement rules have distinct list heads. No ordinary semantic overlap or
priority dependence was found.

Scope limitations without an intended-domain false witness: S01 is an entry
harness rather than general Python module/call semantics; S18/S21/S23 hard-code
the unshadowed builtins used by this exact source; S22 omits `chr` range
exceptions; S17 models only operators for which local rules exist. For all
`allLower` entry states, the intermediate `chr` code is 97–122, the divisor is
26, and the exact bindings are fixed by the submitted source. Consequently
none of these limitations enables a false result on the intended domain.

## Verification equations

| ID / lines | Equation | Static judgment |
|---|---|---|
| V01 / 11 | `decodeCode(C) = ((C-5-97) mod 26)+97`. | The same arithmetic as `solution.py`; unconditional and total on mathematical integers. |
| V02 / 14 | `decodeSpec(nil) = nil`. | Correct base, disjoint from V03. |
| V03 / 15 | Map `decodeCode` over `cons`. | Correct constructor recursion and structurally descending. |
| V04 / 18 | `encodeCode(C) = ((C+5-97) mod 26)+97`. | The prompt's encoder arithmetic; unconditional and total. |
| V05 / 21 | `encodeSpec(nil) = nil`. | Correct base, disjoint from V06. |
| V06 / 22 | Map `encodeCode` over `cons`. | Correct constructor recursion and structurally descending. |
| V07 / 25 | `isLowerCode(C) = (97 <= C and C <= 122)`. | Exact ASCII-lowercase predicate, unconditional and total. |
| V08 / 28 | `allLower(nil) = true`. | Correct base, disjoint from V09. |
| V09 / 29 | Head is lowercase and tail is all-lower. | Correct constructor recursion and structurally descending. |

All six `[total]` declarations have unconditional coverage or disjoint,
exhaustive `nil`/`cons` coverage. No right-hand sides disagree on an overlap.
No equation is an oracle: `decodeCode` is used in the postcondition, but S13–S22
independently execute the AST arithmetic and builtin calls before the loop
claim equates that execution with `decodeSpec`.

## Claims

| Lines / label | Role and judgment |
|---|---|
| 8–10 / `code-inverse` | Arithmetic lemma: for lowercase `C`, `decodeCode(encodeCode(C)) = C`. Ordinary modular arithmetic; no operational rewrite or oracle. |
| 14–34 / `loop-correct` | Progressing circularity for exact `comp("ch",DECODE_EXPR,CS)`, arbitrary continuation, and arbitrary saved `<ch>`. Base is S26; constructor execution takes real S27 and expression steps, restores state through S28, then recurs. |
| 38–65 / `program-correct` | Entry theorem over the literal submitted module. It consumes `<k>`, changes `<s>` from `nil` to `CS`, preserves `<ch>=0` and `<input>=CS`, and fixes `<result>` to `VChars(decodeSpec(CS))`. |

No claim replaces an ordinary semantic step. The only coinductive summary is
the `loop-correct` claim, whose recursive use is preceded by real progress and
whose complete observable footprint (`<k>` and `<ch>`) matches the pure
comprehension region; other cells are neither read nor written by S26–S29.
