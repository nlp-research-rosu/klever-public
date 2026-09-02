# Exhaustive K source inventory

Generated from fresh scratch sources. Every top-level `requires`, module/import,
syntax declaration, configuration, context, rule, claim, and alias is listed
verbatim with its source line. Multiline guards and attributes remain attached.

## Counts

- requires: 25
- module: 27
- endmodule: 27
- imports: 88
- syntax: 229
- configuration: 1
- context: 5
- rule: 697
- claim: 1
- alias: 0

Attribute-bearing declaration/rule block counts:

- function: 147
- total: 108
- functional: 0
- simplification: 0
- concrete: 36
- priority: 45
- owise: 26
- macro: 3
- macro-rec: 1
- strict: 2
- seqstrict: 1
- symbol: 25
- no-evaluators: 22

Per-file rule and declaration counts:

- `reference-semantics/semantics.k`: syntax=0, configuration=0, context=0, rule=0, claim=0
- `reference-semantics/semantics/assert.k`: syntax=0, configuration=0, context=0, rule=3, claim=0
- `reference-semantics/semantics/bool.k`: syntax=0, configuration=0, context=1, rule=13, claim=0
- `reference-semantics/semantics/builtins.k`: syntax=38, configuration=0, context=0, rule=137, claim=0
- `reference-semantics/semantics/call.k`: syntax=3, configuration=0, context=0, rule=21, claim=0
- `reference-semantics/semantics/comprehension.k`: syntax=3, configuration=0, context=0, rule=7, claim=0
- `reference-semantics/semantics/concrete.k`: syntax=5, configuration=0, context=0, rule=16, claim=0
- `reference-semantics/semantics/controls.k`: syntax=3, configuration=0, context=0, rule=34, claim=0
- `reference-semantics/semantics/core.k`: syntax=37, configuration=1, context=0, rule=46, claim=0
- `reference-semantics/semantics/dict.k`: syntax=12, configuration=0, context=0, rule=28, claim=0
- `reference-semantics/semantics/float.k`: syntax=34, configuration=0, context=0, rule=121, claim=0
- `reference-semantics/semantics/functions.k`: syntax=4, configuration=0, context=0, rule=15, claim=0
- `reference-semantics/semantics/int.k`: syntax=1, configuration=0, context=0, rule=16, claim=0
- `reference-semantics/semantics/iter.k`: syntax=1, configuration=0, context=0, rule=0, claim=0
- `reference-semantics/semantics/list.k`: syntax=5, configuration=0, context=0, rule=27, claim=0
- `reference-semantics/semantics/methods.k`: syntax=27, configuration=0, context=0, rule=75, claim=0
- `reference-semantics/semantics/operators.k`: syntax=0, configuration=0, context=2, rule=10, claim=0
- `reference-semantics/semantics/range.k`: syntax=2, configuration=0, context=0, rule=6, claim=0
- `reference-semantics/semantics/set.k`: syntax=6, configuration=0, context=0, rule=12, claim=0
- `reference-semantics/semantics/sort.k`: syntax=6, configuration=0, context=0, rule=19, claim=0
- `reference-semantics/semantics/str.k`: syntax=5, configuration=0, context=0, rule=28, claim=0
- `reference-semantics/semantics/subscript.k`: syntax=15, configuration=0, context=2, rule=40, claim=0
- `reference-semantics/semantics/syntax.k`: syntax=16, configuration=0, context=0, rule=0, claim=0
- `reference-semantics/semantics/tuple.k`: syntax=4, configuration=0, context=0, rule=21, claim=0
- `verification.k`: syntax=2, configuration=0, context=0, rule=2, claim=0
- `spec.k`: syntax=0, configuration=0, context=0, rule=0, claim=1

## Opaque/no-evaluator declarations

- `reference-semantics/semantics/builtins.k:285`

      syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
- `reference-semantics/semantics/float.k:24`

      syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
- `reference-semantics/semantics/float.k:30`

      syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
- `reference-semantics/semantics/float.k:37`

      syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
- `reference-semantics/semantics/float.k:50`

      syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
- `reference-semantics/semantics/float.k:54`

      syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
- `reference-semantics/semantics/float.k:103`

      syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
- `reference-semantics/semantics/float.k:107`

      syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
- `reference-semantics/semantics/float.k:111`

      syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
- `reference-semantics/semantics/float.k:115`

      syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
- `reference-semantics/semantics/float.k:119`

      syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
- `reference-semantics/semantics/float.k:125`

      syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
- `reference-semantics/semantics/float.k:142`

      syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
- `reference-semantics/semantics/float.k:160`

      syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
- `reference-semantics/semantics/float.k:190`

      syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
- `reference-semantics/semantics/float.k:195`

      syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
- `reference-semantics/semantics/float.k:209`

      syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
- `reference-semantics/semantics/float.k:217`

      syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
- `reference-semantics/semantics/float.k:223`

      syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
- `reference-semantics/semantics/float.k:230`

      syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
- `reference-semantics/semantics/sort.k:18`

      syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
- `reference-semantics/semantics/sort.k:49`

      syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]

## Priority-bearing rules

- `reference-semantics/semantics/assert.k:13`

      rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/bool.k:29`

      rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
           [priority(40)]
- `reference-semantics/semantics/bool.k:31`

      rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires truthy(V)
           [priority(40)]
- `reference-semantics/semantics/bool.k:35`

      rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool truthy(V)
           [priority(40)]
- `reference-semantics/semantics/bool.k:39`

      rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires truthy(V)
           [priority(40)]
- `reference-semantics/semantics/bool.k:43`

      rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool truthy(V)
           [priority(40)]
- `reference-semantics/semantics/builtins.k:280`

      rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
           [priority(40)]
- `reference-semantics/semantics/call.k:38`

      rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
            => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/call.k:42`

      rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
            => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isRefV(A)
           [priority(40)]
- `reference-semantics/semantics/call.k:47`

      rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
            => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/call.k:56`

      rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
            => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isMutMethod(M)
           [priority(40)]
- `reference-semantics/semantics/call.k:63`

      rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
            => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
           [priority(40)]
- `reference-semantics/semantics/concrete.k:28`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
            => #ksort(VS, KV, .ValSeq, false) ... </k>
           [priority(40)]
- `reference-semantics/semantics/concrete.k:31`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
            => #ksort(VS, KV, .ValSeq, RB) ... </k>
           [priority(40)]
- `reference-semantics/semantics/controls.k:12`

      rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires "$cells" in_keys(M)
            andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
            andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
           [priority(40)]
- `reference-semantics/semantics/controls.k:27`

      rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires X in_keys(M) andBool isRefV({M[X]}:>Val)
           [priority(40)]
- `reference-semantics/semantics/controls.k:95`

      rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/controls.k:98`

      rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/controls.k:101`

      rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/controls.k:106`

      rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/core.k:85`

      rule <k> cellRef(H:Int) => V ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           <heap> ... H |-> cellV(V:Val) ... </heap>
           requires "$cells" in_keys(M)
           [priority(40)]
- `reference-semantics/semantics/core.k:145`

      rule <k> #look(X:String, L:Int) => V ... </k>
           <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
           <heap> ... H |-> cellV(V:Val) ... </heap>
           requires X in_keys(M) andBool "$cells" in_keys(M)
            andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
            andBool {M[X]}:>Val ==K cellRef(H)
           [priority(40)]
- `reference-semantics/semantics/dict.k:58`

      rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
            => #alloc(list(KS)) ... </k>
           [priority(40)]
- `reference-semantics/semantics/dict.k:65`

      rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
           [priority(45)]
- `reference-semantics/semantics/float.k:66`

      rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
- `reference-semantics/semantics/float.k:71`

      rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
- `reference-semantics/semantics/float.k:83`

      rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
- `reference-semantics/semantics/float.k:233`

      rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
- `reference-semantics/semantics/functions.k:68`

      rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
            => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires "$cells" in_keys(M)
            andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
            andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
           [priority(40)]
- `reference-semantics/semantics/list.k:24`

      rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
           [priority(45)]
- `reference-semantics/semantics/list.k:53`

      rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
           <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
           [priority(40)]
- `reference-semantics/semantics/methods.k:72`

      rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
            => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
           [priority(40)]
- `reference-semantics/semantics/methods.k:89`

      rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
            => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
           [priority(39)]
- `reference-semantics/semantics/methods.k:94`

      rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
            => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
           [priority(40)]
- `reference-semantics/semantics/operators.k:25`

      rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/operators.k:28`

      rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isRefV(L)
           [priority(40)]
- `reference-semantics/semantics/operators.k:34`

      rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires OP =/=String "in" andBool OP =/=String "not in"
           [priority(40)]
- `reference-semantics/semantics/operators.k:38`

      rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isRefV(L)
            orBool OP ==String "in" orBool OP ==String "not in"
           [priority(40)]
- `reference-semantics/semantics/operators.k:44`

      rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/sort.k:40`

      rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
           <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
           [priority(40)]
- `reference-semantics/semantics/subscript.k:31`

      rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/subscript.k:58`

      rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
            => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
           [priority(45)]
- `reference-semantics/semantics/tuple.k:35`

      rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires "$cells" in_keys(M)
            andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
            andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
           [priority(40)]
- `reference-semantics/semantics/tuple.k:44`

      rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]
- `reference-semantics/semantics/tuple.k:52`

      rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

## Complete declaration and rule listing

### `reference-semantics/semantics.k`

- Line 34; `requires`

    requires "semantics/syntax.k"

- Line 35; `requires`

    requires "semantics/core.k"

- Line 36; `requires`

    requires "semantics/iter.k"

- Line 37; `requires`

    requires "semantics/range.k"

- Line 38; `requires`

    requires "semantics/operators.k"

- Line 39; `requires`

    requires "semantics/int.k"

- Line 40; `requires`

    requires "semantics/bool.k"

- Line 41; `requires`

    requires "semantics/float.k"

- Line 42; `requires`

    requires "semantics/str.k"

- Line 43; `requires`

    requires "semantics/set.k"

- Line 44; `requires`

    requires "semantics/list.k"

- Line 45; `requires`

    requires "semantics/tuple.k"

- Line 46; `requires`

    requires "semantics/subscript.k"

- Line 47; `requires`

    requires "semantics/comprehension.k"

- Line 48; `requires`

    requires "semantics/methods.k"

- Line 49; `requires`

    requires "semantics/controls.k"

