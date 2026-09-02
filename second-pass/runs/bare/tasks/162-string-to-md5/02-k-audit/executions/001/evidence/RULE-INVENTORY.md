# Local rule and declaration inventory

Sources inventoried from the clean copy:
`/tmp/audit-work/reconstruction/semantic.k`,
`verification.k`, and `spec.k`. The declaration-line extraction is preserved in
`declaration-lines.log`.

## Syntax, attributes, configuration, and claims

- `MPY-SYNTAX` declares `Program = Module(Stmts)`; list-valued `Stmts`;
  `Stmt = Import | FuncDef | Return`; one-string `Params`; and exactly the
  expression constructors used by the submitted term:
  `NoneVal`, `Str`, `Name`, `Compare`, `IfExp`, `Attribute`, and zero/one
  argument `Call`, plus `CmpOp`. There are no evaluation attributes on this
  constructor syntax because evaluation is explicit through `#eval`.
- `SEMANTIC` declares tagged values `pyNone`, `pyBool`, `pyString`, `pyBytes`,
  `pyModule`, `pyBuiltin`, and `pyMethod`; stored functions `fn`; result
  alternatives; and the explicit computation frames `#load`, `#loadStmts`,
  `#start`, `#invoke`, `#functionEnd`, `#eval`, compare/if/attribute/call
  frames, `#apply0`, and `#apply1`.
- The configuration has exactly `<k>`, `<input>`, `<functions>`, `<env>`, and
  `<result>` below `<py>`. Each non-`k` cell is read or written.
- The MD5 layer declares `Md5State` and the local functions `md5String`,
  `md5Bytes`, `utf8Bytes`, `utf8CodePoint`, `md5Pad`, `md5Blocks`,
  `md5Rounds`, `md5AddState`, `md5StateHex`, `hexWordLE`, `hexByte`,
  `hexNibble`, `md5F`, `md5G`, `md5Shift`, `md5K`, `md5Word`, both arities
  of `add32`, and `rotl32`.
- `verification.k` adds three functions: exact program macros `solutionBody`
  and `solutionProgram`, and `expectedMd5(String)`.
- No local declaration has `[total]`, `[functional]`, `opaque`, `owise`,
  `priority`, or a rule-priority attribute. The only special rule attributes
  are `[simplification]` on `utf8Bytes("")`, `[concrete(S),
  simplification]` on recursive `utf8Bytes(S)`, and `[concrete(B),
  simplification]` on `md5Bytes(B)`.
- `spec.k` has five all-path claims: `empty`, `nonempty-symbolic`,
  `prompt-example`, `unicode-utf8`, and `multiblock-padding`. There are no
  helper/loop claims or trusted claims.

## Rule-by-rule decisions

The 154 rules in `semantic.k` and three rules in `verification.k` are fully
partitioned below. A grouped row makes one decision for every listed rule; no
local rule is omitted.

