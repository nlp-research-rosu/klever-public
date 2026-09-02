# Exhaustive local K inventory

Source files inventoried: `/tmp/audit-work/source/semantic.k`,
`verification.k`, and `spec.k`. There are no other submitted K helper files.

## Syntax, configuration, and attributes

| ID | Location | Declaration | Attributes / role |
|---|---|---|---|
| D01 | semantic.k:8 | `Program ::= Module(Stmts)` | source constructor |
| D02 | semantic.k:10 | `Stmts ::= List{Stmt, ""}` | built-in list syntax |
| D03 | semantic.k:11-12 | `Stmt ::= FuncDef(...) \| Return(Expr)` | two source constructors |
| D04 | semantic.k:14 | `Params ::= Params(Strings)` | source constructor |
| D05 | semantic.k:15 | `Strings ::= List{String, ","}` | built-in list syntax |
| D06 | semantic.k:17-20 | `Expr ::= Name \| Attribute \| Call` | three source constructors |
| D07 | semantic.k:20 | `Exprs ::= List{Expr, ","}` | built-in list syntax |
| D08 | semantic.k:31-33 | `Value ::= StrVal \| SetVal \| IntVal` | three semantic values |
| D09 | semantic.k:34 | `Result ::= noResult \| Value` | result cell values |
| D10 | semantic.k:35 | `KResult ::= Value` | marks all `Value`s evaluated |
| D11 | semantic.k:37-40 | `KItem ::= #lower \| #set \| #len \| #finish` | four strictness continuations |
| D12 | semantic.k:42-48 | `<mpy>` with `<k>`, `<env>`, `<input>`, `<result>` | complete submitted configuration |
| D13 | semantic.k:78 | `lowerString(String):String` | `[function]`; not declared `total` |
| D14 | semantic.k:85 | `lowerChar(String):String` | `[function]`; second equation `[owise]` |
| D15 | semantic.k:92 | `charsSet(String):Set` | `[function]`; not declared `total` |
| D16 | verification.k:8 | `expectedDistinctCharacters(String):Int` | `[function]`; not declared `total` |

There are no submitted `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, explicit priority, or opaque declarations. `[owise]` supplies
the usual lower priority to R14. Imported theory is `STRING-SYNTAX`, `INT`,
`BOOL`, `STRING`, `SET`, and `MAP`.

## Rules and claims

| ID | Location | Rule / claim | Classification and audit result |
|---|---|---|---|
| R01 | semantic.k:52-55 | load the one-function module, bind its sole parameter to `<input>` | ordinary semantic rule; exact for the submitted module and empty initial environment |
| R02 | semantic.k:57 | `Return(E) .Stmts => E ~> #finish` | ordinary control rule; exact for the submitted single-return body |
| R03 | semantic.k:59-60 | `Name(X)` map lookup | ordinary semantic rule; exact for `string` |
| R04 | semantic.k:63 | lower call to receiver then `#lower` | primitive-call dispatch; preserves actual receiver evaluation |
| R05 | semantic.k:64 | apply `lowerString` to `StrVal` | result-bearing primitive bridge; materially incorrect for unrestricted Python strings |
| R06 | semantic.k:66 | set call to argument then `#set` | primitive-call dispatch; exact on the used binding |
| R07 | semantic.k:67 | apply `charsSet` to `StrVal` | result-bearing primitive bridge; correct for the modeled K characters |
| R08 | semantic.k:69 | len call to argument then `#len` | primitive-call dispatch; exact on the used binding |
| R09 | semantic.k:70 | K set size to `IntVal` | trusted SET primitive bridge |
| R10 | semantic.k:72-73 | finish by writing `<result>` | ordinary terminal rule; exact for the top-level execution |
| R11 | semantic.k:79 | `lowerString("") => ""` | definitional base equation; true |
| R12 | semantic.k:80-83 | recurse over first character and suffix | definitional recursion; decreases string length |
| R13 | semantic.k:86-87 | ASCII code 65-90 maps to code + 32 | definitional equation; true for ASCII uppercase |
| R14 | semantic.k:88 | all other characters unchanged `[owise]` | false as a model of Python `str.lower`; witness `C="Ä"` |
| R15 | semantic.k:93 | `charsSet("") => .Set` | definitional base equation; true |
| R16 | semantic.k:94-97 | insert first character and recurse on suffix | definitional recursion; duplicates removed by K set union |
| R17 | verification.k:9 | expected result is `size(charsSet(lowerString(S)))` | definitional summary of the generated semantics, not an independent Python-lower theorem |
| C01 | spec.k:7-22 | universal entry claim for all K strings | closes, pins actual term, but states the wrong Unicode result |
| C02 | spec.k:25-38 | concrete `"xyzXYZ"` result 3 | closes and agrees with Python |
| C03 | spec.k:40-53 | concrete `"Jerry"` result 4 | closes and agrees with Python |
| C04 | spec.k:55-68 | concrete empty-string result 0 | closes and agrees with Python |

## Used-construct coverage and execution order

`solution.mpy` uses `Module`, `FuncDef`, one `Params` item, `Return`, `Call`,
`Name`, `Attribute`, empty `Exprs`, and the `Stmts` list. D01-D07 declare all
of them. R01 loads the exact function; R02 starts return-expression
evaluation; R08/R06/R04 evaluate outer `len`, then `set`, then `lower`; R03
looks up `string`; R05/R07/R09 compute the three primitive results; R10 writes
the result. `<env>` is initialized and bound once, `<input>` is read and
preserved, and `<result>` is written once. The submitted program needs no
heap, output, exceptions, loops, allocation, or call stack.

## Concrete false-conclusion witness

`"Ää"` satisfies C01's unrestricted `S:String` precondition. R14 leaves `Ä`
unchanged, so R05 produces `"Ää"` and the K program obtains a two-element
set. The rebuilt semantics returns `IntVal(2)`, and the added concrete witness
claim proving `2` closes with `#Top`. Python evaluates `"Ää".lower()` as
`"ää"`; both the trusted canonical and submitted Python therefore return `1`.
This witness is on the source-contract domain and makes the generated
semantics materially inadequate.