- Line 50; `requires`

    requires "semantics/functions.k"

- Line 51; `requires`

    requires "semantics/builtins.k"

- Line 52; `requires`

    requires "semantics/call.k"

- Line 53; `requires`

    requires "semantics/sort.k"

- Line 54; `requires`

    requires "semantics/assert.k"

- Line 55; `requires`

    requires "semantics/dict.k"

- Line 56; `requires`

    requires "semantics/concrete.k"

- Line 58; `module`

    module MPY

- Line 59; `imports`

      imports MPY-CORE

- Line 60; `imports`

      imports MPY-ITER

- Line 61; `imports`

      imports MPY-RANGE

- Line 62; `imports`

      imports MPY-OPERATORS

- Line 63; `imports`

      imports MPY-INT

- Line 64; `imports`

      imports MPY-BOOL

- Line 65; `imports`

      imports MPY-FLOAT

- Line 66; `imports`

      imports MPY-STR

- Line 67; `imports`

      imports MPY-SET

- Line 68; `imports`

      imports MPY-LIST

- Line 69; `imports`

      imports MPY-TUPLE

- Line 70; `imports`

      imports MPY-SUBSCRIPT

- Line 71; `imports`

      imports MPY-COMPREHENSION

- Line 72; `imports`

      imports MPY-METHODS

- Line 73; `imports`

      imports MPY-CONTROLS

- Line 74; `imports`

      imports MPY-FUNCTIONS

- Line 75; `imports`

      imports MPY-BUILTINS

- Line 76; `imports`

      imports MPY-CALL

- Line 77; `imports`

      imports MPY-SORT

- Line 78; `imports`

      imports MPY-ASSERT

- Line 79; `imports`

      imports MPY-DICT

- Line 80; `endmodule`

    endmodule

- Line 87; `module`

    module MPY-KRUN

- Line 88; `imports`

      imports MPY

- Line 89; `imports`

      imports MPY-CONCRETE

- Line 90; `endmodule`

    endmodule

### `reference-semantics/semantics/assert.k`

- Line 3; `module`

    module MPY-ASSERT

- Line 4; `imports`

      imports MPY-CORE

- Line 6; `rule`

      rule <k> Assert(V:Val) => .K ... </k>
           requires truthy(V)

- Line 8; `rule`

      rule <k> Assert(V:Val) ~> _ => .K </k>
           <exc> NoExc => AssertionError </exc>
           <exit-code> _ => 1 </exit-code>
           requires notBool truthy(V)

- Line 13; `rule`

      rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 16; `endmodule`

    endmodule

### `reference-semantics/semantics/bool.k`

- Line 5; `module`

    module MPY-BOOL

- Line 6; `imports`

      imports MPY-CORE

- Line 8; `rule`

      rule applyUn("not", V:Val) => notBool truthy(V)

- Line 10; `rule`

      rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2

- Line 11; `rule`

      rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2

- Line 16; `context`

      context BoolOp(_, (HOLE:Expr, _:Exprs))

- Line 17; `rule`

      rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>

- Line 18; `rule`

      rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
           requires truthy(V)

- Line 20; `rule`

      rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
           requires notBool truthy(V)

- Line 22; `rule`

      rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
           requires truthy(V)

- Line 24; `rule`

      rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
           requires notBool truthy(V)

- Line 29; `rule`

      rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
           [priority(40)]

- Line 31; `rule`

      rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires truthy(V)
           [priority(40)]

- Line 35; `rule`

      rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool truthy(V)
           [priority(40)]

- Line 39; `rule`

      rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires truthy(V)
           [priority(40)]

- Line 43; `rule`

      rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool truthy(V)
           [priority(40)]

- Line 47; `endmodule`

    endmodule

### `reference-semantics/semantics/builtins.k`

- Line 3; `module`

    module MPY-BUILTINS

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports MPY-STR

- Line 6; `imports`

      imports MPY-SET

- Line 7; `imports`

      imports MPY-ITER

- Line 8; `imports`

      imports MPY-RANGE

- Line 9; `imports`

      imports MPY-INT

- Line 10; `imports`

      imports MPY-METHODS

- Line 17; `syntax`

      syntax Val ::= applyBuiltin(String, Vals) [function]

- Line 20; `syntax`

      syntax Int ::= seqLen(Val) [function]

- Line 21; `rule`

      rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)

- Line 22; `rule`

      rule seqLen(list(VS:ValSeq))                  => vsLen(VS)

- Line 23; `rule`

      rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)

- Line 24; `rule`

      rule seqLen(str(IS:IntSeq))                   => isLen(IS)

- Line 25; `rule`

      rule seqLen(setV(DS:IntSeq))                  => isLen(DS)

- Line 26; `rule`

      rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)

- Line 32; `rule`

      rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>

- Line 33; `rule`

      rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>

- Line 34; `rule`

      rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>

- Line 35; `rule`

      rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>

- Line 36; `syntax`

      syntax ValSeq ::= charsOf(IntSeq) [function, total]

- Line 37; `rule`

      rule charsOf(.IntSeq)                => .ValSeq

- Line 38; `rule`

      rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))

- Line 41; `rule`

      rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))

- Line 44; `rule`

      rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)

- Line 47; `syntax`

      syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)

- Line 48; `rule`

      rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>

- Line 49; `rule`

      rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>

- Line 50; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
            => #sumAcc(R, ACC +Int intOf(V)) ... </k>
           requires isInt(V) orBool isBool(V)

- Line 54; `syntax`

      syntax Int ::= intOf(Val) [function]

- Line 55; `rule`

      rule intOf(I:Int)  => I

- Line 56; `rule`

      rule intOf(B:Bool) => #if B #then 1 #else 0 #fi

- Line 59; `syntax`

      syntax KItem ::= #allAcc(Iterable) | "#allCont"

- Line 60; `rule`

      rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>

- Line 61; `rule`

      rule <k> #iterDone ~> #allCont => true ... </k>

- Line 62; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
           requires truthy(V)

- Line 64; `rule`

      rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
           requires notBool truthy(V)

- Line 67; `syntax`

      syntax KItem ::= #anyAcc(Iterable) | "#anyCont"

- Line 68; `rule`

      rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>

- Line 69; `rule`

      rule <k> #iterDone ~> #anyCont => false ... </k>

- Line 70; `rule`

      rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
           requires truthy(V)

- Line 72; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
           requires notBool truthy(V)

- Line 76; `syntax`

      syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)

- Line 77; `rule`

      rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>

- Line 78; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
           requires isInt(V)

- Line 80; `rule`

      rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>

- Line 81; `rule`

      rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>

- Line 82; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
            => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
           requires isInt(V)

- Line 86; `syntax`

      syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)

- Line 87; `rule`

      rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>

- Line 88; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
           requires isInt(V)

- Line 90; `rule`

      rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>

- Line 91; `rule`

      rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>

- Line 92; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
            => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
           requires isInt(V)

- Line 97; `syntax`

      syntax Int ::= maxVals(Int, Vals) [function]

- Line 98; `rule`

      rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)

- Line 99; `rule`

      rule maxVals(M:Int, .Vals)           => M

- Line 100; `rule`

      rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)

- Line 102; `syntax`

      syntax Int ::= minVals(Int, Vals) [function]

- Line 103; `rule`

      rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)

- Line 104; `rule`

      rule minVals(M:Int, .Vals)           => M

- Line 105; `rule`

      rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)

- Line 108; `rule`

      rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
           requires N >=Int 0

- Line 111; `rule`

      rule applyBuiltin("bin", N:Int, .Vals)
        => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
           requires N <Int 0

- Line 114; `syntax`

      syntax IntSeq ::= binCodes(Int) [function, total]

- Line 115; `rule`

      rule binCodes(0) => iCons(48, .IntSeq)

- Line 116; `rule`

      rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0

- Line 117; `syntax`

      syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]

- Line 118; `rule`

      rule binAcc(0, ACC:IntSeq) => ACC

- Line 119; `rule`

      rule binAcc(N:Int, ACC:IntSeq)
        => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
           requires N >Int 0

- Line 124; `rule`

      rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
            => #alloc(list(enumVS(VS, 0))) ... </k>

- Line 126; `syntax`

      syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]

- Line 127; `rule`

      rule enumVS(.ValSeq, _:Int) => .ValSeq

- Line 128; `rule`

      rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
        => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))

- Line 132; `rule`

      rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
            => #alloc(list(mapStrVS(VS))) ... </k>

- Line 134; `syntax`

      syntax ValSeq ::= mapStrVS(ValSeq) [function, total]

- Line 135; `rule`

      rule mapStrVS(.ValSeq) => .ValSeq

- Line 136; `rule`

      rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))

- Line 137; `rule`

      rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))

- Line 140; `rule`

      rule applyBuiltin("int", I:Int, .Vals) => I

- Line 143; `rule`

      rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C

- Line 144; `rule`

      rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
           requires 0 <=Int I andBool I <Int 128

- Line 148; `rule`

      rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))

- Line 149; `rule`

      rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)

- Line 152; `rule`

      rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
           requires 48 <=Int C andBool C <=Int 57

- Line 156; `rule`

      rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
           requires isLen(CS) >=Int 2

- Line 158; `syntax`

      syntax Int ::= intDigAcc(IntSeq, Int) [function, total]

- Line 159; `rule`

      rule intDigAcc(.IntSeq, ACC:Int)             => ACC

- Line 160; `rule`

      rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))

- Line 163; `rule`

      rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)

- Line 164; `rule`

      rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)

- Line 167; `rule`

      rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
            => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>

- Line 169; `rule`

      rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>

- Line 170; `rule`

      rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>

- Line 171; `rule`

      rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
            => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>

- Line 173; `rule`

      rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>

- Line 174; `rule`

      rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>

- Line 177; `rule`

      rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)

- Line 178; `rule`

      rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)

- Line 179; `rule`

      rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
           requires S =/=Int 0

- Line 187; `rule`

      rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)

- Line 188; `syntax`

      syntax Int ::= evalArith(IntSeq) [function]

- Line 189; `rule`

      rule evalArith(CS:IntSeq)
        => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))

- Line 192; `syntax`

      syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)

- Line 194; `syntax`

      syntax Bool ::= evDigit(Int) [function, total]

- Line 195; `rule`

      rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57

- Line 196; `syntax`

      syntax Bool ::= evHead42(IntSeq) [function, total]

- Line 197; `rule`

      rule evHead42(iCons(42, _:IntSeq)) => true

