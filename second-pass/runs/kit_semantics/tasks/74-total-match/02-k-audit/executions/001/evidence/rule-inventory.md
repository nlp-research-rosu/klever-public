# Exhaustive K declaration and rule inventory

Generated from the fresh scratch copy. The supplied tree is the integrity-checked fixed baseline; `verification.k` and `spec.k` are candidate-authored and receive independent decisions.

## Counts

- `claim`: 3
- `configuration`: 1
- `context`: 5
- `rule`: 705
- `rule_concrete`: 35
- `rule_owise`: 27
- `rule_priority`: 45
- `rule_simplification`: 1
- `syntax`: 231
- `syntax_function`: 150
- `syntax_no-evaluators`: 22
- `syntax_total`: 111
- `opaque/no-evaluators declarations`: 22
- `priority rules`: 45
- `simplification rules`: 1

## Opaque declarations

- `reference-semantics/semantics/builtins.k:285` (syntax:function,total,no-evaluators, material=false): `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:24` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:30` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:37` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:50` (syntax:function,total,no-evaluators, material=false): `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:54` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:103` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:107` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:111` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:115` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:119` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:125` (syntax:function,total,no-evaluators, material=false): `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:142` (syntax:function,total,no-evaluators, material=false): `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:160` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:190` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:195` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:209` (syntax:function,total,no-evaluators, material=false): `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:217` (syntax:function,total,no-evaluators, material=false): `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:223` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:230` (syntax:function,total,no-evaluators, material=false): `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:18` (syntax:function,total,no-evaluators, material=false): `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:49` (syntax:function,total,no-evaluators, material=false): `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` — FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.

## Complete inventory

### `reference-semantics/semantics/assert.k`

- `reference-semantics/semantics/assert.k:6` — `rule:ordinary`; material=false; `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/assert.k:8` — `rule:ordinary`; material=false; `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/assert.k:13` — `rule:priority`; material=false; `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/bool.k`

- `reference-semantics/semantics/bool.k:8` — `rule:ordinary`; material=false; `rule applyUn("not", V:Val) => notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:10` — `rule:ordinary`; material=false; `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:11` — `rule:ordinary`; material=false; `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:16` — `context`; material=false; `context BoolOp(_, (HOLE:Expr, _:Exprs))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:17` — `rule:ordinary`; material=false; `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:18` — `rule:ordinary`; material=false; `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:20` — `rule:ordinary`; material=false; `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:22` — `rule:ordinary`; material=false; `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:24` — `rule:ordinary`; material=false; `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:29` — `rule:priority`; material=false; `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:31` — `rule:priority`; material=false; `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:35` — `rule:priority`; material=false; `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:39` — `rule:priority`; material=false; `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/bool.k:43` — `rule:priority`; material=false; `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/builtins.k`

- `reference-semantics/semantics/builtins.k:17` — `syntax:function`; material=false; `syntax Val ::= applyBuiltin(String, Vals) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:20` — `syntax:function`; material=true; `syntax Int ::= seqLen(Val) [function]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/builtins.k:21` — `rule:ordinary`; material=true; `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/builtins.k:22` — `rule:ordinary`; material=false; `rule seqLen(list(VS:ValSeq)) => vsLen(VS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:23` — `rule:ordinary`; material=false; `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:24` — `rule:ordinary`; material=true; `rule seqLen(str(IS:IntSeq)) => isLen(IS)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/builtins.k:25` — `rule:ordinary`; material=false; `rule seqLen(setV(DS:IntSeq)) => isLen(DS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:26` — `rule:ordinary`; material=false; `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:32` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:33` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:34` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:35` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:36` — `syntax:function,total`; material=false; `syntax ValSeq ::= charsOf(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:37` — `rule:ordinary`; material=false; `rule charsOf(.IntSeq) => .ValSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:38` — `rule:ordinary`; material=false; `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:41` — `rule:ordinary`; material=false; `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:44` — `rule:ordinary`; material=false; `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:47` — `syntax`; material=false; `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:48` — `rule:ordinary`; material=false; `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:49` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:50` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:54` — `syntax:function`; material=false; `syntax Int ::= intOf(Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:55` — `rule:ordinary`; material=false; `rule intOf(I:Int) => I`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:56` — `rule:ordinary`; material=false; `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:59` — `syntax`; material=false; `syntax KItem ::= #allAcc(Iterable) | "#allCont"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:60` — `rule:ordinary`; material=false; `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:61` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #allCont => true ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:62` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:64` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:67` — `syntax`; material=false; `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:68` — `rule:ordinary`; material=false; `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:69` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #anyCont => false ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:70` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:72` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:76` — `syntax`; material=false; `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:77` — `rule:ordinary`; material=false; `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:78` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:80` — `rule:ordinary`; material=false; `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:81` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:82` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:86` — `syntax`; material=false; `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:87` — `rule:ordinary`; material=false; `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:88` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:90` — `rule:ordinary`; material=false; `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:91` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:92` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:97` — `syntax:function`; material=false; `syntax Int ::= maxVals(Int, Vals) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:98` — `rule:ordinary`; material=false; `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:99` — `rule:ordinary`; material=false; `rule maxVals(M:Int, .Vals) => M`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:100` — `rule:ordinary`; material=false; `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:102` — `syntax:function`; material=false; `syntax Int ::= minVals(Int, Vals) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:103` — `rule:ordinary`; material=false; `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:104` — `rule:ordinary`; material=false; `rule minVals(M:Int, .Vals) => M`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:105` — `rule:ordinary`; material=false; `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:108` — `rule:ordinary`; material=false; `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:111` — `rule:ordinary`; material=false; `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:114` — `syntax:function,total`; material=false; `syntax IntSeq ::= binCodes(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:115` — `rule:ordinary`; material=false; `rule binCodes(0) => iCons(48, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:116` — `rule:ordinary`; material=false; `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:117` — `syntax:function,total`; material=false; `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:118` — `rule:ordinary`; material=false; `rule binAcc(0, ACC:IntSeq) => ACC`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:119` — `rule:ordinary`; material=false; `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:124` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:126` — `syntax:function,total`; material=false; `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:127` — `rule:ordinary`; material=false; `rule enumVS(.ValSeq, _:Int) => .ValSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:128` — `rule:ordinary`; material=false; `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:132` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:134` — `syntax:function,total`; material=false; `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:135` — `rule:ordinary`; material=false; `rule mapStrVS(.ValSeq) => .ValSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:136` — `rule:ordinary`; material=false; `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:137` — `rule:ordinary`; material=false; `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:140` — `rule:ordinary`; material=false; `rule applyBuiltin("int", I:Int, .Vals) => I`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:143` — `rule:ordinary`; material=false; `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:144` — `rule:ordinary`; material=false; `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:148` — `rule:ordinary`; material=false; `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:149` — `rule:ordinary`; material=false; `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:152` — `rule:ordinary`; material=false; `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:156` — `rule:ordinary`; material=false; `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:158` — `syntax:function,total`; material=false; `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:159` — `rule:ordinary`; material=false; `rule intDigAcc(.IntSeq, ACC:Int) => ACC`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:160` — `rule:ordinary`; material=false; `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:163` — `rule:ordinary`; material=false; `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:164` — `rule:ordinary`; material=false; `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:167` — `rule:ordinary`; material=false; `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:169` — `rule:ordinary`; material=false; `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:170` — `rule:ordinary`; material=false; `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:171` — `rule:ordinary`; material=false; `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:173` — `rule:ordinary`; material=false; `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:174` — `rule:ordinary`; material=false; `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:177` — `rule:ordinary`; material=false; `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:178` — `rule:ordinary`; material=false; `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:179` — `rule:ordinary`; material=false; `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:187` — `rule:ordinary`; material=false; `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:188` — `syntax:function`; material=false; `syntax Int ::= evalArith(IntSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:189` — `rule:ordinary`; material=false; `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:192` — `syntax`; material=false; `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:194` — `syntax:function,total`; material=false; `syntax Bool ::= evDigit(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:195` — `rule:ordinary`; material=false; `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:196` — `syntax:function,total`; material=false; `syntax Bool ::= evHead42(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:197` — `rule:ordinary`; material=false; `rule evHead42(iCons(42, _:IntSeq)) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:198` — `rule:owise`; material=false; `rule evHead42(_:IntSeq) => false [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:199` — `syntax:function,total`; material=false; `syntax Bool ::= evHead47(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:200` — `rule:ordinary`; material=false; `rule evHead47(iCons(47, _:IntSeq)) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:201` — `rule:owise`; material=false; `rule evHead47(_:IntSeq) => false [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:203` — `syntax:function,total`; material=false; `syntax OpSeq ::= tokOps(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:204` — `rule:ordinary`; material=false; `rule tokOps(.IntSeq) => .OpSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:205` — `rule:ordinary`; material=false; `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:206` — `rule:ordinary`; material=false; `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:207` — `rule:ordinary`; material=false; `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:208` — `rule:ordinary`; material=false; `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:209` — `rule:ordinary`; material=false; `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:210` — `rule:ordinary`; material=false; `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:211` — `rule:ordinary`; material=false; `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:212` — `rule:ordinary`; material=false; `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:214` — `syntax:function,total`; material=false; `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:216` — `rule:ordinary`; material=false; `rule tokNds(.IntSeq) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:217` — `rule:ordinary`; material=false; `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:218` — `rule:ordinary`; material=false; `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:219` — `rule:ordinary`; material=false; `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:221` — `rule:ordinary`; material=false; `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:223` — `rule:owise`; material=false; `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:225` — `syntax`; material=false; `syntax EvPair ::= evp(OpSeq, IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:226` — `syntax:function,total`; material=false; `syntax Int ::= firstNdE(EvPair) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:227` — `rule:ordinary`; material=false; `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:228` — `rule:owise`; material=false; `rule firstNdE(_:EvPair) => 0 [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:230` — `syntax:function,total`; material=false; `syntax Int ::= applyOpE(String, Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:231` — `rule:ordinary`; material=false; `rule applyOpE("+", A:Int, B:Int) => A +Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:232` — `rule:ordinary`; material=false; `rule applyOpE("-", A:Int, B:Int) => A -Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:233` — `rule:ordinary`; material=false; `rule applyOpE("*", A:Int, B:Int) => A *Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:234` — `rule:ordinary`; material=false; `rule applyOpE("`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:235` — `rule:ordinary`; material=false; `rule applyOpE("**", A:Int, B:Int) => A ^Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:236` — `rule:owise`; material=false; `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:238` — `syntax:function,total`; material=false; `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:239` — `rule:ordinary`; material=false; `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:240` — `rule:ordinary`; material=false; `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:241` — `rule:ordinary`; material=false; `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:243` — `rule:owise`; material=false; `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:244` — `syntax:function,total`; material=false; `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:245` — `rule:ordinary`; material=false; `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:246` — `rule:ordinary`; material=false; `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:247` — `syntax:function,total`; material=false; `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:248` — `rule:ordinary`; material=false; `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:250` — `syntax:function,total`; material=false; `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:251` — `rule:ordinary`; material=false; `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:252` — `rule:ordinary`; material=false; `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:253` — `rule:ordinary`; material=false; `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:254` — `rule:ordinary`; material=false; `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:255` — `syntax:function,total`; material=false; `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:256` — `rule:ordinary`; material=false; `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:257` — `rule:ordinary`; material=false; `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:260` — `rule:ordinary`; material=false; `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:263` — `rule:owise`; material=false; `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:265` — `syntax:function,total`; material=false; `syntax Bool ::= inLevelE(String, String) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:266` — `rule:ordinary`; material=false; `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:267` — `rule:ordinary`; material=false; `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:268` — `rule:owise`; material=false; `rule inLevelE(_:String, _:String) => false [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:269` — `syntax:function,total`; material=false; `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:270` — `rule:ordinary`; material=false; `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:271` — `rule:ordinary`; material=false; `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:272` — `syntax:function,total`; material=false; `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:273` — `rule:ordinary`; material=false; `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:274` — `rule:ordinary`; material=false; `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:279` — `syntax`; material=false; `syntax KItem ::= "#md5"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:280` — `rule:priority`; material=false; `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:282` — `rule:ordinary`; material=false; `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:283` — `syntax`; material=false; `syntax Val ::= md5Obj(IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:284` — `rule:ordinary`; material=false; `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:285` — `syntax:function,total,no-evaluators`; material=false; `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:291` — `rule:ordinary`; material=false; `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:292` — `rule:ordinary`; material=false; `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:293` — `syntax:function`; material=true; `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/builtins.k:294` — `rule:ordinary`; material=false; `rule isIntV(_:Int) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:295` — `rule:owise`; material=false; `rule isIntV(_:Val) => false [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/builtins.k:296` — `rule:ordinary`; material=true; `rule isStrV(str(_:IntSeq)) => true`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/builtins.k:297` — `rule:owise`; material=true; `rule isStrV(_:Val) => false [owise]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
### `reference-semantics/semantics/call.k`

- `reference-semantics/semantics/call.k:16` — `rule:ordinary`; material=false; `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:19` — `syntax`; material=true; `syntax KItem ::= #callee(Exprs)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/call.k:20` — `rule:owise`; material=true; `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/call.k:21` — `rule:ordinary`; material=true; `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/call.k:24` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:26` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:27` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:28` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:29` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:30` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:31` — `rule:owise`; material=true; `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/call.k:32` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:38` — `rule:priority`; material=true; `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/call.k:42` — `rule:priority`; material=false; `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:47` — `rule:priority`; material=false; `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:52` — `syntax:function,total`; material=false; `syntax Bool ::= isMutMethod(String) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:53` — `rule:ordinary`; material=false; `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:56` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:63` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:69` — `rule:ordinary`; material=true; `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/call.k:80` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:87` — `syntax`; material=false; `syntax KItem ::= #allocCells(ParamNames)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:88` — `rule:ordinary`; material=false; `rule <k> #allocCells(.ParamNames) => .K ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/call.k:89` — `rule:ordinary`; material=false; `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/comprehension.k`

- `reference-semantics/semantics/comprehension.k:11` — `rule:ordinary`; material=false; `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:12` — `rule:ordinary`; material=false; `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:14` — `syntax:macro`; material=false; `syntax Stmts ::= compBody(CompFors, Expr) [macro]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:15` — `rule:ordinary`; material=false; `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:18` — `syntax:macro-rec,macro`; material=false; `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:19` — `rule:ordinary`; material=false; `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:21` — `rule:ordinary`; material=false; `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:24` — `syntax:macro`; material=false; `syntax Expr ::= compGuard(Exprs) [macro]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:25` — `rule:ordinary`; material=false; `rule compGuard(.Exprs) => Bool(true)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/comprehension.k:26` — `rule:ordinary`; material=false; `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/concrete.k`

- `reference-semantics/semantics/concrete.k:13` — `rule:ordinary`; material=false; `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:16` — `rule:ordinary`; material=false; `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:25` — `syntax`; material=false; `syntax Val ::= kvP(Val, Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:26` — `syntax`; material=false; `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:28` — `rule:priority`; material=false; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:31` — `rule:priority`; material=false; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:34` — `rule:ordinary`; material=false; `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:36` — `rule:ordinary`; material=false; `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:38` — `rule:ordinary`; material=false; `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:42` — `syntax:function`; material=false; `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:43` — `rule:ordinary`; material=false; `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:44` — `rule:ordinary`; material=false; `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:47` — `rule:ordinary`; material=false; `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:51` — `syntax:function`; material=false; `syntax Bool ::= kLt(Val, Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:52` — `rule:ordinary`; material=false; `rule kLt(I1:Int, I2:Int) => I1 <Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:53` — `rule:ordinary`; material=false; `rule kLt(F1:Float, F2:Float) => F1 <Float F2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:54` — `rule:ordinary`; material=false; `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:56` — `syntax:function,total`; material=false; `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:57` — `rule:ordinary`; material=false; `rule unpairVS(.ValSeq) => .ValSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:58` — `rule:ordinary`; material=false; `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/concrete.k:59` — `rule:owise`; material=false; `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/controls.k`

- `reference-semantics/semantics/controls.k:9` — `rule:ordinary`; material=true; `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:12` — `rule:priority`; material=true; `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:20` — `rule:ordinary`; material=true; `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:27` — `rule:priority`; material=true; `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:35` — `rule:ordinary`; material=false; `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:36` — `rule:owise`; material=false; `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:37` — `syntax`; material=false; `syntax KItem ::= #bindImports(ParamNames)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:38` — `rule:ordinary`; material=false; `rule <k> #bindImports(.ParamNames) => .K ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:39` — `rule:ordinary`; material=false; `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:43` — `rule:ordinary`; material=false; `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:48` — `rule:ordinary`; material=false; `rule <k> Expr(_:Val) => .K ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:51` — `syntax`; material=true; `syntax KItem ::= #branch(Bool, Stmts, Stmts)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/controls.k:52` — `rule:ordinary`; material=true; `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:53` — `rule:ordinary`; material=true; `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:54` — `rule:ordinary`; material=true; `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:57` — `rule:ordinary`; material=false; `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:59` — `rule:ordinary`; material=false; `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:65` — `syntax`; material=true; `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/controls.k:69` — `rule:ordinary`; material=true; `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:71` — `rule:ordinary`; material=true; `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:72` — `rule:ordinary`; material=true; `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:73` — `rule:ordinary`; material=true; `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:77` — `rule:ordinary`; material=false; `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:78` — `rule:ordinary`; material=false; `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:79` — `rule:ordinary`; material=false; `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:81` — `rule:ordinary`; material=false; `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:85` — `rule:ordinary`; material=true; `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/controls.k:86` — `rule:ordinary`; material=false; `rule <k> Continue => #cont ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:87` — `rule:ordinary`; material=false; `rule <k> Break => #brk ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:88` — `rule:ordinary`; material=false; `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:89` — `rule:owise`; material=false; `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:90` — `rule:ordinary`; material=false; `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:91` — `rule:owise`; material=false; `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:95` — `rule:priority`; material=false; `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:98` — `rule:priority`; material=false; `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:101` — `rule:priority`; material=false; `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/controls.k:106` — `rule:priority`; material=false; `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/core.k`

- `reference-semantics/semantics/core.k:13` — `syntax`; material=true; `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:14` — `syntax`; material=true; `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:15` — `syntax`; material=true; `syntax Str ::= str(IntSeq)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:18` — `syntax`; material=true; `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:25` — `syntax:function`; material=true; `syntax Val ::= Int | Bool | "noneV" | Iterable | ref(Int) | cellRef(Int) | closureVal(ParamNames, Stmts, Int) | typeV(String) | builtinV(String) | boundMethodV(Val, String)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:36` — `syntax`; material=true; `syntax Parent ::= "root" | parent(Int)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:37` — `syntax`; material=true; `syntax Scope ::= scope(Map, Parent)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:38` — `syntax`; material=true; `syntax KResult ::= Val`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:39` — `syntax`; material=true; `syntax Expr ::= Val`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:40` — `syntax`; material=true; `syntax Vals ::= List{Val, ","}`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:41` — `syntax`; material=true; `syntax Exc ::= "NoExc" | "AssertionError"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:42` — `syntax`; material=true; `syntax RetState ::= "noRet" | retV(Val)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:49` — `configuration`; material=true; `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:68` — `syntax:function,total`; material=true; `syntax Bool ::= isRefV(Val) [function, total]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:69` — `rule:ordinary`; material=true; `rule isRefV(ref(_:Int)) => true`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:70` — `rule:owise`; material=true; `rule isRefV(_:Val) => false [owise]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:75` — `syntax`; material=false; `syntax HeapVal ::= cellV(Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:76` — `syntax:function,total`; material=false; `syntax Bool ::= isCellRef(Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:77` — `rule:ordinary`; material=false; `rule isCellRef(cellRef(_:Int)) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:78` — `rule:owise`; material=false; `rule isCellRef(_:Val) => false [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:85` — `rule:priority`; material=false; `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:95` — `syntax`; material=false; `syntax Val ::= kwV(String, Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:96` — `syntax`; material=false; `syntax KItem ::= #kwTag(String)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:97` — `rule:ordinary`; material=false; `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:98` — `rule:ordinary`; material=false; `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:100` — `syntax:function,total`; material=false; `syntax Bool ::= isKwV(Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:101` — `rule:ordinary`; material=false; `rule isKwV(kwV(_:String, _:Val)) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:102` — `rule:owise`; material=false; `rule isKwV(_:Val) => false [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:106` — `syntax`; material=false; `syntax Val ::= cellsMark(ParamNames)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:107` — `syntax:function`; material=false; `syntax ParamNames ::= cellsOf(Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:108` — `rule:ordinary`; material=false; `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:109` — `syntax:function,total`; material=false; `syntax Bool ::= pnMember(String, ParamNames) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:110` — `rule:ordinary`; material=false; `rule pnMember(_:String, .ParamNames) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:111` — `rule:ordinary`; material=false; `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:113` — `syntax`; material=false; `syntax KItem ::= #cellW(Val, Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:114` — `rule:ordinary`; material=false; `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:117` — `syntax`; material=false; `syntax KItem ::= #alloc(Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:118` — `rule:ordinary`; material=false; `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:124` — `syntax`; material=true; `syntax KItem ::= #loadAll(Module)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:125` — `rule:ordinary`; material=true; `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:126` — `rule:ordinary`; material=true; `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:127` — `rule:ordinary`; material=true; `rule <k> .Stmts => .K ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:130` — `syntax`; material=true; `syntax KItem ::= #look(String, Int)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:131` — `rule:ordinary`; material=true; `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:132` — `rule:ordinary`; material=true; `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:145` — `rule:priority`; material=true; `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:152` — `rule:ordinary`; material=true; `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:157` — `syntax:function,total`; material=true; `syntax Scope ::= "builtinsScope" [function, total]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:158` — `rule:ordinary`; material=true; `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:185` — `syntax`; material=true; `syntax ApplyK ::= toCall(Val)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:186` — `syntax`; material=true; `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:189` — `rule:ordinary`; material=true; `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:190` — `rule:ordinary`; material=true; `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:191` — `rule:ordinary`; material=true; `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:194` — `rule:ordinary`; material=true; `rule <k> Int(I:Int) => I ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:195` — `rule:ordinary`; material=false; `rule <k> Bool(B:Bool) => B ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:196` — `rule:ordinary`; material=true; `rule <k> NoneVal => noneV ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:199` — `syntax:function`; material=true; `syntax Bool ::= truthy(Val) [function]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:200` — `rule:ordinary`; material=true; `rule truthy(B:Bool) => B`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:201` — `rule:ordinary`; material=false; `rule truthy(noneV) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:202` — `rule:ordinary`; material=false; `rule truthy(I:Int) => I =/=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:203` — `rule:ordinary`; material=false; `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:204` — `rule:ordinary`; material=false; `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:205` — `rule:ordinary`; material=false; `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:208` — `syntax:function`; material=false; `syntax Val ::= applyUn(String, Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:209` — `syntax:function`; material=true; `syntax Val ::= applyBin(String, Val, Val) [function]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:210` — `syntax:function`; material=true; `syntax Bool ::= applyCmp(String, Val, Val) [function]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:213` — `syntax:function,total`; material=true; `syntax Vals ::= appendVal(Vals, Val) [function, total]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:214` — `rule:ordinary`; material=true; `rule appendVal(.Vals, V:Val) => V , .Vals`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:215` — `rule:ordinary`; material=true; `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:217` — `syntax:function,total`; material=false; `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:218` — `rule:ordinary`; material=false; `rule vals2valSeq(.Vals) => .ValSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:219` — `rule:ordinary`; material=false; `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:223` — `syntax:function,total`; material=false; `syntax Int ::= vsLen(ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:224` — `rule:ordinary`; material=false; `rule vsLen(.ValSeq) => 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:225` — `rule:ordinary`; material=false; `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:227` — `syntax:function,total`; material=true; `syntax Int ::= isLen(IntSeq) [function, total]`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/core.k:228` — `rule:ordinary`; material=true; `rule isLen(.IntSeq) => 0`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:229` — `rule:ordinary`; material=true; `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/core.k:233` — `syntax:function,total`; material=false; `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:234` — `rule:ordinary`; material=false; `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:235` — `rule:ordinary`; material=false; `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:236` — `rule:ordinary`; material=false; `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/core.k:238` — `rule:ordinary`; material=false; `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/dict.k`

- `reference-semantics/semantics/dict.k:20` — `syntax`; material=false; `syntax Val ::= dictV(ValSeq, ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:23` — `syntax`; material=false; `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:26` — `rule:ordinary`; material=false; `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:27` — `rule:ordinary`; material=false; `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:28` — `rule:ordinary`; material=false; `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:30` — `rule:ordinary`; material=false; `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:32` — `rule:ordinary`; material=false; `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:37` — `syntax:function,total`; material=false; `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:38` — `rule:ordinary`; material=false; `rule dHasKey(.ValSeq, _:Val) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:39` — `rule:ordinary`; material=false; `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:40` — `rule:ordinary`; material=false; `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:43` — `syntax:function,total`; material=false; `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:44` — `rule:ordinary`; material=false; `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:45` — `rule:ordinary`; material=false; `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:49` — `syntax:function,total`; material=false; `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:50` — `rule:ordinary`; material=false; `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:52` — `rule:ordinary`; material=false; `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:54` — `rule:owise`; material=false; `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:58` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:63` — `rule:ordinary`; material=false; `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:64` — `syntax:function`; material=false; `syntax Val ::= applyIndexD(Val, Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:65` — `rule:priority`; material=false; `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:70` — `syntax:function`; material=false; `syntax Val ::= dictSet(Val, Val, Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:71` — `rule:ordinary`; material=false; `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:76` — `syntax`; material=false; `syntax KItem ::= #dsetK(String, Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:77` — `rule:ordinary`; material=false; `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:78` — `rule:ordinary`; material=false; `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:82` — `rule:ordinary`; material=false; `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:86` — `syntax`; material=false; `syntax KItem ::= #dsetV(Val, Val, Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:87` — `rule:ordinary`; material=false; `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:90` — `syntax:function,total`; material=false; `syntax Int ::= normIdxD(Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:91` — `rule:ordinary`; material=false; `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:92` — `rule:ordinary`; material=false; `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:95` — `rule:ordinary`; material=false; `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:97` — `syntax:function`; material=false; `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:98` — `rule:ordinary`; material=false; `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:99` — `rule:ordinary`; material=false; `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:101` — `syntax:function`; material=false; `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:102` — `rule:ordinary`; material=false; `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/dict.k:103` — `rule:ordinary`; material=false; `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/float.k`

- `reference-semantics/semantics/float.k:20` — `syntax`; material=false; `syntax Val ::= Float`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:21` — `rule:ordinary`; material=false; `rule <k> Float(F:Float) => F ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:24` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:25` — `rule:concrete`; material=false; `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:27` — `rule:ordinary`; material=false; `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:30` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:31` — `rule:concrete`; material=false; `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:32` — `rule:ordinary`; material=false; `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:37` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:38` — `rule:concrete`; material=false; `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:39` — `rule:ordinary`; material=false; `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:43` — `rule:ordinary`; material=false; `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:44` — `rule:ordinary`; material=false; `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:50` — `syntax:function,total,no-evaluators`; material=false; `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:51` — `rule:concrete`; material=false; `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:52` — `rule:ordinary`; material=false; `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:54` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:55` — `rule:concrete`; material=false; `rule absF(F:Float) => absFloat(F) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:56` — `rule:ordinary`; material=false; `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:61` — `rule:ordinary`; material=false; `rule <k> Import(_:String) => .K ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:65` — `syntax`; material=false; `syntax KItem ::= "#mathCeil"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:66` — `rule:priority`; material=false; `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:67` — `rule:ordinary`; material=false; `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:70` — `syntax`; material=false; `syntax KItem ::= "#mathFloor"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:71` — `rule:priority`; material=false; `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:72` — `rule:ordinary`; material=false; `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:73` — `syntax:function,total`; material=false; `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:74` — `rule:concrete`; material=false; `rule floorFI(I:Int) => I [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:75` — `rule:concrete`; material=false; `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:78` — `rule:ordinary`; material=false; `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:79` — `rule:ordinary`; material=false; `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:82` — `syntax`; material=false; `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:83` — `rule:priority`; material=false; `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:84` — `rule:ordinary`; material=false; `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:85` — `rule:ordinary`; material=false; `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:86` — `syntax:function,total`; material=false; `syntax Float ::= toF(Val) [function, total, symbol(toF)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:87` — `rule:concrete`; material=false; `rule toF(F:Float) => F [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:88` — `rule:concrete`; material=false; `rule toF(I:Int) => intToF(I) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:93` — `syntax:function,total`; material=false; `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:94` — `rule:concrete`; material=false; `rule ceilF(I:Int) => I [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:95` — `rule:concrete`; material=false; `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:99` — `rule:ordinary`; material=false; `rule applyUn("-", F:Float) => 0.0 -Float F`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:103` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:104` — `rule:concrete`; material=false; `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:105` — `rule:ordinary`; material=false; `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:107` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:108` — `rule:concrete`; material=false; `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:109` — `rule:ordinary`; material=false; `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:111` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:112` — `rule:concrete`; material=false; `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:113` — `rule:ordinary`; material=false; `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:115` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:116` — `rule:concrete`; material=false; `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:117` — `rule:ordinary`; material=false; `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:119` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:120` — `rule:concrete`; material=false; `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:121` — `rule:ordinary`; material=false; `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:125` — `syntax:function,total,no-evaluators`; material=false; `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:126` — `rule:concrete`; material=false; `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:127` — `rule:ordinary`; material=false; `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:128` — `rule:ordinary`; material=false; `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:129` — `rule:ordinary`; material=false; `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:132` — `rule:ordinary`; material=false; `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:133` — `rule:ordinary`; material=false; `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:134` — `rule:ordinary`; material=false; `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:135` — `rule:ordinary`; material=false; `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:136` — `rule:ordinary`; material=false; `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:137` — `rule:ordinary`; material=false; `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:138` — `rule:ordinary`; material=false; `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:139` — `rule:ordinary`; material=false; `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:142` — `syntax:function,total,no-evaluators`; material=false; `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:143` — `rule:concrete`; material=false; `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:144` — `rule:ordinary`; material=false; `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:145` — `rule:ordinary`; material=false; `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:146` — `rule:ordinary`; material=false; `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:147` — `rule:ordinary`; material=false; `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:148` — `rule:ordinary`; material=false; `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:149` — `rule:ordinary`; material=false; `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:150` — `rule:ordinary`; material=false; `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:151` — `rule:ordinary`; material=false; `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:154` — `rule:ordinary`; material=false; `rule applyCmp("==", V:Val, noneV) => V ==K noneV`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:155` — `rule:ordinary`; material=false; `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:160` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:161` — `rule:concrete`; material=false; `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:162` — `rule:concrete`; material=false; `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:165` — `syntax:function`; material=false; `syntax Int ::= headIS(IntSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:166` — `rule:ordinary`; material=false; `rule headIS(iCons(C:Int, _:IntSeq)) => C`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:167` — `syntax:function,total`; material=false; `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:168` — `rule:ordinary`; material=false; `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:169` — `rule:ordinary`; material=false; `rule intPartAcc(.IntSeq, A:Int) => A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:170` — `rule:ordinary`; material=false; `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:171` — `rule:ordinary`; material=false; `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:173` — `syntax:function,total`; material=false; `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:174` — `rule:ordinary`; material=false; `rule fracPart(.IntSeq) => 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:175` — `rule:ordinary`; material=false; `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:176` — `rule:ordinary`; material=false; `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:177` — `rule:ordinary`; material=false; `rule fracAcc(.IntSeq, A:Int) => A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:178` — `rule:ordinary`; material=false; `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:179` — `syntax:function,total`; material=false; `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:180` — `rule:ordinary`; material=false; `rule fracScale(.IntSeq) => 1`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:181` — `rule:ordinary`; material=false; `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:182` — `rule:ordinary`; material=false; `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:183` — `rule:ordinary`; material=false; `rule fscAcc(.IntSeq, A:Int) => A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:184` — `rule:ordinary`; material=false; `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:185` — `rule:ordinary`; material=false; `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:186` — `rule:ordinary`; material=false; `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:187` — `rule:ordinary`; material=false; `rule applyBuiltin("float", F:Float, .Vals) => F`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:190` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:191` — `rule:concrete`; material=false; `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:192` — `rule:ordinary`; material=false; `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:195` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:196` — `rule:concrete`; material=false; `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:197` — `rule:ordinary`; material=false; `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:198` — `rule:ordinary`; material=false; `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:199` — `rule:ordinary`; material=false; `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:200` — `rule:ordinary`; material=false; `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:201` — `rule:ordinary`; material=false; `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:202` — `rule:ordinary`; material=false; `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:203` — `rule:ordinary`; material=false; `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:204` — `rule:ordinary`; material=false; `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:205` — `rule:ordinary`; material=false; `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:206` — `rule:ordinary`; material=false; `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:209` — `syntax:function,total,no-evaluators`; material=false; `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:210` — `rule:concrete`; material=false; `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:211` — `rule:ordinary`; material=false; `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:213` — `rule:ordinary`; material=false; `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:214` — `rule:ordinary`; material=false; `rule applyBuiltin("float", F:Float, .Vals) => F`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:217` — `syntax:function,total,no-evaluators`; material=false; `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:218` — `rule:concrete`; material=false; `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:223` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:224` — `rule:concrete`; material=false; `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:227` — `rule:ordinary`; material=false; `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:228` — `rule:ordinary`; material=false; `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:230` — `syntax:function,total,no-evaluators`; material=false; `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:231` — `rule:concrete`; material=false; `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:232` — `syntax`; material=false; `syntax KItem ::= "#mathSqrt"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:233` — `rule:priority`; material=false; `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:234` — `rule:ordinary`; material=false; `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:235` — `rule:ordinary`; material=false; `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:243` — `syntax`; material=false; `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:244` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:245` — `rule:ordinary`; material=false; `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:246` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:247` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:250` — `syntax`; material=false; `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:251` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:252` — `rule:ordinary`; material=false; `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:253` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:254` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:261` — `syntax`; material=false; `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:262` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:265` — `rule:ordinary`; material=false; `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:266` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:267` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/float.k:270` — `rule:ordinary`; material=false; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/functions.k`

- `reference-semantics/semantics/functions.k:8` — `syntax`; material=true; `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/functions.k:14` — `rule:ordinary`; material=true; `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:18` — `syntax`; material=true; `syntax Expr ::= closureExpr(ParamNames, Stmts)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/functions.k:19` — `rule:ordinary`; material=true; `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:27` — `syntax`; material=false; `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:31` — `syntax`; material=false; `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:33` — `rule:ordinary`; material=false; `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:36` — `rule:ordinary`; material=false; `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:42` — `rule:ordinary`; material=false; `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:47` — `rule:ordinary`; material=false; `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:50` — `rule:ordinary`; material=false; `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:53` — `rule:ordinary`; material=false; `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:59` — `rule:ordinary`; material=false; `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/functions.k:63` — `rule:ordinary`; material=true; `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:64` — `rule:ordinary`; material=true; `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:68` — `rule:priority`; material=true; `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:78` — `rule:ordinary`; material=true; `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:80` — `rule:ordinary`; material=true; `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/functions.k:85` — `rule:ordinary`; material=true; `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
### `reference-semantics/semantics/int.k`

- `reference-semantics/semantics/int.k:7` — `rule:ordinary`; material=false; `rule applyUn("-", I:Int) => 0 -Int I`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:9` — `rule:ordinary`; material=true; `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/int.k:11` — `rule:ordinary`; material=false; `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:12` — `rule:ordinary`; material=false; `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:13` — `rule:ordinary`; material=false; `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:14` — `rule:ordinary`; material=false; `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:15` — `rule:ordinary`; material=false; `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:16` — `rule:ordinary`; material=false; `rule applyBin("`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:17` — `rule:ordinary`; material=false; `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:19` — `syntax:function`; material=false; `syntax Int ::= pyMod(Int, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:20` — `rule:ordinary`; material=false; `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:22` — `rule:ordinary`; material=false; `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:23` — `rule:ordinary`; material=true; `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/int.k:24` — `rule:ordinary`; material=false; `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:25` — `rule:ordinary`; material=false; `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:26` — `rule:ordinary`; material=false; `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/int.k:27` — `rule:ordinary`; material=false; `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/iter.k`

- `reference-semantics/semantics/iter.k:8` — `syntax`; material=true; `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
### `reference-semantics/semantics/list.k`

- `reference-semantics/semantics/list.k:9` — `rule:ordinary`; material=true; `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/list.k:10` — `rule:ordinary`; material=true; `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/list.k:13` — `syntax`; material=false; `syntax ApplyK ::= "toList"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:14` — `rule:ordinary`; material=false; `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:15` — `rule:ordinary`; material=false; `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:18` — `syntax:function,total`; material=false; `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:19` — `rule:ordinary`; material=false; `rule valSeqConcat(.ValSeq, T:ValSeq) => T`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:20` — `rule:ordinary`; material=false; `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:24` — `rule:priority`; material=false; `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:27` — `rule:ordinary`; material=false; `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:28` — `rule:ordinary`; material=false; `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:33` — `syntax:function,total`; material=false; `syntax Bool ::= hasRefVS(ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:34` — `rule:ordinary`; material=false; `rule hasRefVS(.ValSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:35` — `rule:ordinary`; material=false; `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:37` — `syntax:function`; material=false; `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:39` — `rule:ordinary`; material=false; `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:40` — `rule:ordinary`; material=false; `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:41` — `rule:ordinary`; material=false; `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:42` — `rule:ordinary`; material=false; `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:45` — `rule:ordinary`; material=false; `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:47` — `rule:ordinary`; material=false; `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:49` — `rule:ordinary`; material=false; `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:50` — `rule:owise`; material=false; `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:53` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:58` — `syntax`; material=false; `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:59` — `rule:ordinary`; material=false; `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:60` — `rule:ordinary`; material=false; `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:61` — `rule:ordinary`; material=false; `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:62` — `rule:ordinary`; material=false; `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:63` — `rule:ordinary`; material=false; `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:65` — `rule:ordinary`; material=false; `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/list.k:67` — `rule:ordinary`; material=false; `rule <k> B:Bool ~> #notB => notBool B ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/methods.k`

- `reference-semantics/semantics/methods.k:10` — `syntax:function`; material=false; `syntax Val ::= applyMethod(Val, String, Vals) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:13` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:14` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:15` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:16` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:19` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:20` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:21` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:26` — `rule:ordinary`; material=false; `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:27` — `syntax:function,total`; material=false; `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:28` — `rule:ordinary`; material=false; `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:29` — `rule:ordinary`; material=false; `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:30` — `rule:ordinary`; material=false; `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:34` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:35` — `syntax:function`; material=false; `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:36` — `rule:ordinary`; material=false; `rule cntSub(.IntSeq, _:IntSeq) => 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:37` — `rule:ordinary`; material=false; `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:39` — `rule:ordinary`; material=false; `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:41` — `syntax:function,total`; material=false; `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:42` — `rule:ordinary`; material=false; `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:43` — `rule:owise`; material=false; `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:44` — `rule:ordinary`; material=false; `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:47` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:48` — `syntax:function,total`; material=false; `syntax IntSeq ::= trimWS(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:49` — `rule:ordinary`; material=false; `rule trimWS(.IntSeq) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:50` — `rule:ordinary`; material=false; `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:51` — `rule:ordinary`; material=false; `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:52` — `syntax:function,total`; material=false; `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:53` — `rule:ordinary`; material=false; `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:54` — `rule:ordinary`; material=false; `rule revISAcc(.IntSeq, A:IntSeq) => A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:55` — `rule:ordinary`; material=false; `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:58` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:61` — `rule:ordinary`; material=false; `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:64` — `rule:ordinary`; material=false; `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:65` — `syntax:function,total`; material=false; `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:66` — `rule:ordinary`; material=false; `rule cntOccVS(.ValSeq, _:Val) => 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:67` — `rule:ordinary`; material=false; `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:68` — `rule:ordinary`; material=false; `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:72` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:75` — `syntax:function`; material=false; `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:76` — `rule:ordinary`; material=false; `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:77` — `rule:ordinary`; material=false; `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:79` — `rule:ordinary`; material=false; `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:82` — `syntax:function`; material=false; `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:83` — `rule:ordinary`; material=false; `rule flushTok(ACC:ValSeq, .IntSeq) => ACC`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:84` — `rule:ordinary`; material=false; `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:85` — `syntax:function,total`; material=false; `syntax Bool ::= isWSC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:86` — `rule:ordinary`; material=false; `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:89` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:94` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:97` — `syntax:function`; material=false; `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:98` — `rule:ordinary`; material=false; `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:99` — `rule:ordinary`; material=false; `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:101` — `rule:ordinary`; material=false; `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:104` — `rule:ordinary`; material=false; `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:106` — `syntax:function,total`; material=false; `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:107` — `rule:ordinary`; material=false; `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:108` — `rule:ordinary`; material=false; `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:109` — `rule:ordinary`; material=false; `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:112` — `syntax:function,total`; material=false; `syntax Bool ::= isUpperC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:113` — `rule:ordinary`; material=false; `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:115` — `syntax:function,total`; material=false; `syntax Bool ::= isLowerC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:116` — `rule:ordinary`; material=false; `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:118` — `syntax:function,total`; material=false; `syntax Bool ::= isAlphaC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:119` — `rule:ordinary`; material=false; `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:121` — `syntax:function,total`; material=false; `syntax Bool ::= isDigitC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:122` — `rule:ordinary`; material=false; `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:124` — `syntax:function,total`; material=false; `syntax Bool ::= hasUpper(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:125` — `rule:ordinary`; material=false; `rule hasUpper(.IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:126` — `rule:ordinary`; material=false; `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:128` — `syntax:function,total`; material=false; `syntax Bool ::= hasLower(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:129` — `rule:ordinary`; material=false; `rule hasLower(.IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:130` — `rule:ordinary`; material=false; `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:132` — `syntax:function,total`; material=false; `syntax Bool ::= allAlpha(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:133` — `rule:ordinary`; material=false; `rule allAlpha(.IntSeq) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:134` — `rule:ordinary`; material=false; `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:136` — `syntax:function,total`; material=false; `syntax Bool ::= allDigit(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:137` — `rule:ordinary`; material=false; `rule allDigit(.IntSeq) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:138` — `rule:ordinary`; material=false; `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:140` — `syntax:function,total`; material=false; `syntax Int ::= lowerC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:142` — `rule:ordinary`; material=false; `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:143` — `rule:owise`; material=false; `rule lowerC(C:Int) => C [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:145` — `syntax:function,total`; material=false; `syntax Int ::= upperC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:146` — `rule:ordinary`; material=false; `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:147` — `rule:owise`; material=false; `rule upperC(C:Int) => C [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:149` — `syntax:function,total`; material=false; `syntax Int ::= swapC(Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:150` — `rule:ordinary`; material=false; `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:151` — `rule:ordinary`; material=false; `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:152` — `rule:owise`; material=false; `rule swapC(C:Int) => C [owise]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:154` — `syntax:function,total`; material=false; `syntax IntSeq ::= mapLower(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:155` — `rule:ordinary`; material=false; `rule mapLower(.IntSeq) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:156` — `rule:ordinary`; material=false; `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:158` — `syntax:function,total`; material=false; `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:159` — `rule:ordinary`; material=false; `rule mapUpper(.IntSeq) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:160` — `rule:ordinary`; material=false; `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:162` — `syntax:function,total`; material=false; `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:163` — `rule:ordinary`; material=false; `rule mapSwap(.IntSeq) => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:164` — `rule:ordinary`; material=false; `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:166` — `syntax:function,total`; material=false; `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:167` — `rule:ordinary`; material=false; `rule startsWith(.IntSeq, _:IntSeq) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:168` — `rule:ordinary`; material=false; `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/methods.k:169` — `rule:ordinary`; material=false; `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/operators.k`

- `reference-semantics/semantics/operators.k:10` — `rule:ordinary`; material=false; `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:12` — `rule:ordinary`; material=false; `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:15` — `context`; material=true; `context Compare(HOLE, _)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/operators.k:16` — `context`; material=true; `context Compare(_:Val, CmpOp(_, HOLE))`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/operators.k:17` — `rule:owise`; material=true; `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/operators.k:19` — `rule:ordinary`; material=false; `rule applyCmp("is", V:Val, noneV) => V ==K noneV`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:20` — `rule:ordinary`; material=false; `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:25` — `rule:priority`; material=false; `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:28` — `rule:priority`; material=false; `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:34` — `rule:priority`; material=false; `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:38` — `rule:priority`; material=false; `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/operators.k:44` — `rule:priority`; material=false; `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/range.k`

- `reference-semantics/semantics/range.k:9` — `syntax:function,total`; material=false; `syntax Bool ::= inRange(Int, Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:10` — `rule:ordinary`; material=false; `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:12` — `syntax:function`; material=false; `syntax Int ::= rangeLen(Int, Int, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:13` — `rule:ordinary`; material=false; `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:15` — `rule:ordinary`; material=false; `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:17` — `rule:ordinary`; material=false; `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:20` — `rule:ordinary`; material=false; `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/range.k:23` — `rule:ordinary`; material=false; `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/set.k`

- `reference-semantics/semantics/set.k:8` — `syntax`; material=false; `syntax Val ::= setV(IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:11` — `syntax:function,total`; material=false; `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:12` — `rule:ordinary`; material=false; `rule codeIn(_:Int, .IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:13` — `rule:ordinary`; material=false; `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:16` — `syntax:function,total`; material=false; `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] | dedupFrom(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:18` — `rule:ordinary`; material=false; `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:19` — `rule:ordinary`; material=false; `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:20` — `rule:ordinary`; material=false; `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:22` — `rule:ordinary`; material=false; `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:25` — `syntax:function,total`; material=false; `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:26` — `rule:ordinary`; material=false; `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:27` — `rule:ordinary`; material=false; `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:31` — `syntax:function,total`; material=false; `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:32` — `rule:ordinary`; material=false; `rule subsetCodes(.IntSeq, _:IntSeq) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:33` — `rule:ordinary`; material=false; `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:35` — `syntax:function,total`; material=false; `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:36` — `rule:ordinary`; material=false; `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/set.k:39` — `rule:ordinary`; material=false; `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/sort.k`

- `reference-semantics/semantics/sort.k:18` — `syntax:function,total,no-evaluators`; material=false; `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:19` — `syntax:function`; material=false; `syntax ValSeq ::= insVS(Int, ValSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:20` — `rule:concrete`; material=false; `rule sortVS(.ValSeq) => .ValSeq [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:21` — `rule:concrete`; material=false; `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:22` — `rule:concrete`; material=false; `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:23` — `rule:concrete`; material=false; `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:24` — `rule:concrete`; material=false; `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:26` — `syntax:function`; material=false; `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:27` — `rule:concrete`; material=false; `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:28` — `rule:concrete`; material=false; `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:29` — `rule:concrete`; material=false; `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:31` — `rule:concrete`; material=false; `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:36` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:40` — `rule:priority`; material=false; `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:49` — `syntax:function,total,no-evaluators`; material=false; `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:51` — `syntax:function,total`; material=false; `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:53` — `rule:ordinary`; material=false; `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:54` — `rule:ordinary`; material=false; `rule revVSAcc(.ValSeq, A:ValSeq) => A`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:55` — `rule:ordinary`; material=false; `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:57` — `syntax:function,total`; material=false; `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:58` — `rule:ordinary`; material=false; `rule condRev(S:ValSeq, false) => S`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:59` — `rule:ordinary`; material=false; `rule condRev(S:ValSeq, true) => revVS(S)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:61` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:63` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/sort.k:65` — `rule:ordinary`; material=false; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/str.k`

- `reference-semantics/semantics/str.k:8` — `rule:ordinary`; material=false; `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:9` — `rule:ordinary`; material=false; `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:13` — `syntax:function`; material=false; `syntax IntSeq ::= strToCodes(String) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:14` — `rule:ordinary`; material=false; `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:15` — `rule:ordinary`; material=false; `rule strToCodes("") => .IntSeq`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:16` — `rule:ordinary`; material=false; `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:20` — `syntax:function,total`; material=false; `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:21` — `rule:ordinary`; material=false; `rule seqConcat(.IntSeq, T:IntSeq) => T`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:22` — `rule:ordinary`; material=false; `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:24` — `rule:ordinary`; material=false; `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:25` — `rule:ordinary`; material=false; `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:26` — `rule:ordinary`; material=false; `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:29` — `rule:ordinary`; material=false; `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:30` — `rule:ordinary`; material=false; `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:32` — `syntax:function,total`; material=false; `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:33` — `rule:ordinary`; material=false; `rule strPrefix(.IntSeq, _:IntSeq) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:34` — `rule:ordinary`; material=false; `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:35` — `rule:ordinary`; material=false; `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:37` — `syntax:function,total`; material=false; `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:38` — `rule:ordinary`; material=false; `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:39` — `rule:ordinary`; material=false; `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:40` — `rule:ordinary`; material=false; `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:48` — `syntax:function,total`; material=false; `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:49` — `rule:ordinary`; material=false; `rule strLt(.IntSeq, .IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:50` — `rule:ordinary`; material=false; `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:51` — `rule:ordinary`; material=false; `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:52` — `rule:ordinary`; material=false; `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:53` — `rule:ordinary`; material=false; `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:54` — `rule:ordinary`; material=false; `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:56` — `rule:ordinary`; material=false; `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:57` — `rule:ordinary`; material=false; `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:58` — `rule:ordinary`; material=false; `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/str.k:59` — `rule:ordinary`; material=false; `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/subscript.k`

- `reference-semantics/semantics/subscript.k:11` — `syntax:function,total`; material=false; `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:12` — `rule:ordinary`; material=false; `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:13` — `rule:ordinary`; material=false; `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:16` — `syntax:function`; material=false; `syntax Int ::= intSeqAt(IntSeq, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:17` — `rule:ordinary`; material=false; `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:18` — `rule:ordinary`; material=false; `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:21` — `syntax:function,total`; material=false; `syntax Int ::= normIdx(Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:22` — `rule:ordinary`; material=false; `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:23` — `rule:ordinary`; material=false; `rule normIdx(I:Int, _:Int) => I requires I >=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:27` — `context`; material=false; `context Subscript(HOLE, _)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:28` — `context`; material=false; `context Subscript(_:Val, HOLE:Expr)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:31` — `rule:priority`; material=false; `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:35` — `rule:ordinary`; material=false; `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:37` — `syntax:function`; material=false; `syntax Val ::= applyIndex(Val, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:38` — `rule:ordinary`; material=false; `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:39` — `rule:ordinary`; material=false; `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:40` — `rule:ordinary`; material=false; `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:44` — `syntax`; material=false; `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:49` — `syntax`; material=false; `syntax OptInt ::= "noB" | someB(Int)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:50` — `rule:ordinary`; material=false; `rule <k> #evalB(NoBound) => noB ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:51` — `rule:ordinary`; material=false; `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:52` — `rule:ordinary`; material=false; `rule <k> I:Int ~> #toSome => someB(I) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:54` — `rule:ordinary`; material=false; `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:55` — `rule:ordinary`; material=false; `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:56` — `rule:ordinary`; material=false; `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:58` — `rule:priority`; material=false; `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:61` — `rule:ordinary`; material=false; `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:63` — `syntax:function`; material=false; `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:64` — `rule:ordinary`; material=false; `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:66` — `rule:ordinary`; material=false; `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:68` — `rule:ordinary`; material=false; `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:72` — `syntax:function,total`; material=false; `syntax Int ::= slStep(OptInt) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:73` — `rule:ordinary`; material=false; `rule slStep(noB) => 1`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:74` — `rule:ordinary`; material=false; `rule slStep(someB(S:Int)) => S`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:76` — `syntax:function`; material=false; `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:77` — `rule:ordinary`; material=false; `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:79` — `rule:ordinary`; material=false; `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:81` — `rule:ordinary`; material=false; `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:83` — `syntax:function`; material=false; `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:84` — `rule:ordinary`; material=false; `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:86` — `rule:ordinary`; material=false; `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:88` — `rule:ordinary`; material=false; `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:90` — `syntax:function,total`; material=false; `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:91` — `rule:ordinary`; material=false; `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:93` — `rule:ordinary`; material=false; `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:96` — `syntax:function,total`; material=false; `syntax Int ::= clampLo(Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:97` — `rule:ordinary`; material=false; `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:99` — `rule:ordinary`; material=false; `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:102` — `syntax:function,total`; material=false; `syntax Int ::= clampHi(Int, Int, Int) [function, total]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:103` — `rule:ordinary`; material=false; `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:105` — `rule:ordinary`; material=false; `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:109` — `syntax:function`; material=false; `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:110` — `rule:ordinary`; material=false; `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:113` — `rule:ordinary`; material=false; `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:116` — `syntax:function`; material=false; `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:117` — `rule:ordinary`; material=false; `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/subscript.k:120` — `rule:ordinary`; material=false; `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `reference-semantics/semantics/syntax.k`

- `reference-semantics/semantics/syntax.k:9` — `syntax:macro,strict,seqstrict`; material=true; `syntax Expr ::= "Int" "(" Int ")" | "Float" "(" Float ")" | "Bool" "(" Bool ")" | "Name" "(" String ")" | "Str" "(" String ")" | "UnaryOp" "(" String "," Expr ")" [strict(2)] | "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp" "(" String "," Exprs ")" | "ListExpr" "(" Exprs ")" | "DictExpr" "(" Entries ")" | "ListComp" "(" Expr "," CompFors ")" [macro] | "GenExp" "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda" "(" Params "," Expr ")" | "KwArg" "(" String "," Expr ")" | "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call" "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare" "(" Expr "," CmpOp ")"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/syntax.k:32` — `syntax`; material=true; `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/syntax.k:33` — `syntax`; material=false; `syntax Entry ::= "Entry" "(" Expr "," Expr ")"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:34` — `syntax`; material=false; `syntax Entries ::= List{Entry, ","}`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:35` — `syntax`; material=false; `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:36` — `syntax`; material=false; `syntax CompFors ::= List{CompFor, ""}`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:37` — `syntax`; material=false; `syntax Exprs ::= List{Expr, ","}`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:38` — `syntax`; material=false; `syntax Index ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:39` — `syntax`; material=false; `syntax Bound ::= Expr | "NoBound"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:41` — `syntax:strict`; material=true; `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] | "Import" "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While" "(" Expr "," Stmts ")" | "Break" | "Continue" | "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return" "(" Expr ")" [strict] | "Assert" "(" Expr ")" [strict] | "Expr" "(" Expr ")" [strict] | "FuncDef" "(" String "," Params "," Stmts ")" | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/syntax.k:56` — `syntax`; material=true; `syntax Stmts ::= List{Stmt, ""}`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/syntax.k:57` — `syntax`; material=true; `syntax Params ::= "Params" "(" ParamNames ")"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/syntax.k:58` — `syntax`; material=false; `syntax CellVars ::= "CellVars" "(" ParamNames ")"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:59` — `syntax`; material=false; `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/syntax.k:60` — `syntax`; material=true; `syntax ParamNames ::= List{String, ","}`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/syntax.k:61` — `syntax`; material=true; `syntax Module ::= "Module" "(" Stmts ")"`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
### `reference-semantics/semantics/tuple.k`

- `reference-semantics/semantics/tuple.k:10` — `rule:ordinary`; material=false; `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:11` — `rule:ordinary`; material=false; `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:14` — `syntax`; material=false; `syntax ApplyK ::= "toTuple"`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:15` — `rule:ordinary`; material=false; `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:16` — `rule:ordinary`; material=false; `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:18` — `rule:ordinary`; material=false; `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:20` — `rule:ordinary`; material=false; `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:21` — `rule:ordinary`; material=false; `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:23` — `rule:ordinary`; material=false; `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:24` — `syntax:function`; material=false; `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:25` — `rule:ordinary`; material=false; `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:26` — `rule:ordinary`; material=false; `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:28` — `rule:ordinary`; material=false; `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:31` — `syntax`; material=true; `syntax KItem ::= #bindTgt(Expr, Val)`  
  Decision: FIXED-MATERIAL—declaration/configuration used by the submitted constructor term and fixed execution path.
- `reference-semantics/semantics/tuple.k:32` — `rule:ordinary`; material=true; `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/tuple.k:35` — `rule:priority`; material=true; `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`  
  Decision: FIXED-MATERIAL—selected supplied-semantics rule; inspected on the actual load/call/lookup/loop/len/int-comparison/return path and consistent with the modeled operation.
- `reference-semantics/semantics/tuple.k:42` — `rule:ordinary`; material=false; `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:43` — `rule:ordinary`; material=false; `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:44` — `rule:priority`; material=false; `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:49` — `syntax`; material=false; `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:50` — `rule:ordinary`; material=false; `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:51` — `rule:ordinary`; material=false; `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:52` — `rule:priority`; material=false; `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:55` — `rule:ordinary`; material=false; `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
- `reference-semantics/semantics/tuple.k:57` — `rule:ordinary`; material=false; `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`  
  Decision: FIXED-INERT—part of the integrity-checked supplied baseline; its outer constructor/function/type/guard is not reachable on this program's formal domain and it contributes no proof-local rewrite.
### `verification.k`

- `verification.k:8` — `syntax:function,total`; material=true; `syntax Bool ::= onlyStrings(ValSeq) [function, total]`  
  Decision: SOUND—proof-local declaration for the reviewed equations.
- `verification.k:9` — `rule:ordinary`; material=true; `rule onlyStrings(.ValSeq) => true`  
  Decision: SOUND—constructor recursion defines exactly the all-string predicate.
- `verification.k:10` — `rule:ordinary`; material=true; `rule onlyStrings(vCons(V:Val, REST:ValSeq)) => isStrV(V) andBool onlyStrings(REST)`  
  Decision: SOUND—constructor recursion defines exactly the all-string predicate.
- `verification.k:15` — `syntax:function,total`; material=true; `syntax IntSeq ::= stringCodes(Val) [function, total]`  
  Decision: SOUND—proof-local declaration for the reviewed equations.
- `verification.k:16` — `rule:ordinary`; material=true; `rule stringCodes(str(CS:IntSeq)) => CS`  
  Decision: SOUND—disjoint string projection and owise non-string default.
- `verification.k:17` — `rule:owise`; material=true; `rule stringCodes(_V:Val) => .IntSeq [owise]`  
  Decision: SOUND—disjoint string projection and owise non-string default.
- `verification.k:21` — `rule:simplification`; material=true; `rule seqLen(V:Val) => isLen(stringCodes(V)) requires isStrV(V) [simplification]`  
  Decision: SOUND—under isStrV(V), V is str(CS); both sides reduce to isLen(CS).
- `verification.k:26` — `syntax:function,total`; material=true; `syntax Int ::= totalLen(ValSeq) [function, total] | totalLenFrom(Int, ValSeq) [function, total]`  
  Decision: SOUND—proof-local declaration for the reviewed equations.
- `verification.k:28` — `rule:ordinary`; material=true; `rule totalLen(ITEMS:ValSeq) => totalLenFrom(0, ITEMS)`  
  Decision: SOUND—descending left-fold equations for summed string lengths.
- `verification.k:29` — `rule:ordinary`; material=true; `rule totalLenFrom(ACC:Int, .ValSeq) => ACC`  
  Decision: SOUND—descending left-fold equations for summed string lengths.
- `verification.k:30` — `rule:ordinary`; material=true; `rule totalLenFrom(ACC:Int, vCons(V:Val, REST:ValSeq)) => totalLenFrom(ACC +Int isLen(stringCodes(V)), REST)`  
  Decision: SOUND—descending left-fold equations for summed string lengths.
- `verification.k:34` — `syntax:function,total`; material=true; `syntax Val ::= lastLoopValue(ValSeq, Val) [function, total]`  
  Decision: SOUND—proof-local declaration for the reviewed equations.
- `verification.k:35` — `rule:ordinary`; material=true; `rule lastLoopValue(.ValSeq, OLD:Val) => OLD`  
  Decision: SOUND—descending equations for the final for-target value.
- `verification.k:36` — `rule:ordinary`; material=true; `rule lastLoopValue(vCons(V:Val, REST:ValSeq), _OLD:Val) => lastLoopValue(REST, V)`  
  Decision: SOUND—descending equations for the final for-target value.
### `spec.k`

- `spec.k:6` — `claim`; material=true; `claim [sum-loop]: <k> #loop( list(ITEMS:ValSeq), Name("string"), AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))) ) => .K ... </k> <env> L:Int </env> <scopes> 0 |-> scope(MODULE:Map, parent(-1)) -1 |-> builtinsScope L |-> scope( "strings" |-> ORIGINAL:Val "total" |-> (ACC:Int => totalLenFrom(ACC, ITEMS)) "string" |-> (OLD:Val => lastLoopValue(ITEMS, OLD)), parent(0) ) OTHER:Map </scopes> <scopeLoc> SL:Int </scopeLoc> <heap> HP:Map </heap> <heapLoc> HL:Int </heapLoc> <stack> STACK:List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires L >Int 0 andBool notBool ("len" in_keys(MODULE)) andBool onlyStrings(ITEMS)`  
  Decision: CLAIM—audited separately for satisfiable guards, exact program pinning, result constraint, and clean closure.
- `spec.k:39` — `claim`; material=true; `claim [entry-first]: <k> #loadAll(Module( FuncDef("_total_length", Params("strings"), Assign(Name("total"), Int(0)) Assign(Name("string"), NoneVal) For(Name("string"), Name("strings"), AugAssign(Name("total"), "+", Call(Name("len"), Name("string")))) Return(Name("total"))) FuncDef("total_match", Params("lst1", "lst2"), If(Compare( Call(Name("_total_length"), Name("lst1")), CmpOp("<=", Call(Name("_total_length"), Name("lst2")))), Return(Name("lst1")), .Stmts) Return(Name("lst2"))) )) ~> Call( Name("total_match"), list(A:ValSeq), list(B:ValSeq) ) => list(A) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope => 0 |-> scope( "_total_length" |-> closureVal( ("strings", .ParamNames), Assign(Name("total"), Int(0)) Assign(Name("string"), NoneVal) For(Name("string"), Name("strings"), AugAssign(Name("total"), "+", Call(Name("len"), Name("string")))) Return(Name("total")), 0 ) "total_match" |-> closureVal( ("lst1", "lst2", .ParamNames), If(Compare( Call(Name("_total_length"), Name("lst1")), CmpOp("<=", Call(Name("_total_length"), Name("lst2")))), Return(Name("lst1")), .Stmts) Return(Name("lst2")), 0 ), parent(-1) ) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires onlyStrings(A) andBool onlyStrings(B) andBool totalLen(A) <=Int totalLen(B)`  
  Decision: CLAIM—audited separately for satisfiable guards, exact program pinning, result constraint, and clean closure.
- `spec.k:103` — `claim`; material=true; `claim [entry-second]: <k> #loadAll(Module( FuncDef("_total_length", Params("strings"), Assign(Name("total"), Int(0)) Assign(Name("string"), NoneVal) For(Name("string"), Name("strings"), AugAssign(Name("total"), "+", Call(Name("len"), Name("string")))) Return(Name("total"))) FuncDef("total_match", Params("lst1", "lst2"), If(Compare( Call(Name("_total_length"), Name("lst1")), CmpOp("<=", Call(Name("_total_length"), Name("lst2")))), Return(Name("lst1")), .Stmts) Return(Name("lst2"))) )) ~> Call( Name("total_match"), list(A:ValSeq), list(B:ValSeq) ) => list(B) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope => 0 |-> scope( "_total_length" |-> closureVal( ("strings", .ParamNames), Assign(Name("total"), Int(0)) Assign(Name("string"), NoneVal) For(Name("string"), Name("strings"), AugAssign(Name("total"), "+", Call(Name("len"), Name("string")))) Return(Name("total")), 0 ) "total_match" |-> closureVal( ("lst1", "lst2", .ParamNames), If(Compare( Call(Name("_total_length"), Name("lst1")), CmpOp("<=", Call(Name("_total_length"), Name("lst2")))), Return(Name("lst1")), .Stmts) Return(Name("lst2")), 0 ), parent(-1) ) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code> requires onlyStrings(A) andBool onlyStrings(B) andBool totalLen(A) >Int totalLen(B)`  
  Decision: CLAIM—audited separately for satisfiable guards, exact program pinning, result constraint, and clean closure.