| Lines | Rules | Count | Class and decision |
|---|---|---:|---|
| 64–69 | `#load(Module)`, empty/import/function `#loadStmts` | 4 | Ordinary operational rules. For the exact module, they preserve source order, ignore the non-effectful import statement, and bind the exact function body. Sound for the submitted module. |
| 72–83 | `#start`, `#invoke`, `Return`, `#functionEnd` | 4 | Ordinary operational rules. They bind the configured input to `text`, execute the stored body, implement abrupt return, and place the value in `<result>`. The environment reset drops globals, but the only global use is separately modeled `hashlib`; sound for this body, not reusable Python semantics. |
| 87–91 | `NoneVal`, `Str`, special `Name("hashlib")`, environment `Name(N)` | 4 | Ordinary expression rules. Correct on the reached environments. The two name rules would overlap if a local `hashlib` binding existed; the real invocation creates only `text`, so this is a reuse limitation rather than a false reachable conclusion. |
| 93–98 | compare-left, compare-right, string `==` | 3 | Ordinary frames/rule. Left then right evaluation and string equality match the sole submitted comparison. Guards/shape are disjoint. |
| 100–103 | conditional test, true branch, false branch | 3 | Ordinary frames/rules. Exactly one branch fires after a Boolean test; correct and disjoint. |
| 105–112 | attribute receiver; `hashlib.md5`, `str.encode`, `md5.hexdigest` selections | 4 | Ordinary operational rules. Binding and receiver evaluation match the exact nested expression. `pyBytes` represents both encoded bytes and the one-use MD5 object; that conflation would accept invalid programs such as `text.encode().hexdigest()`, but the submitted constructor tree always inserts the `hashlib.md5` call first. |
| 114–120 | zero-argument call frame/apply; encode and hexdigest applications | 4 | Ordinary operational bridge for the two fixed external operations. Encode delegates to `utf8Bytes`; hexdigest delegates to the local MD5 definition. Correct for Unicode scalar strings, subject to the surrogate-domain and external-input caveats below. |
| 122–127 | one-argument call frame/apply; `hashlib.md5` application | 3 | Ordinary operational rules. Function expression precedes argument; the bytes payload is preserved as the modeled MD5 object. Exact for the sole use. |
| 157 | `md5String(S)` | 1 | Definitional summary, reducing to MD5 of UTF-8 bytes. |
| 158–163 | empty and recursive `utf8Bytes` | 2 | Definitional summaries/simplifications. Guards are disjoint and cover K strings; recursion removes one character and descends. The equations are correct for internal Unicode-scalar K strings. The `krun -cTEXT` front end does not preserve such strings above U+00FF; that is a concrete bridge defect recorded separately. |
| 165–181 | four `utf8CodePoint` ranges | 4 | Definitional UTF-8 equations. The four numeric guards are disjoint and cover 0..0x10ffff. Formulas are correct for Unicode scalar values. The third guard also includes 0xd800..0xdfff, where Python strict UTF-8 raises and Unicode defines no scalar. Witness: `C=55296` yields bytes `ed a0 80` under the rule while `chr(55296).encode()` raises `UnicodeEncodeError`. The Haskell backend rejects a surrogate K string, so this manifests as source-domain narrowing rather than a runnable K-string witness. |
| 182–187 | `md5Bytes` | 1 | Concrete simplification/definitional summary. Initializes the RFC state, pads, processes blocks, and formats the state. It is not an unconstrained oracle: every ground byte string reduces through the following equations. |
| 189–194 | `md5Pad` | 1 | Definitional rule. Appends `0x80`, pads to 56 modulo 64, and appends the low 64 bits of the bit length little-endian. K's documented fixed-width `Int2Bytes` truncates high bits as RFC MD5 requires. |
| 196–200 | `md5Blocks` stop and recursive cases | 2 | Definitional rules. Guards are complementary; padded inputs advance by 64 and terminate. |
| 202–218 | `md5Rounds` base and recursive cases | 2 | Definitional rules. From `I=0`, the recursive guard covers 0..63, advances by one, and reaches the disjoint `I=64` base. The state permutation matches RFC MD5. |
| 220–223 | `md5AddState` | 1 | Definitional component-wise modulo-2^32 feed-forward. |
| 225–227 | `md5StateHex` | 1 | Definitional concatenation of four little-endian words. |
| 229–233 | `hexWordLE` | 1 | Definitional extraction of four low-to-high bytes. |
| 234–235 | `hexByte` | 1 | Definitional high/low nibble formatting; its reached domain is 0..255. |
| 236–251 | `hexNibble(0)` through `hexNibble(15)` | 16 | Sixteen disjoint exhaustive equations on the reached nibble domain, with the correct lowercase hexadecimal digit in every row. |
| 253–260 | `md5Word` | 1 | Definitional little-endian load of four bytes at word index `G`; padding and round guards keep every reached slice in bounds. |
| 262–264 | two- and four-operand `add32` | 2 | Definitional modulo-2^32 addition. Arity makes the rules disjoint. |
| 265–266 | `rotl32` | 1 | Definitional 32-bit left rotation; every reached shift is 4..23 and every input is masked/nonnegative modulo 2^32. |
| 268–275 | four `md5F` round ranges | 4 | Definitional RFC Boolean functions. Guards are pairwise disjoint and cover reached indices 0..63. Negative mathematical integers from `~Int` are reduced modulo 2^32 by the surrounding `add32`, preserving the low 32-bit result. |
| 277–283 | four `md5G` round ranges | 4 | Definitional RFC word-index schedules. Guards are pairwise disjoint and cover 0..63. |
| 285–300 | sixteen `md5Shift` range/residue rules | 16 | Definitional shift table. Range/residue guards are pairwise disjoint and cover each index 0..63 exactly once. `md5-table-check.log` verifies all 64 derived entries. |
| 302–365 | `md5K(0)` through `md5K(63)` | 64 | Sixty-four distinct ground equations. `md5-table-check.log` independently recomputes every value as `floor(2^32 * abs(sin(i+1)))`; all match. |
| `verification.k` 9–21 | `solutionBody` | 1 | Definitional source macro. Constructor-level identity with trusted regeneration is established by `program-term-check.log`. |
| `verification.k` 24–27 | `solutionProgram` | 1 | Definitional source macro. It contains the exact import, function name, parameter, and `solutionBody`; constructor identity passes. |
| `verification.k` 31 | `expectedMd5(S)` | 1 | Definitional postcondition summary `pyString(md5String(S))`. It does not replace program execution. It shares the semantic MD5 function used by the external primitive model, so the reachability proof establishes equality to that modeled primitive; correctness relative to CPython/RFC remains in the audited semantics/trust boundary. |

Count check: operational rules 29; MD5/UTF-8 rules 125; total
`semantic.k` rules 154. Adding the three verification rules gives 157 local
rules. The five spec claims are inventoried separately.

## Trusted imported operations

The local equations depend on K's built-in `String`, `Bytes`, `Int`, `Bool`,
and `Map` hooks, especially `ordChar`, `substrString`, `lengthString`,
`Int2Bytes`, `Bytes2Int`, byte concatenation/slicing/padding, integer
bitwise/arithmetic operations, and map lookup/update. These are toolchain
primitives rather than candidate-local proof rules.