- Line 198; `rule`

      rule evHead42(_:IntSeq)            => false [owise]

- Line 199; `syntax`

      syntax Bool ::= evHead47(IntSeq) [function, total]

- Line 200; `rule`

      rule evHead47(iCons(47, _:IntSeq)) => true

- Line 201; `rule`

      rule evHead47(_:IntSeq)            => false [owise]

- Line 203; `syntax`

      syntax OpSeq ::= tokOps(IntSeq) [function, total]

- Line 204; `rule`

      rule tokOps(.IntSeq)                 => .OpSeq

- Line 205; `rule`

      rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)

- Line 206; `rule`

      rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)

- Line 207; `rule`

      rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))

- Line 208; `rule`

      rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)

- Line 209; `rule`

      rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))

- Line 210; `rule`

      rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)

- Line 211; `rule`

      rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))

- Line 212; `rule`

      rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))

- Line 214; `syntax`

      syntax IntSeq ::= tokNds(IntSeq) [function, total]
                      | tokNdAcc(Int, IntSeq) [function, total]

- Line 216; `rule`

      rule tokNds(.IntSeq)                => .IntSeq

- Line 217; `rule`

      rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)

- Line 218; `rule`

      rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)

- Line 219; `rule`

      rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
           requires notBool evDigit(C) andBool C =/=Int 32

- Line 221; `rule`

      rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
           requires evDigit(C)

- Line 223; `rule`

      rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]

- Line 225; `syntax`

      syntax EvPair ::= evp(OpSeq, IntSeq)

- Line 226; `syntax`

      syntax Int ::= firstNdE(EvPair) [function, total]

- Line 227; `rule`

      rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N

- Line 228; `rule`

      rule firstNdE(_:EvPair) => 0 [owise]

- Line 230; `syntax`

      syntax Int ::= applyOpE(String, Int, Int) [function, total]

- Line 231; `rule`

      rule applyOpE("+",  A:Int, B:Int) => A +Int B

- Line 232; `rule`

      rule applyOpE("-",  A:Int, B:Int) => A -Int B

- Line 233; `rule`

      rule applyOpE("*",  A:Int, B:Int) => A *Int B

- Line 234; `rule`

      rule applyOpE("//", A:Int, B:Int) => A divInt B

- Line 235; `rule`

      rule applyOpE("**", A:Int, B:Int) => A ^Int B

- Line 236; `rule`

      rule applyOpE(_:String, A:Int, _:Int) => A [owise]

- Line 238; `syntax`

      syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]

- Line 239; `rule`

      rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)

- Line 240; `rule`

      rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))

- Line 241; `rule`

      rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
           requires O =/=String "**"

- Line 243; `rule`

      rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]

- Line 244; `syntax`

      syntax EvPair ::= powCombE(Int, EvPair) [function, total]

- Line 245; `rule`

      rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))

- Line 246; `rule`

      rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))

- Line 247; `syntax`

      syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]

- Line 248; `rule`

      rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))

- Line 250; `syntax`

      syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]

- Line 251; `rule`

      rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)

- Line 252; `rule`

      rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)

- Line 253; `rule`

      rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)

- Line 254; `rule`

      rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)

- Line 255; `syntax`

      syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]

- Line 256; `rule`

      rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))

- Line 257; `rule`

      rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
        => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
           requires inLevelE(L, O)

- Line 260; `rule`

      rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
        => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
           requires notBool inLevelE(L, O)

- Line 263; `rule`

      rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
        => evp(OO, appendIE(ON, CUR)) [owise]

- Line 265; `syntax`

      syntax Bool ::= inLevelE(String, String) [function, total]

- Line 266; `rule`

      rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"

- Line 267; `rule`

      rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"

- Line 268; `rule`

      rule inLevelE(_:String, _:String) => false [owise]

- Line 269; `syntax`

      syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]

- Line 270; `rule`

      rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)

- Line 271; `rule`

      rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))

- Line 272; `syntax`

      syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]

- Line 273; `rule`

      rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)

- Line 274; `rule`

      rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))

- Line 279; `syntax`

      syntax KItem ::= "#md5"

- Line 280; `rule`

      rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
           [priority(40)]

- Line 282; `rule`

      rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>

- Line 283; `syntax`

      syntax Val ::= md5Obj(IntSeq)

- Line 284; `rule`

      rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))

- Line 285; `syntax`

      syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]

- Line 291; `rule`

      rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)

- Line 292; `rule`

      rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)

- Line 293; `syntax`

      syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]

- Line 294; `rule`

      rule isIntV(_:Int)         => true

- Line 295; `rule`

      rule isIntV(_:Val)         => false [owise]

- Line 296; `rule`

      rule isStrV(str(_:IntSeq)) => true

- Line 297; `rule`

      rule isStrV(_:Val)         => false [owise]

- Line 298; `endmodule`

    endmodule

### `reference-semantics/semantics/call.k`

- Line 10; `module`

    module MPY-CALL

- Line 11; `imports`

      imports MPY-METHODS

- Line 12; `imports`

      imports MPY-BUILTINS

- Line 13; `imports`

      imports MPY-FUNCTIONS

- Line 16; `rule`

      rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>

- Line 19; `syntax`

      syntax KItem ::= #callee(Exprs)

- Line 20; `rule`

      rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]

- Line 21; `rule`

      rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>

- Line 24; `rule`

      rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>

- Line 26; `rule`

      rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>

- Line 27; `rule`

      rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>

- Line 28; `rule`

      rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>

- Line 29; `rule`

      rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>

- Line 30; `rule`

      rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>

- Line 31; `rule`

      rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]

- Line 32; `rule`

      rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>

- Line 38; `rule`

      rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
            => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 42; `rule`

      rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
            => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isRefV(A)
           [priority(40)]

- Line 47; `rule`

      rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
            => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 52; `syntax`

      syntax Bool ::= isMutMethod(String) [function, total]

- Line 53; `rule`

      rule isMutMethod(M:String)
        => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
           orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"

- Line 56; `rule`

      rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
            => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isMutMethod(M)
           [priority(40)]

- Line 63; `rule`

      rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
            => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
           [priority(40)]

- Line 69; `rule`

      rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
            => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
           <env>     CALLERL:Int => NEWL </env>
           <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
           <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
           <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>

- Line 80; `rule`

      rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
            => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
           <env>     CALLERL:Int => NEWL </env>
           <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
           <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
           <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>

- Line 87; `syntax`

      syntax KItem ::= #allocCells(ParamNames)

- Line 88; `rule`

      rule <k> #allocCells(.ParamNames) => .K ... </k>

- Line 89; `rule`

      rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
           <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
           <heapLoc> N:Int => N +Int 1 </heapLoc>
           requires notBool N in_keys(H)

- Line 95; `endmodule`

    endmodule

### `reference-semantics/semantics/comprehension.k`

- Line 3; `module`

    module MPY-COMPREHENSION

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports MPY-OPERATORS

- Line 6; `imports`

      imports MPY-LIST

- Line 7; `imports`

      imports MPY-CONTROLS

- Line 8; `imports`

      imports MPY-FUNCTIONS

- Line 11; `rule`

      rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)

- Line 12; `rule`

      rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)

- Line 14; `syntax`

      syntax Stmts ::= compBody(CompFors, Expr) [macro]

- Line 15; `rule`

      rule compBody(Gs:CompFors, ELT:Expr)
        => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))

- Line 18; `syntax`

      syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]

- Line 19; `rule`

      rule compNest(.CompFors, ELT:Expr)
        => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))

- Line 21; `rule`

      rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
        => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))

- Line 24; `syntax`

      syntax Expr ::= compGuard(Exprs) [macro]

- Line 25; `rule`

      rule compGuard(.Exprs)             => Bool(true)

- Line 26; `rule`

      rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))

- Line 27; `endmodule`

    endmodule

### `reference-semantics/semantics/concrete.k`

- Line 8; `module`

    module MPY-CONCRETE

- Line 9; `imports`

      imports MPY

- Line 13; `rule`

      rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
           <heap> HP:Map </heap>
           requires hasRefVS(A) orBool hasRefVS(B)

- Line 16; `rule`

      rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
           <heap> HP:Map </heap>
           requires hasRefVS(A) orBool hasRefVS(B)

- Line 25; `syntax`

      syntax Val ::= kvP(Val, Val)

- Line 26; `syntax`

      syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                     | #ksIns(Val, ValSeq, Val, ValSeq, Bool)

- Line 28; `rule`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
            => #ksort(VS, KV, .ValSeq, false) ... </k>
           [priority(40)]

- Line 31; `rule`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
            => #ksort(VS, KV, .ValSeq, RB) ... </k>
           [priority(40)]

- Line 34; `rule`

      rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
            => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>

- Line 36; `rule`

      rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
            => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>

- Line 38; `rule`

      rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
            => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
           requires notBool isKwV(K)

- Line 42; `syntax`

      syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]

- Line 43; `rule`

      rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)

- Line 44; `rule`

      rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
        => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
           requires kLt(K, K2)

- Line 47; `rule`

      rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
        => vCons(kvP(K2, V2), insPair(R, K, V))
           requires notBool kLt(K, K2)

- Line 51; `syntax`

      syntax Bool ::= kLt(Val, Val) [function]

- Line 52; `rule`

      rule kLt(I1:Int, I2:Int)             => I1 <Int I2

- Line 53; `rule`

      rule kLt(F1:Float, F2:Float)         => F1 <Float F2

- Line 54; `rule`

      rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)

- Line 56; `syntax`

      syntax ValSeq ::= unpairVS(ValSeq) [function, total]

- Line 57; `rule`

      rule unpairVS(.ValSeq) => .ValSeq

- Line 58; `rule`

      rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))

- Line 59; `rule`

      rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]

- Line 60; `endmodule`

    endmodule

### `reference-semantics/semantics/controls.k`

- Line 3; `module`

    module MPY-CONTROLS

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports MPY-TUPLE

- Line 6; `imports`

      imports MPY-ITER

- Line 9; `rule`

      rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>

- Line 12; `rule`

      rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires "$cells" in_keys(M)
            andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
            andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
           [priority(40)]

- Line 20; `rule`

      rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
           requires X in_keys(M)

- Line 27; `rule`

      rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires X in_keys(M) andBool isRefV({M[X]}:>Val)
           [priority(40)]

- Line 35; `rule`

      rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>

- Line 36; `rule`

      rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]

- Line 37; `syntax`

      syntax KItem ::= #bindImports(ParamNames)

- Line 38; `rule`

      rule <k> #bindImports(.ParamNames) => .K ... </k>

- Line 39; `rule`

      rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
           requires N ==String "floor" orBool N ==String "ceil"

- Line 43; `rule`

      rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
           requires notBool (N ==String "floor" orBool N ==String "ceil")

- Line 48; `rule`

      rule <k> Expr(_:Val) => .K ... </k>

- Line 51; `syntax`

      syntax KItem ::= #branch(Bool, Stmts, Stmts)

- Line 52; `rule`

      rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>

- Line 53; `rule`

      rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>

- Line 54; `rule`

      rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>

- Line 57; `rule`

      rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
           requires truthy(V)

- Line 59; `rule`

      rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
           requires notBool truthy(V)

- Line 65; `syntax`

      syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                     | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                     | #loopLbl(K) | "#cont" | "#brk"

- Line 69; `rule`

      rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>

- Line 71; `rule`

      rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>

- Line 72; `rule`

      rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>

- Line 73; `rule`

      rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
            => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>

- Line 77; `rule`

      rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>

- Line 78; `rule`

      rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>

- Line 79; `rule`

      rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
           requires truthy(V)

- Line 81; `rule`

      rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
           requires notBool truthy(V)

- Line 85; `rule`

      rule <k> #loopLbl(NEXT:K) => NEXT ... </k>

- Line 86; `rule`

      rule <k> Continue => #cont ... </k>

- Line 87; `rule`

      rule <k> Break => #brk ... </k>

- Line 88; `rule`

      rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>

- Line 89; `rule`

      rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]

- Line 90; `rule`

      rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>

- Line 91; `rule`

      rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]

- Line 95; `rule`

      rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 98; `rule`

      rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 101; `rule`

      rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 106; `rule`

      rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 109; `endmodule`

    endmodule

### `reference-semantics/semantics/core.k`

- Line 3; `module`

    module MPY-CORE

- Line 4; `imports`

      imports MPY-SYNTAX

- Line 5; `imports`

      imports INT

- Line 6; `imports`

      imports BOOL

- Line 7; `imports`

      imports STRING

- Line 8; `imports`

      imports MAP

- Line 9; `imports`

      imports LIST

- Line 10; `imports`

      imports K-EQUAL

- Line 13; `syntax`

      syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

- Line 14; `syntax`

      syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)

- Line 15; `syntax`

      syntax Str    ::= str(IntSeq)

- Line 18; `syntax`

      syntax Iterable ::= list(ValSeq)
                        | tuple(ValSeq)
                        | Str
                        | rangeObj(Int, Int, Int)
                        | zipObj(ValSeq, ValSeq)
                        | zipObjS(IntSeq, IntSeq)

- Line 25; `syntax`

      syntax Val      ::= Int
                        | Bool
                        | "noneV"
                        | Iterable
                        | ref(Int)          // a heap object: <heap> holds its list(VS)
                        | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
                        | closureVal(ParamNames, Stmts, Int)
                        | typeV(String)     // a type object (int/str), resolved from the builtins frame
                        | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
                        | boundMethodV(Val, String)   // a cooled Attribute: obj.method

- Line 36; `syntax`

      syntax Parent   ::= "root" | parent(Int)

- Line 37; `syntax`

      syntax Scope    ::= scope(Map, Parent)

- Line 38; `syntax`

      syntax KResult  ::= Val

- Line 39; `syntax`

      syntax Expr     ::= Val   // cooling puts results back into expression holes

- Line 40; `syntax`

      syntax Vals     ::= List{Val, ","}

- Line 41; `syntax`

      syntax Exc      ::= "NoExc" | "AssertionError"

- Line 42; `syntax`

      syntax RetState ::= "noRet" | retV(Val)

- Line 49; `configuration`

      configuration
        <k>       #loadAll($PGM:Module) </k>
        <env>     0 </env>
        <scopes>   0     |-> scope(.Map, parent(-1))
                  -1    |-> builtinsScope </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap>    .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack>   .List </stack>
        <ret>     noRet </ret>
        <exc>     NoExc </exc>
        <exit-code exit=""> 0 </exit-code>

- Line 68; `syntax`

      syntax Bool ::= isRefV(Val) [function, total]

- Line 69; `rule`

      rule isRefV(ref(_:Int)) => true

- Line 70; `rule`

      rule isRefV(_:Val)      => false [owise]

- Line 75; `syntax`

      syntax HeapVal ::= cellV(Val)

- Line 76; `syntax`

      syntax Bool ::= isCellRef(Val) [function, total]

- Line 77; `rule`

      rule isCellRef(cellRef(_:Int)) => true

- Line 78; `rule`

      rule isCellRef(_:Val)          => false [owise]

- Line 85; `rule`

      rule <k> cellRef(H:Int) => V ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           <heap> ... H |-> cellV(V:Val) ... </heap>
           requires "$cells" in_keys(M)
           [priority(40)]

- Line 95; `syntax`

      syntax Val ::= kwV(String, Val)

- Line 96; `syntax`

      syntax KItem ::= #kwTag(String)

- Line 97; `rule`

      rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>

- Line 98; `rule`

      rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
           requires notBool isKwV(V)

- Line 100; `syntax`

      syntax Bool ::= isKwV(Val) [function, total]

- Line 101; `rule`

      rule isKwV(kwV(_:String, _:Val)) => true

- Line 102; `rule`

      rule isKwV(_:Val)                => false [owise]

- Line 106; `syntax`

      syntax Val ::= cellsMark(ParamNames)

- Line 107; `syntax`

      syntax ParamNames ::= cellsOf(Val) [function]

- Line 108; `rule`

      rule cellsOf(cellsMark(CVS:ParamNames)) => CVS

- Line 109; `syntax`

      syntax Bool ::= pnMember(String, ParamNames) [function, total]

- Line 110; `rule`

      rule pnMember(_:String, .ParamNames) => false

- Line 111; `rule`

      rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)

- Line 113; `syntax`

      syntax KItem ::= #cellW(Val, Val)

- Line 114; `rule`

      rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
           <heap> ... H |-> cellV(_:Val => V) ... </heap>

- Line 117; `syntax`

      syntax KItem ::= #alloc(Val)

- Line 118; `rule`

      rule <k> #alloc(V:Val) => ref(N) ... </k>
           <heap>    H:Map => (N |-> V) H </heap>
           <heapLoc> N:Int => N +Int 1 </heapLoc>
           requires notBool N in_keys(H)

- Line 124; `syntax`

      syntax KItem ::= #loadAll(Module)

- Line 125; `rule`

      rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>

- Line 126; `rule`

      rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>

- Line 127; `rule`

      rule <k> .Stmts => .K ... </k>

- Line 130; `syntax`

      syntax KItem ::= #look(String, Int)

- Line 131; `rule`

      rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>

- Line 132; `rule`

      rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
           <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
           requires X in_keys(M)

- Line 145; `rule`

      rule <k> #look(X:String, L:Int) => V ... </k>
           <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
           <heap> ... H |-> cellV(V:Val) ... </heap>
           requires X in_keys(M) andBool "$cells" in_keys(M)
            andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
            andBool {M[X]}:>Val ==K cellRef(H)
           [priority(40)]

- Line 152; `rule`

      rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
           <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
           requires notBool (X in_keys(M))

- Line 157; `syntax`

      syntax Scope ::= "builtinsScope" [function, total]

- Line 158; `rule`

      rule builtinsScope
        => scope(.Map [ "len"    <- builtinV("len")    ]
                      [ "set"    <- builtinV("set")    ]
                      [ "sum"    <- builtinV("sum")    ]
                      [ "abs"    <- builtinV("abs")    ]
                      [ "min"    <- builtinV("min")    ]
                      [ "max"    <- builtinV("max")    ]
                      [ "ord"    <- builtinV("ord")    ]
                      [ "chr"    <- builtinV("chr")    ]
                      [ "range"  <- builtinV("range")  ]
                      [ "all"    <- builtinV("all")    ]
                      [ "any"    <- builtinV("any")    ]
                      [ "zip"    <- builtinV("zip")    ]
                      [ "isinstance" <- builtinV("isinstance") ]
                      [ "sorted" <- builtinV("sorted") ]
                      [ "list"   <- builtinV("list")   ]
                      [ "round"  <- builtinV("round")  ]
                      [ "bin"    <- builtinV("bin")    ]
                      [ "enumerate" <- builtinV("enumerate") ]
                      [ "map"    <- builtinV("map")    ]
                      [ "eval"   <- builtinV("eval")   ]
                      [ "int"    <- typeV("int")       ]
                      [ "str"    <- typeV("str")       ]
                      [ "float"  <- typeV("float")     ], root)

- Line 185; `syntax`

      syntax ApplyK ::= toCall(Val)

- Line 186; `syntax`

      syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                      | #evalArgCont(Exprs, Vals, ApplyK)
                      | #applyK(ApplyK, Vals)

- Line 189; `rule`

      rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>

- Line 190; `rule`

      rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>

- Line 191; `rule`

      rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>

- Line 194; `rule`

      rule <k> Int(I:Int)   => I ... </k>

- Line 195; `rule`

      rule <k> Bool(B:Bool) => B ... </k>

- Line 196; `rule`

      rule <k> NoneVal      => noneV ... </k>

- Line 199; `syntax`

      syntax Bool ::= truthy(Val) [function]

- Line 200; `rule`

      rule truthy(B:Bool)          => B

- Line 201; `rule`

      rule truthy(noneV)           => false

- Line 202; `rule`

      rule truthy(I:Int)           => I =/=Int 0

- Line 203; `rule`

      rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)

- Line 204; `rule`

      rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)

- Line 205; `rule`

      rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)

- Line 208; `syntax`

      syntax Val  ::= applyUn(String, Val) [function]

- Line 209; `syntax`

      syntax Val  ::= applyBin(String, Val, Val) [function]

- Line 210; `syntax`

      syntax Bool ::= applyCmp(String, Val, Val) [function]

- Line 213; `syntax`

      syntax Vals ::= appendVal(Vals, Val) [function, total]

- Line 214; `rule`

      rule appendVal(.Vals, V:Val)              => V , .Vals

- Line 215; `rule`

      rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)

- Line 217; `syntax`

      syntax ValSeq ::= vals2valSeq(Vals) [function, total]

- Line 218; `rule`

      rule vals2valSeq(.Vals)            => .ValSeq

- Line 219; `rule`

      rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))

- Line 223; `syntax`

      syntax Int ::= vsLen(ValSeq) [function, total]

- Line 224; `rule`

      rule vsLen(.ValSeq)                => 0

- Line 225; `rule`

      rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)

- Line 227; `syntax`

      syntax Int ::= isLen(IntSeq) [function, total]

- Line 228; `rule`

      rule isLen(.IntSeq)                => 0

- Line 229; `rule`

      rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)

- Line 233; `syntax`

      syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]

- Line 234; `rule`

      rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq

- Line 235; `rule`

      rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)

- Line 236; `rule`

      rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
           requires I >Int 0

- Line 238; `rule`

      rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
           requires I <Int 0

- Line 240; `endmodule`

    endmodule

### `reference-semantics/semantics/dict.k`

- Line 13; `module`

    module MPY-DICT

- Line 14; `imports`

      imports MPY-CORE

- Line 15; `imports`

      imports MPY-ITER

- Line 16; `imports`

      imports MPY-METHODS

- Line 17; `imports`

      imports MPY-LIST

- Line 20; `syntax`

      syntax Val ::= dictV(ValSeq, ValSeq)

- Line 23; `syntax`

      syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                     | #dictKey(Expr, Entries, ValSeq, ValSeq)
                     | #dictVal(Val, Entries, ValSeq, ValSeq)

- Line 26; `rule`

      rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>

- Line 27; `rule`

      rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>

- Line 28; `rule`

      rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
            => K ~> #dictKey(V, REST, KS, VS) ... </k>

- Line 30; `rule`

      rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
            => V ~> #dictVal(KV, REST, KS, VS) ... </k>

- Line 32; `rule`

      rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
            => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>

- Line 37; `syntax`

      syntax Bool ::= dHasKey(ValSeq, Val) [function, total]

- Line 38; `rule`

      rule dHasKey(.ValSeq, _:Val)                => false

- Line 39; `rule`

      rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K

- Line 40; `rule`

      rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)

- Line 43; `syntax`

      syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]

- Line 44; `rule`

      rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)

- Line 45; `rule`

      rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)

- Line 49; `syntax`

      syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]

- Line 50; `rule`

      rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
           requires A ==K K

- Line 52; `rule`

      rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
           requires notBool (A ==K K)

- Line 54; `rule`

      rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]

- Line 58; `rule`

      rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
            => #alloc(list(KS)) ... </k>
           [priority(40)]

- Line 63; `rule`

      rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)

- Line 64; `syntax`

      syntax Val ::= applyIndexD(Val, Val) [function]

- Line 65; `rule`

      rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
           [priority(45)]

- Line 70; `syntax`

      syntax Val ::= dictSet(Val, Val, Val) [function]

- Line 71; `rule`

      rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))

- Line 76; `syntax`

      syntax KItem ::= #dsetK(String, Val)

- Line 77; `rule`

      rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>

- Line 78; `rule`

      rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
           requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)

- Line 82; `rule`

      rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires X in_keys(M) andBool isRefV({M[X]}:>Val)

- Line 86; `syntax`

      syntax KItem ::= #dsetV(Val, Val, Val)

- Line 87; `rule`

      rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
           <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>

- Line 90; `syntax`

      syntax Int ::= normIdxD(Int, Int) [function, total]

- Line 91; `rule`

      rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0

- Line 92; `rule`

      rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0

- Line 95; `rule`

      rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
        => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)

- Line 97; `syntax`

      syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]

- Line 98; `rule`

      rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true

- Line 99; `rule`

      rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
        => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)

- Line 101; `syntax`

      syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]

- Line 102; `rule`

      rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K

- Line 103; `rule`

      rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)

- Line 104; `endmodule`

    endmodule

### `reference-semantics/semantics/float.k`

- Line 14; `module`

    module MPY-FLOAT

- Line 15; `imports`

      imports MPY-OPERATORS

- Line 16; `imports`

      imports MPY-BUILTINS

- Line 17; `imports`

      imports FLOAT

- Line 20; `syntax`

      syntax Val ::= Float

- Line 21; `rule`

      rule <k> Float(F:Float) => F ... </k>

- Line 24; `syntax`

      syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]

- Line 25; `rule`

      rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]

- Line 27; `rule`

      rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)

- Line 30; `syntax`

      syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]

- Line 31; `rule`

      rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]

- Line 32; `rule`

      rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)

- Line 37; `syntax`

      syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]

- Line 38; `rule`

      rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]

- Line 39; `rule`

      rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)

- Line 43; `rule`

      rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2

- Line 44; `rule`

      rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)

- Line 50; `syntax`

      syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]

- Line 51; `rule`

      rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]

- Line 52; `rule`

      rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)

- Line 54; `syntax`

      syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]

- Line 55; `rule`

      rule absF(F:Float) => absFloat(F) [concrete]

- Line 56; `rule`

      rule applyBuiltin("abs", F:Float, .Vals) => absF(F)

- Line 61; `rule`

      rule <k> Import(_:String) => .K ... </k>

- Line 65; `syntax`

      syntax KItem ::= "#mathCeil"

- Line 66; `rule`

      rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]

- Line 67; `rule`

      rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>

- Line 70; `syntax`

      syntax KItem ::= "#mathFloor"

- Line 71; `rule`

      rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]

- Line 72; `rule`

      rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>

- Line 73; `syntax`

      syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]

- Line 74; `rule`

      rule floorFI(I:Int)   => I                        [concrete]

- Line 75; `rule`

      rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]

- Line 78; `rule`

      rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)

- Line 79; `rule`

      rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)

- Line 82; `syntax`

      syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)

- Line 83; `rule`

      rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]

- Line 84; `rule`

      rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>

- Line 85; `rule`

      rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>

- Line 86; `syntax`

      syntax Float ::= toF(Val) [function, total, symbol(toF)]

- Line 87; `rule`

      rule toF(F:Float) => F        [concrete]

- Line 88; `rule`

      rule toF(I:Int)   => intToF(I) [concrete]

- Line 93; `syntax`

      syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]

- Line 94; `rule`

      rule ceilF(I:Int)   => I                       [concrete]

- Line 95; `rule`

      rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]

- Line 99; `rule`

      rule applyUn("-", F:Float) => 0.0 -Float F

- Line 103; `syntax`

      syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]

- Line 104; `rule`

      rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]

- Line 105; `rule`

      rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)

- Line 107; `syntax`

      syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]

- Line 108; `rule`

      rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]

- Line 109; `rule`

      rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)

- Line 111; `syntax`

      syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]

- Line 112; `rule`

      rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]

- Line 113; `rule`

      rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)

- Line 115; `syntax`

      syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]

- Line 116; `rule`

      rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]

- Line 117; `rule`

      rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)

- Line 119; `syntax`

      syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]

- Line 120; `rule`

      rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]

- Line 121; `rule`

      rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)

- Line 125; `syntax`

      syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]

- Line 126; `rule`

      rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]

- Line 127; `rule`

      rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)

- Line 128; `rule`

      rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)

- Line 129; `rule`

      rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)

- Line 132; `rule`

      rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)

- Line 133; `rule`

      rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))

- Line 134; `rule`

      rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)

- Line 135; `rule`

      rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))

- Line 136; `rule`

      rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)

- Line 137; `rule`

      rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))

- Line 138; `rule`

      rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)

- Line 139; `rule`

      rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))

- Line 142; `syntax`

      syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]

- Line 143; `rule`

      rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]

- Line 144; `rule`

      rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)

- Line 145; `rule`

      rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))

- Line 146; `rule`

      rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)

- Line 147; `rule`

      rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))

- Line 148; `rule`

      rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)

- Line 149; `rule`

      rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))

- Line 150; `rule`

      rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)

- Line 151; `rule`

      rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))

- Line 154; `rule`

      rule applyCmp("==", V:Val, noneV) => V ==K noneV

- Line 155; `rule`

      rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)

- Line 160; `syntax`

      syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]

- Line 161; `rule`

      rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]

- Line 162; `rule`

      rule decStrToF(CS:IntSeq)
        => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
           requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]

- Line 165; `syntax`

      syntax Int ::= headIS(IntSeq) [function]

- Line 166; `rule`

      rule headIS(iCons(C:Int, _:IntSeq)) => C

- Line 167; `syntax`

      syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]

- Line 168; `rule`

      rule intPart(CS:IntSeq) => intPartAcc(CS, 0)

- Line 169; `rule`

      rule intPartAcc(.IntSeq, A:Int) => A

- Line 170; `rule`

      rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A

- Line 171; `rule`

      rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
           requires C =/=Int 46

- Line 173; `syntax`

      syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]

- Line 174; `rule`

      rule fracPart(.IntSeq) => 0

- Line 175; `rule`

      rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)

- Line 176; `rule`

      rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46

- Line 177; `rule`

      rule fracAcc(.IntSeq, A:Int) => A

- Line 178; `rule`

      rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))

- Line 179; `syntax`

      syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]

- Line 180; `rule`

      rule fracScale(.IntSeq) => 1

- Line 181; `rule`

      rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)

- Line 182; `rule`

      rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46

- Line 183; `rule`

      rule fscAcc(.IntSeq, A:Int) => A

- Line 184; `rule`

      rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)

- Line 185; `rule`

      rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)

- Line 186; `rule`

      rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)

- Line 187; `rule`

      rule applyBuiltin("float", F:Float, .Vals)        => F

- Line 190; `syntax`

      syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]

- Line 191; `rule`

      rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]

- Line 192; `rule`

      rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)

- Line 195; `syntax`

      syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]

- Line 196; `rule`

      rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]

- Line 197; `rule`

      rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)

- Line 198; `rule`

      rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))

- Line 199; `rule`

      rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)

- Line 200; `rule`

      rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))

- Line 201; `rule`

      rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)

- Line 202; `rule`

      rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))

- Line 203; `rule`

      rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)

- Line 204; `rule`

      rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))

- Line 205; `rule`

      rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)

- Line 206; `rule`

      rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))

- Line 209; `syntax`

      syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]

- Line 210; `rule`

      rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]

- Line 211; `rule`

      rule applyBuiltin("int", F:Float, .Vals) => truncF(F)

- Line 213; `rule`

      rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)

- Line 214; `rule`

      rule applyBuiltin("float", F:Float, .Vals) => F

- Line 217; `syntax`

      syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]

- Line 218; `rule`

      rule roundF(F:Float)
        => #if (F -Float floorFloat(F)) ==Float 0.5
           #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
                  #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
           #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]

- Line 223; `syntax`

      syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]

- Line 224; `rule`

      rule roundFN(F:Float, N:Int)
        => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
           /Float Int2Float(10 ^Int N, 53, 11) [concrete]

- Line 227; `rule`

      rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)

- Line 228; `rule`

      rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)

- Line 230; `syntax`

      syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]

- Line 231; `rule`

      rule sqrtF(F:Float) => sqrtFloat(F) [concrete]

- Line 232; `syntax`

      syntax KItem ::= "#mathSqrt"

- Line 233; `rule`

      rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]

- Line 234; `rule`

      rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>

- Line 235; `rule`

      rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>

- Line 243; `syntax`

      syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)

- Line 244; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)

- Line 245; `rule`

      rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>

- Line 246; `rule`

      rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>

- Line 247; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
           requires isFloat(V)

- Line 250; `syntax`

      syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)

- Line 251; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)

- Line 252; `rule`

      rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>

- Line 253; `rule`

      rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>

- Line 254; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
           requires isFloat(V)

- Line 261; `syntax`

      syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)

- Line 262; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
            => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
           requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))

- Line 265; `rule`

      rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>

- Line 266; `rule`

      rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>

- Line 267; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
            => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
           requires isFloat(V)

- Line 270; `rule`

      rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
            => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
           requires isInt(V) orBool isBool(V)

- Line 273; `endmodule`

    endmodule

### `reference-semantics/semantics/functions.k`

- Line 3; `module`

    module MPY-FUNCTIONS

- Line 4; `imports`

      imports MPY-CORE

- Line 8; `syntax`

      syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                     | #bindP(ParamNames, Vals)
                     | "#pop"
                     | "#endcall"

- Line 14; `rule`

      rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>

- Line 18; `syntax`

      syntax Expr ::= closureExpr(ParamNames, Stmts)

- Line 19; `rule`

      rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
           <env> L:Int </env>

- Line 27; `syntax`

      syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)

- Line 31; `syntax`

      syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                     | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)

- Line 33; `rule`

      rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                       FreeVars(FVS:ParamNames), BODY:Stmts)
            => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>

- Line 36; `rule`

      rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                          (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
            => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires FV in_keys(M)

- Line 42; `rule`

      rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                          .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>

- Line 47; `rule`

      rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
            => closureVal(PNS, Return(E) .Stmts, L) ... </k>
           <env> L:Int </env>

- Line 50; `rule`

      rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                      FreeVars(FVS:ParamNames), E:Expr)
            => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>

- Line 53; `rule`

      rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                         (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
            => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires FV in_keys(M)

- Line 59; `rule`

      rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
            => closureValC(PNS, CVS, BODY, CM) ... </k>

- Line 63; `rule`

      rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>

- Line 64; `rule`

      rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>

- Line 68; `rule`

      rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
            => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires "$cells" in_keys(M)
            andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
            andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
           [priority(40)]

- Line 78; `rule`

      rule <k> Return(V:Val) ~> _ => #pop </k>
           <ret> noRet => retV(V) </ret>

- Line 80; `rule`

      rule <k> #endcall => #pop ... </k>
           <ret> noRet => retV(noneV) </ret>

- Line 85; `rule`

      rule <k> #pop => V ~> CONT </k>
           <ret>   retV(V) => noRet </ret>
           <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
           <env>   L:Int => CALLERL </env>
           <scopes> SC:Map => SC [ L <- undef ] </scopes>
           <scopeLoc> _ => SAVEDL </scopeLoc>

- Line 91; `endmodule`

    endmodule

### `reference-semantics/semantics/int.k`

- Line 4; `module`

    module MPY-INT

- Line 5; `imports`

      imports MPY-CORE

- Line 7; `rule`

      rule applyUn("-", I:Int) => 0 -Int I

- Line 9; `rule`

      rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2

- Line 11; `rule`

      rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi

- Line 12; `rule`

      rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I

- Line 13; `rule`

      rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2

- Line 14; `rule`

      rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2

- Line 15; `rule`

      rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)

- Line 16; `rule`

      rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2

- Line 17; `rule`

      rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0

- Line 19; `syntax`

      syntax Int ::= pyMod(Int, Int) [function]

- Line 20; `rule`

      rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2

- Line 22; `rule`

      rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2

- Line 23; `rule`

      rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2

- Line 24; `rule`

      rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2

- Line 25; `rule`

      rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2

- Line 26; `rule`

      rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2

- Line 27; `rule`

      rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2

- Line 28; `endmodule`

    endmodule

### `reference-semantics/semantics/iter.k`

- Line 6; `module`

    module MPY-ITER

- Line 7; `imports`

      imports MPY-CORE

- Line 8; `syntax`

      syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)

- Line 9; `endmodule`

    endmodule

### `reference-semantics/semantics/list.k`

- Line 3; `module`

    module MPY-LIST

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports MPY-ITER

- Line 6; `imports`

      imports MPY-OPERATORS

- Line 9; `rule`

      rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>

- Line 10; `rule`

      rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>

- Line 13; `syntax`

      syntax ApplyK ::= "toList"

- Line 14; `rule`

      rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>

- Line 15; `rule`

      rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>

- Line 18; `syntax`

      syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]

- Line 19; `rule`

      rule valSeqConcat(.ValSeq, T:ValSeq)                => T

- Line 20; `rule`

      rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))

- Line 24; `rule`

      rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
           [priority(45)]

- Line 27; `rule`

      rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B

- Line 28; `rule`

      rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)

- Line 33; `syntax`

      syntax Bool ::= hasRefVS(ValSeq) [function, total]

- Line 34; `rule`

      rule hasRefVS(.ValSeq)                => false

- Line 35; `rule`

      rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)

- Line 37; `syntax`

      syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                    | deepEqV(Val, Val, Map)        [function]

- Line 39; `rule`

      rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true

- Line 40; `rule`

      rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false

- Line 41; `rule`

      rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false

- Line 42; `rule`

      rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
        => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)

- Line 45; `rule`

      rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
           requires H in_keys(HP)

- Line 47; `rule`

      rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
           requires notBool isRefV(A) andBool H in_keys(HP)

- Line 49; `rule`

      rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)

- Line 50; `rule`

      rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]

- Line 53; `rule`

      rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
           <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
           [priority(40)]

- Line 58; `syntax`

      syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"

- Line 59; `rule`

      rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>

- Line 60; `rule`

      rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>

- Line 61; `rule`

      rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>

- Line 62; `rule`

      rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>

- Line 63; `rule`

      rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
           requires E ==K V

- Line 65; `rule`

      rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
           requires notBool (E ==K V)

- Line 67; `rule`

      rule <k> B:Bool ~> #notB => notBool B ... </k>

- Line 68; `endmodule`

    endmodule

### `reference-semantics/semantics/methods.k`

- Line 3; `module`

    module MPY-METHODS

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports K-EQUAL

- Line 6; `imports`

      imports MPY-STR

- Line 7; `imports`

      imports MPY-LIST

- Line 10; `syntax`

      syntax Val ::= applyMethod(Val, String, Vals) [function]

- Line 13; `rule`

      rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)

- Line 14; `rule`

      rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)

- Line 15; `rule`

      rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)

- Line 16; `rule`

      rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)

- Line 19; `rule`

      rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))

- Line 20; `rule`

      rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))

- Line 21; `rule`

      rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))

- Line 26; `rule`

      rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))

- Line 27; `syntax`

      syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]

- Line 28; `rule`

      rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq

- Line 29; `rule`

      rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS

- Line 30; `rule`

      rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
        => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))

- Line 34; `rule`

      rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)

- Line 35; `syntax`

      syntax Int ::= cntSub(IntSeq, IntSeq) [function]

- Line 36; `rule`

      rule cntSub(.IntSeq, _:IntSeq) => 0

- Line 37; `rule`

      rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
           requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0

- Line 39; `rule`

      rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
           requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0

- Line 41; `syntax`

      syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]

- Line 42; `rule`

      rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0

- Line 43; `rule`

      rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]

- Line 44; `rule`

      rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0

- Line 47; `rule`

      rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))

- Line 48; `syntax`

      syntax IntSeq ::= trimWS(IntSeq) [function, total]

- Line 49; `rule`

      rule trimWS(.IntSeq) => .IntSeq

- Line 50; `rule`

      rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)

- Line 51; `rule`

      rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)

- Line 52; `syntax`

      syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]

- Line 53; `rule`

      rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)

- Line 54; `rule`

      rule revISAcc(.IntSeq, A:IntSeq) => A

- Line 55; `rule`

      rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))

- Line 58; `rule`

      rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)

- Line 61; `rule`

      rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)

- Line 64; `rule`

      rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)

- Line 65; `syntax`

      syntax Int ::= cntOccVS(ValSeq, Val) [function, total]

- Line 66; `rule`

      rule cntOccVS(.ValSeq, _:Val)                => 0

- Line 67; `rule`

      rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V

- Line 68; `rule`

      rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)

- Line 72; `rule`

      rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
            => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
           [priority(40)]

- Line 75; `syntax`

      syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result

- Line 76; `rule`

      rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)

- Line 77; `rule`

      rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
           requires isWSC(C)

- Line 79; `rule`

      rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
           requires notBool isWSC(C)

- Line 82; `syntax`

      syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]

- Line 83; `rule`

      rule flushTok(ACC:ValSeq, .IntSeq)            => ACC

- Line 84; `rule`

      rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))

- Line 85; `syntax`

      syntax Bool ::= isWSC(Int) [function, total]

- Line 86; `rule`

      rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13

- Line 89; `rule`

      rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
            => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
           [priority(39)]

- Line 94; `rule`

      rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
            => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
           [priority(40)]

- Line 97; `syntax`

      syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token

- Line 98; `rule`

      rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)

- Line 99; `rule`

      rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
           requires C ==Int SEP

- Line 101; `rule`

      rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
           requires notBool (C ==Int SEP)

- Line 104; `rule`

      rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
        => str(replaceC(CS, A, B))

- Line 106; `syntax`

      syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]

- Line 107; `rule`

      rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq

- Line 108; `rule`

      rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A

- Line 109; `rule`

      rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)

- Line 112; `syntax`

      syntax Bool ::= isUpperC(Int) [function, total]

- Line 113; `rule`

      rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90

- Line 115; `syntax`

      syntax Bool ::= isLowerC(Int) [function, total]

- Line 116; `rule`

      rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122

- Line 118; `syntax`

      syntax Bool ::= isAlphaC(Int) [function, total]

- Line 119; `rule`

      rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)

- Line 121; `syntax`

      syntax Bool ::= isDigitC(Int) [function, total]

- Line 122; `rule`

      rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57

- Line 124; `syntax`

      syntax Bool ::= hasUpper(IntSeq) [function, total]

- Line 125; `rule`

      rule hasUpper(.IntSeq) => false

- Line 126; `rule`

      rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)

- Line 128; `syntax`

      syntax Bool ::= hasLower(IntSeq) [function, total]

- Line 129; `rule`

      rule hasLower(.IntSeq) => false

- Line 130; `rule`

      rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)

- Line 132; `syntax`

      syntax Bool ::= allAlpha(IntSeq) [function, total]

- Line 133; `rule`

      rule allAlpha(.IntSeq) => true

- Line 134; `rule`

      rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)

- Line 136; `syntax`

      syntax Bool ::= allDigit(IntSeq) [function, total]

- Line 137; `rule`

      rule allDigit(.IntSeq) => true

- Line 138; `rule`

      rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)

- Line 140; `syntax`

      syntax Int ::= lowerC(Int) [function, total]

- Line 142; `rule`

      rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)

- Line 143; `rule`

      rule lowerC(C:Int) => C         [owise]

- Line 145; `syntax`

      syntax Int ::= upperC(Int) [function, total]

- Line 146; `rule`

      rule upperC(C:Int) => C -Int 32 requires isLowerC(C)

- Line 147; `rule`

      rule upperC(C:Int) => C         [owise]

- Line 149; `syntax`

      syntax Int ::= swapC(Int) [function, total]

- Line 150; `rule`

      rule swapC(C:Int) => C +Int 32 requires isUpperC(C)

- Line 151; `rule`

      rule swapC(C:Int) => C -Int 32 requires isLowerC(C)

- Line 152; `rule`

      rule swapC(C:Int) => C         [owise]

- Line 154; `syntax`

      syntax IntSeq ::= mapLower(IntSeq) [function, total]

- Line 155; `rule`

      rule mapLower(.IntSeq) => .IntSeq

- Line 156; `rule`

      rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))

- Line 158; `syntax`

      syntax IntSeq ::= mapUpper(IntSeq) [function, total]

- Line 159; `rule`

      rule mapUpper(.IntSeq) => .IntSeq

- Line 160; `rule`

      rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))

- Line 162; `syntax`

      syntax IntSeq ::= mapSwap(IntSeq) [function, total]

- Line 163; `rule`

      rule mapSwap(.IntSeq) => .IntSeq

- Line 164; `rule`

      rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))

- Line 166; `syntax`

      syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]

- Line 167; `rule`

      rule startsWith(.IntSeq, _:IntSeq)               => true

- Line 168; `rule`

      rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false

- Line 169; `rule`

      rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)

- Line 170; `endmodule`

    endmodule

### `reference-semantics/semantics/operators.k`

- Line 6; `module`

    module MPY-OPERATORS

- Line 7; `imports`

      imports MPY-CORE

- Line 8; `imports`

      imports MPY-ITER

- Line 10; `rule`

      rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>

- Line 12; `rule`

      rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>

- Line 15; `context`

      context Compare(HOLE, _)

- Line 16; `context`

      context Compare(_:Val, CmpOp(_, HOLE))

- Line 17; `rule`

      rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]

- Line 19; `rule`

      rule applyCmp("is",     V:Val, noneV) => V ==K noneV

- Line 20; `rule`

      rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)

- Line 25; `rule`

      rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 28; `rule`

      rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isRefV(L)
           [priority(40)]

- Line 34; `rule`

      rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires OP =/=String "in" andBool OP =/=String "not in"
           [priority(40)]

- Line 38; `rule`

      rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           requires notBool isRefV(L)
            orBool OP ==String "in" orBool OP ==String "not in"
           [priority(40)]

- Line 44; `rule`

      rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 47; `endmodule`

    endmodule

### `reference-semantics/semantics/range.k`

- Line 5; `module`

    module MPY-RANGE

- Line 6; `imports`

      imports MPY-CORE

- Line 7; `imports`

      imports MPY-ITER

- Line 9; `syntax`

      syntax Bool ::= inRange(Int, Int, Int) [function, total]

- Line 10; `rule`

      rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)

- Line 12; `syntax`

      syntax Int ::= rangeLen(Int, Int, Int) [function]

- Line 13; `rule`

      rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
           requires ST >Int 0 andBool HI >Int LO

- Line 15; `rule`

      rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
           requires ST <Int 0 andBool HI <Int LO

- Line 17; `rule`

      rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
           requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)

- Line 20; `rule`

      rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
            => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
           requires inRange(I, HI, ST)

- Line 23; `rule`

      rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
           requires notBool inRange(I, HI, ST)

- Line 25; `endmodule`

    endmodule

### `reference-semantics/semantics/set.k`

- Line 3; `module`

    module MPY-SET

- Line 4; `imports`

      imports MPY-CORE

- Line 8; `syntax`

      syntax Val ::= setV(IntSeq)

- Line 11; `syntax`

      syntax Bool ::= codeIn(Int, IntSeq) [function, total]

- Line 12; `rule`

      rule codeIn(_:Int, .IntSeq)                => false

- Line 13; `rule`

      rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)

- Line 16; `syntax`

      syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                      | dedupFrom(IntSeq, IntSeq)  [function, total]

- Line 18; `rule`

      rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)

- Line 19; `rule`

      rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC

- Line 20; `rule`

      rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
           requires codeIn(C, ACC)

- Line 22; `rule`

      rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
           requires notBool codeIn(C, ACC)

- Line 25; `syntax`

      syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]

- Line 26; `rule`

      rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)

- Line 27; `rule`

      rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))

- Line 31; `syntax`

      syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]

- Line 32; `rule`

      rule subsetCodes(.IntSeq, _:IntSeq)                => true

- Line 33; `rule`

      rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)

- Line 35; `syntax`

      syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]

- Line 36; `rule`

      rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)

- Line 39; `rule`

      rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)

- Line 40; `endmodule`

    endmodule

### `reference-semantics/semantics/sort.k`

- Line 10; `module`

    module MPY-SORT

- Line 11; `imports`

      imports MPY-BUILTINS

- Line 12; `imports`

      imports MPY-SUBSCRIPT

- Line 18; `syntax`

      syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]

- Line 19; `syntax`

      syntax ValSeq ::= insVS(Int, ValSeq) [function]

- Line 20; `rule`

      rule sortVS(.ValSeq)                => .ValSeq          [concrete]

- Line 21; `rule`

      rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]

- Line 22; `rule`

      rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]

- Line 23; `rule`

      rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]

- Line 24; `rule`

      rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]

- Line 26; `syntax`

      syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]

- Line 27; `rule`

      rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]

- Line 28; `rule`

      rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]

- Line 29; `rule`

      rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
           requires strLt(A, B) orBool A ==K B [concrete]

- Line 31; `rule`

      rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
           requires notBool (strLt(A, B) orBool A ==K B) [concrete]

- Line 36; `rule`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
            => #alloc(list(sortVS(VS))) ... </k>

- Line 40; `rule`

      rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
           <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
           [priority(40)]

- Line 49; `syntax`

      syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]

- Line 51; `syntax`

      syntax ValSeq ::= revVS(ValSeq) [function, total]
                      | revVSAcc(ValSeq, ValSeq) [function, total]

- Line 53; `rule`

      rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)

- Line 54; `rule`

      rule revVSAcc(.ValSeq, A:ValSeq) => A

- Line 55; `rule`

      rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))

- Line 57; `syntax`

      syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]

- Line 58; `rule`

      rule condRev(S:ValSeq, false) => S

- Line 59; `rule`

      rule condRev(S:ValSeq, true)  => revVS(S)

- Line 61; `rule`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
            => #alloc(list(sortKeyVS(VS, KV))) ... </k>

- Line 63; `rule`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
            => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>

- Line 65; `rule`

      rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
            => #alloc(list(condRev(sortVS(VS), RB))) ... </k>

- Line 72; `endmodule`

    endmodule

### `reference-semantics/semantics/str.k`

- Line 3; `module`

    module MPY-STR

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports MPY-ITER

- Line 8; `rule`

      rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>

- Line 9; `rule`

      rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
            => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>

- Line 13; `syntax`

      syntax IntSeq ::= strToCodes(String) [function]

- Line 14; `rule`

      rule <k> Str(S:String) => str(strToCodes(S)) ... </k>

- Line 15; `rule`

      rule strToCodes("") => .IntSeq

- Line 16; `rule`

      rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
        requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128

- Line 20; `syntax`

      syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]

- Line 21; `rule`

      rule seqConcat(.IntSeq, T:IntSeq)                => T

- Line 22; `rule`

      rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))

- Line 24; `rule`

      rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))

- Line 25; `rule`

      rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B

- Line 26; `rule`

      rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)

- Line 29; `rule`

      rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)

- Line 30; `rule`

      rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)

- Line 32; `syntax`

      syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]

- Line 33; `rule`

      rule strPrefix(.IntSeq, _:IntSeq)               => true

- Line 34; `rule`

      rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false

- Line 35; `rule`

      rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)

- Line 37; `syntax`

      syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]

- Line 38; `rule`

      rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)

- Line 39; `rule`

      rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)

- Line 40; `rule`

      rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
           requires notBool strPrefix(P, iCons(C, Xs))

- Line 48; `syntax`

      syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]

- Line 49; `rule`

      rule strLt(.IntSeq, .IntSeq)                => false

- Line 50; `rule`

      rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true

- Line 51; `rule`

      rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false

- Line 52; `rule`

      rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B

- Line 53; `rule`

      rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B

- Line 54; `rule`

      rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B

- Line 56; `rule`

      rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)

- Line 57; `rule`

      rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)

- Line 58; `rule`

      rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)

- Line 59; `rule`

      rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)

- Line 60; `endmodule`

    endmodule

### `reference-semantics/semantics/subscript.k`

- Line 3; `module`

    module MPY-SUBSCRIPT

- Line 4; `imports`

      imports MPY-CORE

- Line 11; `syntax`

      syntax Val ::= valSeqAt(ValSeq, Int) [function, total]

- Line 12; `rule`

      rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V

- Line 13; `rule`

      rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
           requires I >Int 0

- Line 16; `syntax`

      syntax Int ::= intSeqAt(IntSeq, Int) [function]

- Line 17; `rule`

      rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C

- Line 18; `rule`

      rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
           requires I >Int 0

- Line 21; `syntax`

      syntax Int ::= normIdx(Int, Int) [function, total]

- Line 22; `rule`

      rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0

- Line 23; `rule`

      rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0

- Line 27; `context`

      context Subscript(HOLE, _)

- Line 28; `context`

      context Subscript(_:Val, HOLE:Expr)

- Line 31; `rule`

      rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 35; `rule`

      rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>

- Line 37; `syntax`

      syntax Val ::= applyIndex(Val, Int) [function]

- Line 38; `rule`

      rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))

- Line 39; `rule`

      rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))

- Line 40; `rule`

      rule applyIndex(str(IS:IntSeq),   I:Int)
        => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))

- Line 44; `syntax`

      syntax KItem ::= #evalB(Bound) | "#toSome"
                     | #slLo(Val, Bound, Bound)
                     | #slHi(Val, OptInt, Bound)
                     | #slStep(Val, OptInt, OptInt)

- Line 49; `syntax`

      syntax OptInt ::= "noB" | someB(Int)

- Line 50; `rule`

      rule <k> #evalB(NoBound)  => noB ... </k>

- Line 51; `rule`

      rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>

- Line 52; `rule`

      rule <k> I:Int ~> #toSome => someB(I) ... </k>

- Line 54; `rule`

      rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>

- Line 55; `rule`

      rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>

- Line 56; `rule`

      rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>

- Line 58; `rule`

      rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
            => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
           [priority(45)]

- Line 61; `rule`

      rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>

- Line 63; `syntax`

      syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]

- Line 64; `rule`

      rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
        => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))

- Line 66; `rule`

      rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
        => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))

- Line 68; `rule`

      rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
        => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))

- Line 72; `syntax`

      syntax Int ::= slStep(OptInt) [function, total]

- Line 73; `rule`

      rule slStep(noB)          => 1

- Line 74; `rule`

      rule slStep(someB(S:Int)) => S

- Line 76; `syntax`

      syntax Int ::= slStart(OptInt, OptInt, Int) [function]

- Line 77; `rule`

      rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
           requires slStep(ST) >Int 0

- Line 79; `rule`

      rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
           requires slStep(ST) <Int 0

- Line 81; `rule`

      rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))

- Line 83; `syntax`

      syntax Int ::= slStop(OptInt, OptInt, Int) [function]

- Line 84; `rule`

      rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
           requires slStep(ST) >Int 0

- Line 86; `rule`

      rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
           requires slStep(ST) <Int 0

- Line 88; `rule`

      rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))

- Line 90; `syntax`

      syntax Int ::= slAdjust(Int, Int, Int) [function, total]

- Line 91; `rule`

      rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
           requires I  <Int 0

- Line 93; `rule`

      rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
           requires I >=Int 0

- Line 96; `syntax`

      syntax Int ::= clampLo(Int, Int) [function, total]

- Line 97; `rule`

      rule clampLo(J:Int, _STEP:Int) => J
           requires J >=Int 0

- Line 99; `rule`

      rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
           requires J <Int 0

- Line 102; `syntax`

      syntax Int ::= clampHi(Int, Int, Int) [function, total]

- Line 103; `rule`

      rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
           requires I  <Int LEN

- Line 105; `rule`

      rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
           requires I >=Int LEN

- Line 109; `syntax`

      syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]

- Line 110; `rule`

      rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
        => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
           requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)

- Line 113; `rule`

      rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
           requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))

- Line 116; `syntax`

      syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]

- Line 117; `rule`

      rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
        => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
           requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)

- Line 120; `rule`

      rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
           requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))

- Line 122; `endmodule`

    endmodule

### `reference-semantics/semantics/syntax.k`

- Line 3; `module`

    module MPY-SYNTAX

- Line 4; `imports`

      imports INT-SYNTAX

- Line 5; `imports`

      imports FLOAT-SYNTAX

- Line 6; `imports`

      imports BOOL-SYNTAX

- Line 7; `imports`

      imports STRING-SYNTAX

- Line 9; `syntax`

      syntax Expr ::= "Int"      "(" Int ")"
                    | "Float"    "(" Float ")"
                    | "Bool"     "(" Bool ")"
                    | "Name"     "(" String ")"
                    | "Str"      "(" String ")"
                    | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
                    | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
                    | "BoolOp"    "(" String "," Exprs ")"
                    | "ListExpr"  "(" Exprs ")"
                    | "DictExpr"  "(" Entries ")"
                    | "ListComp"  "(" Expr "," CompFors ")" [macro]
                    | "GenExp"    "(" Expr "," CompFors ")" [macro]
                    | "TupleExpr" "(" Exprs ")"
                    | "Subscript" "(" Expr "," Index ")"
                    | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
                    | "Lambda"    "(" Params "," Expr ")"
                    | "KwArg"     "(" String "," Expr ")"
                    | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
                    | "NoneVal"
                    | "Call"      "(" Expr "," Exprs ")"
                    | "Attribute" "(" Expr "," String ")" [strict(1)]
                    | "Compare"   "(" Expr "," CmpOp ")"

- Line 32; `syntax`

      syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"

- Line 33; `syntax`

      syntax Entry    ::= "Entry" "(" Expr "," Expr ")"

- Line 34; `syntax`

      syntax Entries  ::= List{Entry, ","}

- Line 35; `syntax`

      syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"

- Line 36; `syntax`

      syntax CompFors ::= List{CompFor, ""}

- Line 37; `syntax`

      syntax Exprs    ::= List{Expr, ","}

- Line 38; `syntax`

      syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"

- Line 39; `syntax`

      syntax Bound    ::= Expr | "NoBound"

- Line 41; `syntax`

      syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
                    | "Import"    "(" String ")"
                    | "ImportFrom" "(" String "," ParamNames ")"
                    | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
                    | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
                    | "While"     "(" Expr "," Stmts ")"
                    | "Break"
                    | "Continue"
                    | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
                    | "Return"    "(" Expr ")" [strict]
                    | "Assert"    "(" Expr ")" [strict]
                    | "Expr"      "(" Expr ")" [strict]
                    | "FuncDef"   "(" String "," Params "," Stmts ")"
                    | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"

- Line 56; `syntax`

      syntax Stmts      ::= List{Stmt, ""}

- Line 57; `syntax`

      syntax Params     ::= "Params" "(" ParamNames ")"

- Line 58; `syntax`

      syntax CellVars   ::= "CellVars" "(" ParamNames ")"

- Line 59; `syntax`

      syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"

- Line 60; `syntax`

      syntax ParamNames ::= List{String, ","}

- Line 61; `syntax`

      syntax Module     ::= "Module" "(" Stmts ")"

- Line 62; `endmodule`

    endmodule

### `reference-semantics/semantics/tuple.k`

- Line 3; `module`

    module MPY-TUPLE

- Line 4; `imports`

      imports MPY-CORE

- Line 5; `imports`

      imports MPY-ITER

- Line 6; `imports`

      imports MPY-LIST

- Line 7; `imports`

      imports MPY-METHODS

- Line 10; `rule`

      rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>

- Line 11; `rule`

      rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>

- Line 14; `syntax`

      syntax ApplyK ::= "toTuple"

- Line 15; `rule`

      rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>

- Line 16; `rule`

      rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>

- Line 18; `rule`

      rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B

- Line 20; `rule`

      rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>

- Line 21; `rule`

      rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>

- Line 23; `rule`

      rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)

- Line 24; `syntax`

      syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]

- Line 25; `rule`

      rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V

- Line 26; `rule`

      rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
           requires notBool (A ==K V)

- Line 28; `rule`

      rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)

- Line 31; `syntax`

      syntax KItem ::= #bindTgt(Expr, Val)

- Line 32; `rule`

      rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>

- Line 35; `rule`

      rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
           <env> L:Int </env>
           <scopes> ... L |-> scope(M:Map, _) ... </scopes>
           requires "$cells" in_keys(M)
            andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
            andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
           [priority(40)]

- Line 42; `rule`

      rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>

- Line 43; `rule`

      rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>

- Line 44; `rule`

      rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 49; `syntax`

      syntax KItem ::= #unpackSeq(Exprs, ValSeq)

- Line 50; `rule`

      rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>

- Line 51; `rule`

      rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>

- Line 52; `rule`

      rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
           <heap> ... H |-> V:Val ... </heap>
           [priority(40)]

- Line 55; `rule`

      rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
            => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>

- Line 57; `rule`

      rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>

- Line 58; `endmodule`

    endmodule

### `verification.k`

- Line 1; `requires`

    requires "reference-semantics/semantics.k"

- Line 3; `module`

    module SUM-TO-N-VERIFICATION

- Line 4; `imports`

      imports MPY

- Line 7; `syntax`

      syntax KItem ::= "#runSumToN" "(" Int ")"

- Line 8; `rule`

      rule #runSumToN(N:Int)
        => #loadAll(
             Module(
               FuncDef(
                 "sum_to_n",
                 Params("n"),
                 Return(
                   BinOp(
                     "//",
                     BinOp("*", Name("n"), BinOp("+", Name("n"), Int(1))),
                     Int(2))))))
           ~> Call(Name("sum_to_n"), Int(N), .Exprs)

- Line 24; `syntax`

      syntax Int ::= triangular(Int) [function, total]

- Line 25; `rule`

      rule triangular(N:Int)
        => (N *Int (N +Int 1) -Int pyMod(N *Int (N +Int 1), 2)) /Int 2

- Line 27; `endmodule`

    endmodule

### `spec.k`

- Line 1; `requires`

    requires "verification.k"

- Line 3; `module`

    module SUM-TO-N-SPEC

- Line 4; `imports`

      imports SUM-TO-N-VERIFICATION

- Line 6; `claim`

      claim
        <k> #runSumToN(N) => triangular(N) </k>
        <env> 0 </env>
        <scopes>
          0  |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
          =>
          0  |-> scope(
                   "sum_to_n"
                   |-> closureVal(
                         "n",
                         Return(
                           BinOp(
                             "//",
                             BinOp("*", Name("n"), BinOp("+", Name("n"), Int(1))),
                             Int(2)))
                         .Stmts,
                         0),
                   parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
        requires N >=Int 0

- Line 35; `endmodule`

    endmodule

