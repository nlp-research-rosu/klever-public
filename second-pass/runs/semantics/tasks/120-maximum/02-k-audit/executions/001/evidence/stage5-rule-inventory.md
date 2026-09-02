# Exhaustive K inventory

Each row is one top-level K configuration, syntax declaration, context, claim, or rule. Full multiline source and the per-entry decision are in `stage5-rule-inventory.jsonl`.

- Files: 25
- Items: 931
- Rules: 697
- Syntax declarations: 228
- Contexts: 5
- Configurations: 1
- Claims found in definition/proof extension: 0
- Function-tagged declarations/items: 145
- Functional-tagged declarations/items: 0
- Total-tagged declarations/items: 107
- Opaque symbol-tagged items: 25
- No-evaluators-tagged items: 22
- Priority-tagged rules/items: 45
- Simplification-tagged rules/items: 1
- Concrete-tagged rules/items: 35
- Macro-tagged declarations/items: 5

## File hashes and counts

| File | SHA-256 | configuration | syntax | context | rule | claim |
|---|---|---:|---:|---:|---:|---:|
| `semantics.k` | `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97` | 0 | 0 | 0 | 0 | 0 |
| `semantics/assert.k` | `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b` | 0 | 0 | 0 | 3 | 0 |
| `semantics/bool.k` | `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd` | 0 | 0 | 1 | 13 | 0 |
| `semantics/builtins.k` | `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd` | 0 | 38 | 0 | 137 | 0 |
| `semantics/call.k` | `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4` | 0 | 3 | 0 | 21 | 0 |
| `semantics/comprehension.k` | `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7` | 0 | 3 | 0 | 7 | 0 |
| `semantics/concrete.k` | `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305` | 0 | 5 | 0 | 16 | 0 |
| `semantics/controls.k` | `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae` | 0 | 3 | 0 | 34 | 0 |
| `semantics/core.k` | `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e` | 1 | 37 | 0 | 46 | 0 |
| `semantics/dict.k` | `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580` | 0 | 12 | 0 | 28 | 0 |
| `semantics/float.k` | `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f` | 0 | 34 | 0 | 121 | 0 |
| `semantics/functions.k` | `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193` | 0 | 4 | 0 | 15 | 0 |
| `semantics/int.k` | `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5` | 0 | 1 | 0 | 16 | 0 |
| `semantics/iter.k` | `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f` | 0 | 1 | 0 | 0 | 0 |
| `semantics/list.k` | `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa` | 0 | 5 | 0 | 27 | 0 |
| `semantics/methods.k` | `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743` | 0 | 27 | 0 | 75 | 0 |
| `semantics/operators.k` | `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b` | 0 | 0 | 2 | 10 | 0 |
| `semantics/range.k` | `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d` | 0 | 2 | 0 | 6 | 0 |
| `semantics/set.k` | `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7` | 0 | 6 | 0 | 12 | 0 |
| `semantics/sort.k` | `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a` | 0 | 6 | 0 | 19 | 0 |
| `semantics/str.k` | `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f` | 0 | 5 | 0 | 28 | 0 |
| `semantics/subscript.k` | `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7` | 0 | 15 | 2 | 40 | 0 |
| `semantics/syntax.k` | `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6` | 0 | 16 | 0 | 0 | 0 |
| `semantics/tuple.k` | `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb` | 0 | 4 | 0 | 21 | 0 |
| `verification.k` | `21f4e09e6ddfa5288e8fed7f28fe83663f8afd898a6100b5516285e5d7fa37a7` | 0 | 1 | 0 | 2 | 0 |

## Rule classes

| Class | Count |
|---|---:|
| `concrete-semantic-rule` | 35 |
| `configuration-declaration` | 1 |
| `context-declaration` | 5 |
| `macro-expansion-rule` | 1 |
| `ordinary-semantic-rule` | 660 |
| `simplification-rule` | 1 |
| `syntax-declaration` | 228 |

## Complete line-addressed item list

| ID | Kind/class | Tags | Decision | First source line |
|---|---|---|---|---|
| `semantics/assert.k:6:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assert(V:Val) => .K ... </k>` |
| `semantics/assert.k:8:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assert(V:Val) ~> _ => .K </k>` |
| `semantics/assert.k:13:3` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>` |
| `semantics/bool.k:8:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyUn("not", V:Val) => notBool truthy(V)` |
| `semantics/bool.k:10:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2` |
| `semantics/bool.k:11:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2` |
| `semantics/bool.k:16:4` | `context` / `context-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `context BoolOp(_, (HOLE:Expr, _:Exprs))` |
| `semantics/bool.k:17:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>` |
| `semantics/bool.k:18:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>` |
| `semantics/bool.k:20:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>` |
| `semantics/bool.k:22:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>` |
| `semantics/bool.k:24:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>` |
| `semantics/bool.k:29:10` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>` |
| `semantics/bool.k:31:11` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>` |
| `semantics/bool.k:35:12` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>` |
| `semantics/bool.k:39:13` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>` |
| `semantics/bool.k:43:14` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>` |
| `semantics/builtins.k:17:1` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= applyBuiltin(String, Vals) [function]` |
| `semantics/builtins.k:20:2` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= seqLen(Val) [function]` |
| `semantics/builtins.k:21:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)` |
| `semantics/builtins.k:22:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqLen(list(VS:ValSeq))                  => vsLen(VS)` |
| `semantics/builtins.k:23:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)` |
| `semantics/builtins.k:24:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqLen(str(IS:IntSeq))                   => isLen(IS)` |
| `semantics/builtins.k:25:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqLen(setV(DS:IntSeq))                  => isLen(DS)` |
| `semantics/builtins.k:26:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)` |
| `semantics/builtins.k:32:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>` |
| `semantics/builtins.k:33:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>` |
| `semantics/builtins.k:34:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>` |
| `semantics/builtins.k:35:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>` |
| `semantics/builtins.k:36:13` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= charsOf(IntSeq) [function, total]` |
| `semantics/builtins.k:37:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule charsOf(.IntSeq)                => .ValSeq` |
| `semantics/builtins.k:38:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))` |
| `semantics/builtins.k:41:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))` |
| `semantics/builtins.k:44:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)` |
| `semantics/builtins.k:47:18` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #sumAcc(Iterable, Int) \| #sumCont(Int)` |
| `semantics/builtins.k:48:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>` |
| `semantics/builtins.k:49:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>` |
| `semantics/builtins.k:50:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)` |
| `semantics/builtins.k:54:22` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= intOf(Val) [function]` |
| `semantics/builtins.k:55:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intOf(I:Int)  => I` |
| `semantics/builtins.k:56:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi` |
| `semantics/builtins.k:59:25` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #allAcc(Iterable) \| "#allCont"` |
| `semantics/builtins.k:60:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>` |
| `semantics/builtins.k:61:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #allCont => true ... </k>` |
| `semantics/builtins.k:62:28` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>` |
| `semantics/builtins.k:64:29` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>` |
| `semantics/builtins.k:67:30` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #anyAcc(Iterable) \| "#anyCont"` |
| `semantics/builtins.k:68:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>` |
| `semantics/builtins.k:69:32` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #anyCont => false ... </k>` |
| `semantics/builtins.k:70:33` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>` |
| `semantics/builtins.k:72:34` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>` |
| `semantics/builtins.k:76:35` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #maxAcc0(Iterable) \| "#maxCont0" \| #maxAcc(Iterable, Int) \| #maxCont(Int)` |
| `semantics/builtins.k:77:36` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>` |
| `semantics/builtins.k:78:37` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>` |
| `semantics/builtins.k:80:38` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>` |
| `semantics/builtins.k:81:39` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>` |
| `semantics/builtins.k:82:40` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)` |
| `semantics/builtins.k:86:41` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #minAcc0(Iterable) \| "#minCont0" \| #minAcc(Iterable, Int) \| #minCont(Int)` |
| `semantics/builtins.k:87:42` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>` |
| `semantics/builtins.k:88:43` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>` |
| `semantics/builtins.k:90:44` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>` |
| `semantics/builtins.k:91:45` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>` |
| `semantics/builtins.k:92:46` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)` |
| `semantics/builtins.k:97:47` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= maxVals(Int, Vals) [function]` |
| `semantics/builtins.k:98:48` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)` |
| `semantics/builtins.k:99:49` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule maxVals(M:Int, .Vals)           => M` |
| `semantics/builtins.k:100:50` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)` |
| `semantics/builtins.k:102:51` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= minVals(Int, Vals) [function]` |
| `semantics/builtins.k:103:52` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)` |
| `semantics/builtins.k:104:53` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule minVals(M:Int, .Vals)           => M` |
| `semantics/builtins.k:105:54` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)` |
| `semantics/builtins.k:108:55` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))` |
| `semantics/builtins.k:111:56` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("bin", N:Int, .Vals)` |
| `semantics/builtins.k:114:57` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= binCodes(Int) [function, total]` |
| `semantics/builtins.k:115:58` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule binCodes(0) => iCons(48, .IntSeq)` |
| `semantics/builtins.k:116:59` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0` |
| `semantics/builtins.k:117:60` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]` |
| `semantics/builtins.k:118:61` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule binAcc(0, ACC:IntSeq) => ACC` |
| `semantics/builtins.k:119:62` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule binAcc(N:Int, ACC:IntSeq)` |
| `semantics/builtins.k:124:63` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))` |
| `semantics/builtins.k:126:64` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]` |
| `semantics/builtins.k:127:65` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule enumVS(.ValSeq, _:Int) => .ValSeq` |
| `semantics/builtins.k:128:66` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule enumVS(vCons(V:Val, R:ValSeq), I:Int)` |
| `semantics/builtins.k:132:67` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))` |
| `semantics/builtins.k:134:68` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]` |
| `semantics/builtins.k:135:69` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapStrVS(.ValSeq) => .ValSeq` |
| `semantics/builtins.k:136:70` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))` |
| `semantics/builtins.k:137:71` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))` |
| `semantics/builtins.k:140:72` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("int", I:Int, .Vals) => I` |
| `semantics/builtins.k:143:73` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C` |
| `semantics/builtins.k:144:74` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))` |
| `semantics/builtins.k:148:75` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))` |
| `semantics/builtins.k:149:76` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)` |
| `semantics/builtins.k:152:77` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48` |
| `semantics/builtins.k:156:78` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)` |
| `semantics/builtins.k:158:79` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]` |
| `semantics/builtins.k:159:80` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intDigAcc(.IntSeq, ACC:Int)             => ACC` |
| `semantics/builtins.k:160:81` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))` |
| `semantics/builtins.k:163:82` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)` |
| `semantics/builtins.k:164:83` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)` |
| `semantics/builtins.k:167:84` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))` |
| `semantics/builtins.k:169:85` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>` |
| `semantics/builtins.k:170:86` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k:171:87` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))` |
| `semantics/builtins.k:173:88` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>` |
| `semantics/builtins.k:174:89` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>` |
| `semantics/builtins.k:177:90` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)` |
| `semantics/builtins.k:178:91` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)` |
| `semantics/builtins.k:179:92` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)` |
| `semantics/builtins.k:187:93` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)` |
| `semantics/builtins.k:188:94` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= evalArith(IntSeq) [function]` |
| `semantics/builtins.k:189:95` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule evalArith(CS:IntSeq)` |
| `semantics/builtins.k:192:96` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax OpSeq ::= ".OpSeq" \| oCons(String, OpSeq)` |
| `semantics/builtins.k:194:97` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= evDigit(Int) [function, total]` |
| `semantics/builtins.k:195:98` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `semantics/builtins.k:196:99` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= evHead42(IntSeq) [function, total]` |
| `semantics/builtins.k:197:100` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule evHead42(iCons(42, _:IntSeq)) => true` |
| `semantics/builtins.k:198:101` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule evHead42(_:IntSeq)            => false [owise]` |
| `semantics/builtins.k:199:102` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= evHead47(IntSeq) [function, total]` |
| `semantics/builtins.k:200:103` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule evHead47(iCons(47, _:IntSeq)) => true` |
| `semantics/builtins.k:201:104` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule evHead47(_:IntSeq)            => false [owise]` |
| `semantics/builtins.k:203:105` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax OpSeq ::= tokOps(IntSeq) [function, total]` |
| `semantics/builtins.k:204:106` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(.IntSeq)                 => .OpSeq` |
| `semantics/builtins.k:205:107` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)` |
| `semantics/builtins.k:206:108` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)` |
| `semantics/builtins.k:207:109` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))` |
| `semantics/builtins.k:208:110` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)` |
| `semantics/builtins.k:209:111` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))` |
| `semantics/builtins.k:210:112` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)` |
| `semantics/builtins.k:211:113` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))` |
| `semantics/builtins.k:212:114` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))` |
| `semantics/builtins.k:214:115` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= tokNds(IntSeq) [function, total]` |
| `semantics/builtins.k:216:116` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokNds(.IntSeq)                => .IntSeq` |
| `semantics/builtins.k:217:117` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)` |
| `semantics/builtins.k:218:118` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)` |
| `semantics/builtins.k:219:119` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)` |
| `semantics/builtins.k:221:120` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)` |
| `semantics/builtins.k:223:121` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]` |
| `semantics/builtins.k:225:122` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax EvPair ::= evp(OpSeq, IntSeq)` |
| `semantics/builtins.k:226:123` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= firstNdE(EvPair) [function, total]` |
| `semantics/builtins.k:227:124` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N` |
| `semantics/builtins.k:228:125` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule firstNdE(_:EvPair) => 0 [owise]` |
| `semantics/builtins.k:230:126` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= applyOpE(String, Int, Int) [function, total]` |
| `semantics/builtins.k:231:127` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyOpE("+",  A:Int, B:Int) => A +Int B` |
| `semantics/builtins.k:232:128` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyOpE("-",  A:Int, B:Int) => A -Int B` |
| `semantics/builtins.k:233:129` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyOpE("*",  A:Int, B:Int) => A *Int B` |
| `semantics/builtins.k:234:130` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyOpE("//", A:Int, B:Int) => A divInt B` |
| `semantics/builtins.k:235:131` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyOpE("**", A:Int, B:Int) => A ^Int B` |
| `semantics/builtins.k:236:132` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyOpE(_:String, A:Int, _:Int) => A [owise]` |
| `semantics/builtins.k:238:133` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]` |
| `semantics/builtins.k:239:134` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)` |
| `semantics/builtins.k:240:135` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))` |
| `semantics/builtins.k:241:136` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))` |
| `semantics/builtins.k:243:137` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]` |
| `semantics/builtins.k:244:138` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax EvPair ::= powCombE(Int, EvPair) [function, total]` |
| `semantics/builtins.k:245:139` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))` |
| `semantics/builtins.k:246:140` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))` |
| `semantics/builtins.k:247:141` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]` |
| `semantics/builtins.k:248:142` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))` |
| `semantics/builtins.k:250:143` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax EvPair ::= passMulE(EvPair) [function, total] \| passAddE(EvPair) [function, total]` |
| `semantics/builtins.k:251:144` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `semantics/builtins.k:252:145` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `semantics/builtins.k:253:146` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)` |
| `semantics/builtins.k:254:147` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)` |
| `semantics/builtins.k:255:148` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]` |
| `semantics/builtins.k:256:149` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))` |
| `semantics/builtins.k:257:150` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)` |
| `semantics/builtins.k:260:151` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)` |
| `semantics/builtins.k:263:152` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)` |
| `semantics/builtins.k:265:153` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= inLevelE(String, String) [function, total]` |
| `semantics/builtins.k:266:154` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"` |
| `semantics/builtins.k:267:155` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"` |
| `semantics/builtins.k:268:156` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule inLevelE(_:String, _:String) => false [owise]` |
| `semantics/builtins.k:269:157` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]` |
| `semantics/builtins.k:270:158` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)` |
| `semantics/builtins.k:271:159` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))` |
| `semantics/builtins.k:272:160` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]` |
| `semantics/builtins.k:273:161` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)` |
| `semantics/builtins.k:274:162` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))` |
| `semantics/builtins.k:279:163` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= "#md5"` |
| `semantics/builtins.k:280:164` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>` |
| `semantics/builtins.k:282:165` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>` |
| `semantics/builtins.k:283:166` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= md5Obj(IntSeq)` |
| `semantics/builtins.k:284:167` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))` |
| `semantics/builtins.k:285:168` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]` |
| `semantics/builtins.k:291:169` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)` |
| `semantics/builtins.k:292:170` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)` |
| `semantics/builtins.k:293:171` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isIntV(Val) [function] \| isStrV(Val) [function]` |
| `semantics/builtins.k:294:172` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isIntV(_:Int)         => true` |
| `semantics/builtins.k:295:173` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule isIntV(_:Val)         => false [owise]` |
| `semantics/builtins.k:296:174` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isStrV(str(_:IntSeq)) => true` |
| `semantics/builtins.k:297:175` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule isStrV(_:Val)         => false [owise]` |
| `semantics/call.k:16:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>` |
| `semantics/call.k:19:2` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #callee(Exprs)` |
| `semantics/call.k:20:3` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]` |
| `semantics/call.k:21:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>` |
| `semantics/call.k:24:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>` |
| `semantics/call.k:26:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>` |
| `semantics/call.k:27:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>` |
| `semantics/call.k:28:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>` |
| `semantics/call.k:29:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>` |
| `semantics/call.k:30:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>` |
| `semantics/call.k:31:11` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]` |
| `semantics/call.k:32:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>` |
| `semantics/call.k:38:13` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))` |
| `semantics/call.k:42:14` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))` |
| `semantics/call.k:47:15` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))` |
| `semantics/call.k:52:16` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isMutMethod(String) [function, total]` |
| `semantics/call.k:53:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isMutMethod(M:String)` |
| `semantics/call.k:56:18` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)` |
| `semantics/call.k:63:19` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))` |
| `semantics/call.k:69:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT` |
| `semantics/call.k:80:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT` |
| `semantics/call.k:87:22` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #allocCells(ParamNames)` |
| `semantics/call.k:88:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #allocCells(.ParamNames) => .K ... </k>` |
| `semantics/call.k:89:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>` |
| `semantics/comprehension.k:11:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `semantics/comprehension.k:12:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)` |
| `semantics/comprehension.k:14:3` | `syntax` / `syntax-declaration` | macro | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Stmts ::= compBody(CompFors, Expr) [macro]` |
| `semantics/comprehension.k:15:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule compBody(Gs:CompFors, ELT:Expr)` |
| `semantics/comprehension.k:18:5` | `syntax` / `syntax-declaration` | macro | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]` |
| `semantics/comprehension.k:19:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule compNest(.CompFors, ELT:Expr)` |
| `semantics/comprehension.k:21:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)` |
| `semantics/comprehension.k:24:8` | `syntax` / `syntax-declaration` | macro | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Expr ::= compGuard(Exprs) [macro]` |
| `semantics/comprehension.k:25:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule compGuard(.Exprs)             => Bool(true)` |
| `semantics/comprehension.k:26:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))` |
| `semantics/concrete.k:13:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>` |
| `semantics/concrete.k:16:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>` |
| `semantics/concrete.k:25:3` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= kvP(Val, Val)` |
| `semantics/concrete.k:26:4` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)` |
| `semantics/concrete.k:28:5` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))` |
| `semantics/concrete.k:31:6` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))` |
| `semantics/concrete.k:34:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)` |
| `semantics/concrete.k:36:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)` |
| `semantics/concrete.k:38:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)` |
| `semantics/concrete.k:42:10` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]` |
| `semantics/concrete.k:43:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)` |
| `semantics/concrete.k:44:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)` |
| `semantics/concrete.k:47:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)` |
| `semantics/concrete.k:51:14` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= kLt(Val, Val) [function]` |
| `semantics/concrete.k:52:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule kLt(I1:Int, I2:Int)             => I1 <Int I2` |
| `semantics/concrete.k:53:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule kLt(F1:Float, F2:Float)         => F1 <Float F2` |
| `semantics/concrete.k:54:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `semantics/concrete.k:56:18` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= unpairVS(ValSeq) [function, total]` |
| `semantics/concrete.k:57:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule unpairVS(.ValSeq) => .ValSeq` |
| `semantics/concrete.k:58:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))` |
| `semantics/concrete.k:59:21` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]` |
| `semantics/controls.k:9:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assign(Name(X:String), V:Val) => .K ... </k>` |
| `semantics/controls.k:12:2` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>` |
| `semantics/controls.k:20:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>` |
| `semantics/controls.k:27:4` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>` |
| `semantics/controls.k:35:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>` |
| `semantics/controls.k:36:6` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]` |
| `semantics/controls.k:37:7` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #bindImports(ParamNames)` |
| `semantics/controls.k:38:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindImports(.ParamNames) => .K ... </k>` |
| `semantics/controls.k:39:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>` |
| `semantics/controls.k:43:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>` |
| `semantics/controls.k:48:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Expr(_:Val) => .K ... </k>` |
| `semantics/controls.k:51:12` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #branch(Bool, Stmts, Stmts)` |
| `semantics/controls.k:52:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>` |
| `semantics/controls.k:53:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>` |
| `semantics/controls.k:54:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>` |
| `semantics/controls.k:57:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>` |
| `semantics/controls.k:59:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>` |
| `semantics/controls.k:65:18` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #loop(Val, Expr, Stmts) \| #loopStep(Expr, Stmts)` |
| `semantics/controls.k:69:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>` |
| `semantics/controls.k:71:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>` |
| `semantics/controls.k:72:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>` |
| `semantics/controls.k:73:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)` |
| `semantics/controls.k:77:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>` |
| `semantics/controls.k:78:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>` |
| `semantics/controls.k:79:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>` |
| `semantics/controls.k:81:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>` |
| `semantics/controls.k:85:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `semantics/controls.k:86:28` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Continue => #cont ... </k>` |
| `semantics/controls.k:87:29` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Break => #brk ... </k>` |
| `semantics/controls.k:88:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>` |
| `semantics/controls.k:89:31` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]` |
| `semantics/controls.k:90:32` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>` |
| `semantics/controls.k:91:33` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]` |
| `semantics/controls.k:95:34` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>` |
| `semantics/controls.k:98:35` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>` |
| `semantics/controls.k:101:36` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>` |
| `semantics/controls.k:106:37` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>` |
| `semantics/core.k:13:1` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= ".IntSeq" \| iCons(Int, IntSeq)` |
| `semantics/core.k:14:2` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= ".ValSeq" \| vCons(Val, ValSeq)` |
| `semantics/core.k:15:3` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Str    ::= str(IntSeq)` |
| `semantics/core.k:18:4` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Iterable ::= list(ValSeq)` |
| `semantics/core.k:25:5` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val      ::= Int` |
| `semantics/core.k:36:6` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Parent   ::= "root" \| parent(Int)` |
| `semantics/core.k:37:7` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Scope    ::= scope(Map, Parent)` |
| `semantics/core.k:38:8` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KResult  ::= Val` |
| `semantics/core.k:39:9` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Expr     ::= Val   // cooling puts results back into expression holes` |
| `semantics/core.k:40:10` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Vals     ::= List{Val, ","}` |
| `semantics/core.k:41:11` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Exc      ::= "NoExc" \| "AssertionError"` |
| `semantics/core.k:42:12` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax RetState ::= "noRet" \| retV(Val)` |
| `semantics/core.k:49:13` | `configuration` / `configuration-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `configuration` |
| `semantics/core.k:68:14` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isRefV(Val) [function, total]` |
| `semantics/core.k:69:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isRefV(ref(_:Int)) => true` |
| `semantics/core.k:70:16` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule isRefV(_:Val)      => false [owise]` |
| `semantics/core.k:75:17` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax HeapVal ::= cellV(Val)` |
| `semantics/core.k:76:18` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isCellRef(Val) [function, total]` |
| `semantics/core.k:77:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isCellRef(cellRef(_:Int)) => true` |
| `semantics/core.k:78:20` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule isCellRef(_:Val)          => false [owise]` |
| `semantics/core.k:85:21` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> cellRef(H:Int) => V ... </k>` |
| `semantics/core.k:95:22` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= kwV(String, Val)` |
| `semantics/core.k:96:23` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #kwTag(String)` |
| `semantics/core.k:97:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>` |
| `semantics/core.k:98:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>` |
| `semantics/core.k:100:26` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isKwV(Val) [function, total]` |
| `semantics/core.k:101:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isKwV(kwV(_:String, _:Val)) => true` |
| `semantics/core.k:102:28` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule isKwV(_:Val)                => false [owise]` |
| `semantics/core.k:106:29` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= cellsMark(ParamNames)` |
| `semantics/core.k:107:30` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ParamNames ::= cellsOf(Val) [function]` |
| `semantics/core.k:108:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS` |
| `semantics/core.k:109:32` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= pnMember(String, ParamNames) [function, total]` |
| `semantics/core.k:110:33` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule pnMember(_:String, .ParamNames) => false` |
| `semantics/core.k:111:34` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)` |
| `semantics/core.k:113:35` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #cellW(Val, Val)` |
| `semantics/core.k:114:36` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>` |
| `semantics/core.k:117:37` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #alloc(Val)` |
| `semantics/core.k:118:38` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #alloc(V:Val) => ref(N) ... </k>` |
| `semantics/core.k:124:39` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #loadAll(Module)` |
| `semantics/core.k:125:40` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>` |
| `semantics/core.k:126:41` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>` |
| `semantics/core.k:127:42` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> .Stmts => .K ... </k>` |
| `semantics/core.k:130:43` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #look(String, Int)` |
| `semantics/core.k:131:44` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>` |
| `semantics/core.k:132:45` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>` |
| `semantics/core.k:145:46` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #look(X:String, L:Int) => V ... </k>` |
| `semantics/core.k:152:47` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>` |
| `semantics/core.k:157:48` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Scope ::= "builtinsScope" [function, total]` |
| `semantics/core.k:158:49` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule builtinsScope` |
| `semantics/core.k:185:50` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ApplyK ::= toCall(Val)` |
| `semantics/core.k:186:51` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)` |
| `semantics/core.k:189:52` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>` |
| `semantics/core.k:190:53` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>` |
| `semantics/core.k:191:54` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>` |
| `semantics/core.k:194:55` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Int(I:Int)   => I ... </k>` |
| `semantics/core.k:195:56` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Bool(B:Bool) => B ... </k>` |
| `semantics/core.k:196:57` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> NoneVal      => noneV ... </k>` |
| `semantics/core.k:199:58` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= truthy(Val) [function]` |
| `semantics/core.k:200:59` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule truthy(B:Bool)          => B` |
| `semantics/core.k:201:60` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule truthy(noneV)           => false` |
| `semantics/core.k:202:61` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule truthy(I:Int)           => I =/=Int 0` |
| `semantics/core.k:203:62` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)` |
| `semantics/core.k:204:63` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)` |
| `semantics/core.k:205:64` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)` |
| `semantics/core.k:208:65` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val  ::= applyUn(String, Val) [function]` |
| `semantics/core.k:209:66` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val  ::= applyBin(String, Val, Val) [function]` |
| `semantics/core.k:210:67` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= applyCmp(String, Val, Val) [function]` |
| `semantics/core.k:213:68` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Vals ::= appendVal(Vals, Val) [function, total]` |
| `semantics/core.k:214:69` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule appendVal(.Vals, V:Val)              => V , .Vals` |
| `semantics/core.k:215:70` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)` |
| `semantics/core.k:217:71` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= vals2valSeq(Vals) [function, total]` |
| `semantics/core.k:218:72` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule vals2valSeq(.Vals)            => .ValSeq` |
| `semantics/core.k:219:73` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))` |
| `semantics/core.k:223:74` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= vsLen(ValSeq) [function, total]` |
| `semantics/core.k:224:75` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule vsLen(.ValSeq)                => 0` |
| `semantics/core.k:225:76` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)` |
| `semantics/core.k:227:77` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= isLen(IntSeq) [function, total]` |
| `semantics/core.k:228:78` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isLen(.IntSeq)                => 0` |
| `semantics/core.k:229:79` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)` |
| `semantics/core.k:233:80` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]` |
| `semantics/core.k:234:81` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq` |
| `semantics/core.k:235:82` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)` |
| `semantics/core.k:236:83` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))` |
| `semantics/core.k:238:84` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS` |
| `semantics/dict.k:20:1` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= dictV(ValSeq, ValSeq)` |
| `semantics/dict.k:23:2` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)` |
| `semantics/dict.k:26:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>` |
| `semantics/dict.k:27:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>` |
| `semantics/dict.k:28:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)` |
| `semantics/dict.k:30:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)` |
| `semantics/dict.k:32:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)` |
| `semantics/dict.k:37:8` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]` |
| `semantics/dict.k:38:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dHasKey(.ValSeq, _:Val)                => false` |
| `semantics/dict.k:39:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K` |
| `semantics/dict.k:40:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)` |
| `semantics/dict.k:43:12` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]` |
| `semantics/dict.k:44:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)` |
| `semantics/dict.k:45:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)` |
| `semantics/dict.k:49:15` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]` |
| `semantics/dict.k:50:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)` |
| `semantics/dict.k:52:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))` |
| `semantics/dict.k:54:18` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]` |
| `semantics/dict.k:58:19` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)` |
| `semantics/dict.k:63:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)` |
| `semantics/dict.k:64:21` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= applyIndexD(Val, Val) [function]` |
| `semantics/dict.k:65:22` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>` |
| `semantics/dict.k:70:23` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= dictSet(Val, Val, Val) [function]` |
| `semantics/dict.k:71:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))` |
| `semantics/dict.k:76:25` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #dsetK(String, Val)` |
| `semantics/dict.k:77:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>` |
| `semantics/dict.k:78:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>` |
| `semantics/dict.k:82:28` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>` |
| `semantics/dict.k:86:29` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #dsetV(Val, Val, Val)` |
| `semantics/dict.k:87:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>` |
| `semantics/dict.k:90:31` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= normIdxD(Int, Int) [function, total]` |
| `semantics/dict.k:91:32` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| `semantics/dict.k:92:33` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0` |
| `semantics/dict.k:95:34` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))` |
| `semantics/dict.k:97:35` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]` |
| `semantics/dict.k:98:36` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true` |
| `semantics/dict.k:99:37` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)` |
| `semantics/dict.k:101:38` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]` |
| `semantics/dict.k:102:39` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K` |
| `semantics/dict.k:103:40` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)` |
| `semantics/float.k:20:1` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= Float` |
| `semantics/float.k:21:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Float(F:Float) => F ... </k>` |
| `semantics/float.k:24:3` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]` |
| `semantics/float.k:25:4` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]` |
| `semantics/float.k:27:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)` |
| `semantics/float.k:30:6` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]` |
| `semantics/float.k:31:7` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]` |
| `semantics/float.k:32:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)` |
| `semantics/float.k:37:9` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]` |
| `semantics/float.k:38:10` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]` |
| `semantics/float.k:39:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)` |
| `semantics/float.k:43:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2` |
| `semantics/float.k:44:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)` |
| `semantics/float.k:50:14` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]` |
| `semantics/float.k:51:15` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]` |
| `semantics/float.k:52:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)` |
| `semantics/float.k:54:17` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]` |
| `semantics/float.k:55:18` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule absF(F:Float) => absFloat(F) [concrete]` |
| `semantics/float.k:56:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)` |
| `semantics/float.k:61:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Import(_:String) => .K ... </k>` |
| `semantics/float.k:65:21` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= "#mathCeil"` |
| `semantics/float.k:66:22` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]` |
| `semantics/float.k:67:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>` |
| `semantics/float.k:70:24` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= "#mathFloor"` |
| `semantics/float.k:71:25` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]` |
| `semantics/float.k:72:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>` |
| `semantics/float.k:73:27` | `syntax` / `syntax-declaration` | function, total, symbol | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]` |
| `semantics/float.k:74:28` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule floorFI(I:Int)   => I                        [concrete]` |
| `semantics/float.k:75:29` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]` |
| `semantics/float.k:78:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)` |
| `semantics/float.k:79:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)` |
| `semantics/float.k:82:32` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #mathPow1(Expr) \| #mathPow2(Val)` |
| `semantics/float.k:83:33` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]` |
| `semantics/float.k:84:34` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>` |
| `semantics/float.k:85:35` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>` |
| `semantics/float.k:86:36` | `syntax` / `syntax-declaration` | function, total, symbol | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= toF(Val) [function, total, symbol(toF)]` |
| `semantics/float.k:87:37` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule toF(F:Float) => F        [concrete]` |
| `semantics/float.k:88:38` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule toF(I:Int)   => intToF(I) [concrete]` |
| `semantics/float.k:93:39` | `syntax` / `syntax-declaration` | function, total, symbol | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]` |
| `semantics/float.k:94:40` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule ceilF(I:Int)   => I                       [concrete]` |
| `semantics/float.k:95:41` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]` |
| `semantics/float.k:99:42` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyUn("-", F:Float) => 0.0 -Float F` |
| `semantics/float.k:103:43` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]` |
| `semantics/float.k:104:44` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]` |
| `semantics/float.k:105:45` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)` |
| `semantics/float.k:107:46` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]` |
| `semantics/float.k:108:47` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]` |
| `semantics/float.k:109:48` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)` |
| `semantics/float.k:111:49` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]` |
| `semantics/float.k:112:50` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]` |
| `semantics/float.k:113:51` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)` |
| `semantics/float.k:115:52` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]` |
| `semantics/float.k:116:53` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]` |
| `semantics/float.k:117:54` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)` |
| `semantics/float.k:119:55` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]` |
| `semantics/float.k:120:56` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]` |
| `semantics/float.k:121:57` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)` |
| `semantics/float.k:125:58` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]` |
| `semantics/float.k:126:59` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]` |
| `semantics/float.k:127:60` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)` |
| `semantics/float.k:128:61` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)` |
| `semantics/float.k:129:62` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)` |
| `semantics/float.k:132:63` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)` |
| `semantics/float.k:133:64` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))` |
| `semantics/float.k:134:65` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)` |
| `semantics/float.k:135:66` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))` |
| `semantics/float.k:136:67` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)` |
| `semantics/float.k:137:68` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))` |
| `semantics/float.k:138:69` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)` |
| `semantics/float.k:139:70` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))` |
| `semantics/float.k:142:71` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]` |
| `semantics/float.k:143:72` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]` |
| `semantics/float.k:144:73` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)` |
| `semantics/float.k:145:74` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))` |
| `semantics/float.k:146:75` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)` |
| `semantics/float.k:147:76` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))` |
| `semantics/float.k:148:77` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)` |
| `semantics/float.k:149:78` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))` |
| `semantics/float.k:150:79` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)` |
| `semantics/float.k:151:80` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))` |
| `semantics/float.k:154:81` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", V:Val, noneV) => V ==K noneV` |
| `semantics/float.k:155:82` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)` |
| `semantics/float.k:160:83` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]` |
| `semantics/float.k:161:84` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]` |
| `semantics/float.k:162:85` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule decStrToF(CS:IntSeq)` |
| `semantics/float.k:165:86` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= headIS(IntSeq) [function]` |
| `semantics/float.k:166:87` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule headIS(iCons(C:Int, _:IntSeq)) => C` |
| `semantics/float.k:167:88` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= intPart(IntSeq) [function, total] \| intPartAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k:168:89` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)` |
| `semantics/float.k:169:90` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intPartAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k:170:91` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A` |
| `semantics/float.k:171:92` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))` |
| `semantics/float.k:173:93` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= fracPart(IntSeq) [function, total] \| fracAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k:174:94` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracPart(.IntSeq) => 0` |
| `semantics/float.k:175:95` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)` |
| `semantics/float.k:176:96` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46` |
| `semantics/float.k:177:97` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k:178:98` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))` |
| `semantics/float.k:179:99` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= fracScale(IntSeq) [function, total] \| fscAcc(IntSeq, Int) [function, total]` |
| `semantics/float.k:180:100` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracScale(.IntSeq) => 1` |
| `semantics/float.k:181:101` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)` |
| `semantics/float.k:182:102` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46` |
| `semantics/float.k:183:103` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fscAcc(.IntSeq, A:Int) => A` |
| `semantics/float.k:184:104` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)` |
| `semantics/float.k:185:105` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)` |
| `semantics/float.k:186:106` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)` |
| `semantics/float.k:187:107` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("float", F:Float, .Vals)        => F` |
| `semantics/float.k:190:108` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]` |
| `semantics/float.k:191:109` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]` |
| `semantics/float.k:192:110` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)` |
| `semantics/float.k:195:111` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]` |
| `semantics/float.k:196:112` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]` |
| `semantics/float.k:197:113` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)` |
| `semantics/float.k:198:114` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))` |
| `semantics/float.k:199:115` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)` |
| `semantics/float.k:200:116` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))` |
| `semantics/float.k:201:117` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)` |
| `semantics/float.k:202:118` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))` |
| `semantics/float.k:203:119` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)` |
| `semantics/float.k:204:120` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))` |
| `semantics/float.k:205:121` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)` |
| `semantics/float.k:206:122` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))` |
| `semantics/float.k:209:123` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]` |
| `semantics/float.k:210:124` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]` |
| `semantics/float.k:211:125` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)` |
| `semantics/float.k:213:126` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)` |
| `semantics/float.k:214:127` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("float", F:Float, .Vals) => F` |
| `semantics/float.k:217:128` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]` |
| `semantics/float.k:218:129` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule roundF(F:Float)` |
| `semantics/float.k:223:130` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]` |
| `semantics/float.k:224:131` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule roundFN(F:Float, N:Int)` |
| `semantics/float.k:227:132` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)` |
| `semantics/float.k:228:133` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)` |
| `semantics/float.k:230:134` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]` |
| `semantics/float.k:231:135` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]` |
| `semantics/float.k:232:136` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= "#mathSqrt"` |
| `semantics/float.k:233:137` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]` |
| `semantics/float.k:234:138` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>` |
| `semantics/float.k:235:139` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>` |
| `semantics/float.k:243:140` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #maxAccF(Iterable, Float) \| #maxContF(Float)` |
| `semantics/float.k:244:141` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `semantics/float.k:245:142` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>` |
| `semantics/float.k:246:143` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>` |
| `semantics/float.k:247:144` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>` |
| `semantics/float.k:250:145` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #minAccF(Iterable, Float) \| #minContF(Float)` |
| `semantics/float.k:251:146` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)` |
| `semantics/float.k:252:147` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>` |
| `semantics/float.k:253:148` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>` |
| `semantics/float.k:254:149` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>` |
| `semantics/float.k:261:150` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #sumAccF(Iterable, Float) \| #sumContF(Float)` |
| `semantics/float.k:262:151` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)` |
| `semantics/float.k:265:152` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>` |
| `semantics/float.k:266:153` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>` |
| `semantics/float.k:267:154` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)` |
| `semantics/float.k:270:155` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)` |
| `semantics/functions.k:8:1` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)` |
| `semantics/functions.k:14:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>` |
| `semantics/functions.k:18:3` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Expr ::= closureExpr(ParamNames, Stmts)` |
| `semantics/functions.k:19:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>` |
| `semantics/functions.k:27:5` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)` |
| `semantics/functions.k:31:6` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)` |
| `semantics/functions.k:33:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),` |
| `semantics/functions.k:36:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,` |
| `semantics/functions.k:42:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,` |
| `semantics/functions.k:47:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Lambda(Params(PNS:ParamNames), E:Expr)` |
| `semantics/functions.k:50:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),` |
| `semantics/functions.k:53:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,` |
| `semantics/functions.k:59:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)` |
| `semantics/functions.k:63:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>` |
| `semantics/functions.k:64:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>` |
| `semantics/functions.k:68:16` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))` |
| `semantics/functions.k:78:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Return(V:Val) ~> _ => #pop </k>` |
| `semantics/functions.k:80:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #endcall => #pop ... </k>` |
| `semantics/functions.k:85:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #pop => V ~> CONT </k>` |
| `semantics/int.k:7:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyUn("-", I:Int) => 0 -Int I` |
| `semantics/int.k:9:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2` |
| `semantics/int.k:11:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi` |
| `semantics/int.k:12:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I` |
| `semantics/int.k:13:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2` |
| `semantics/int.k:14:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2` |
| `semantics/int.k:15:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)` |
| `semantics/int.k:16:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2` |
| `semantics/int.k:17:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0` |
| `semantics/int.k:19:10` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= pyMod(Int, Int) [function]` |
| `semantics/int.k:20:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2` |
| `semantics/int.k:22:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2` |
| `semantics/int.k:23:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2` |
| `semantics/int.k:24:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2` |
| `semantics/int.k:25:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2` |
| `semantics/int.k:26:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2` |
| `semantics/int.k:27:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2` |
| `semantics/iter.k:8:1` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #iterNext(Iterable) \| "#iterDone" \| #iterYield(Val, Iterable)` |
| `semantics/list.k:9:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>` |
| `semantics/list.k:10:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>` |
| `semantics/list.k:13:3` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ApplyK ::= "toList"` |
| `semantics/list.k:14:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>` |
| `semantics/list.k:15:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>` |
| `semantics/list.k:18:6` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]` |
| `semantics/list.k:19:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule valSeqConcat(.ValSeq, T:ValSeq)                => T` |
| `semantics/list.k:20:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))` |
| `semantics/list.k:24:9` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>` |
| `semantics/list.k:27:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B` |
| `semantics/list.k:28:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)` |
| `semantics/list.k:33:12` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= hasRefVS(ValSeq) [function, total]` |
| `semantics/list.k:34:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule hasRefVS(.ValSeq)                => false` |
| `semantics/list.k:35:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)` |
| `semantics/list.k:37:15` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]` |
| `semantics/list.k:39:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true` |
| `semantics/list.k:40:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false` |
| `semantics/list.k:41:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false` |
| `semantics/list.k:42:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)` |
| `semantics/list.k:45:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)` |
| `semantics/list.k:47:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)` |
| `semantics/list.k:49:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)` |
| `semantics/list.k:50:23` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]` |
| `semantics/list.k:53:24` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>` |
| `semantics/list.k:58:25` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #memberAcc(Val, Iterable) \| #memberCont(Val) \| "#notB"` |
| `semantics/list.k:59:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>` |
| `semantics/list.k:60:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>` |
| `semantics/list.k:61:28` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>` |
| `semantics/list.k:62:29` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>` |
| `semantics/list.k:63:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>` |
| `semantics/list.k:65:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>` |
| `semantics/list.k:67:32` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> B:Bool ~> #notB => notBool B ... </k>` |
| `semantics/methods.k:10:1` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= applyMethod(Val, String, Vals) [function]` |
| `semantics/methods.k:13:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)` |
| `semantics/methods.k:14:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)` |
| `semantics/methods.k:15:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)` |
| `semantics/methods.k:16:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)` |
| `semantics/methods.k:19:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))` |
| `semantics/methods.k:20:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))` |
| `semantics/methods.k:21:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))` |
| `semantics/methods.k:26:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))` |
| `semantics/methods.k:27:10` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]` |
| `semantics/methods.k:28:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq` |
| `semantics/methods.k:29:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS` |
| `semantics/methods.k:30:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))` |
| `semantics/methods.k:34:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)` |
| `semantics/methods.k:35:15` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= cntSub(IntSeq, IntSeq) [function]` |
| `semantics/methods.k:36:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cntSub(.IntSeq, _:IntSeq) => 0` |
| `semantics/methods.k:37:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)` |
| `semantics/methods.k:39:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)` |
| `semantics/methods.k:41:19` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]` |
| `semantics/methods.k:42:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0` |
| `semantics/methods.k:43:21` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]` |
| `semantics/methods.k:44:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0` |
| `semantics/methods.k:47:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))` |
| `semantics/methods.k:48:24` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= trimWS(IntSeq) [function, total]` |
| `semantics/methods.k:49:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule trimWS(.IntSeq) => .IntSeq` |
| `semantics/methods.k:50:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)` |
| `semantics/methods.k:51:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)` |
| `semantics/methods.k:52:28` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= revIS(IntSeq) [function, total] \| revISAcc(IntSeq, IntSeq) [function, total]` |
| `semantics/methods.k:53:29` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)` |
| `semantics/methods.k:54:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule revISAcc(.IntSeq, A:IntSeq) => A` |
| `semantics/methods.k:55:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))` |
| `semantics/methods.k:58:32` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)` |
| `semantics/methods.k:61:33` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)` |
| `semantics/methods.k:64:34` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)` |
| `semantics/methods.k:65:35` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]` |
| `semantics/methods.k:66:36` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cntOccVS(.ValSeq, _:Val)                => 0` |
| `semantics/methods.k:67:37` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V` |
| `semantics/methods.k:68:38` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)` |
| `semantics/methods.k:72:39` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)` |
| `semantics/methods.k:75:40` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result` |
| `semantics/methods.k:76:41` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)` |
| `semantics/methods.k:77:42` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))` |
| `semantics/methods.k:79:43` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)` |
| `semantics/methods.k:82:44` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]` |
| `semantics/methods.k:83:45` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule flushTok(ACC:ValSeq, .IntSeq)            => ACC` |
| `semantics/methods.k:84:46` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))` |
| `semantics/methods.k:85:47` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isWSC(Int) [function, total]` |
| `semantics/methods.k:86:48` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13` |
| `semantics/methods.k:89:49` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))` |
| `semantics/methods.k:94:50` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))` |
| `semantics/methods.k:97:51` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token` |
| `semantics/methods.k:98:52` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)` |
| `semantics/methods.k:99:53` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))` |
| `semantics/methods.k:101:54` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))` |
| `semantics/methods.k:104:55` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)` |
| `semantics/methods.k:106:56` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]` |
| `semantics/methods.k:107:57` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq` |
| `semantics/methods.k:108:58` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A` |
| `semantics/methods.k:109:59` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)` |
| `semantics/methods.k:112:60` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isUpperC(Int) [function, total]` |
| `semantics/methods.k:113:61` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90` |
| `semantics/methods.k:115:62` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isLowerC(Int) [function, total]` |
| `semantics/methods.k:116:63` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122` |
| `semantics/methods.k:118:64` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isAlphaC(Int) [function, total]` |
| `semantics/methods.k:119:65` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)` |
| `semantics/methods.k:121:66` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= isDigitC(Int) [function, total]` |
| `semantics/methods.k:122:67` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57` |
| `semantics/methods.k:124:68` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= hasUpper(IntSeq) [function, total]` |
| `semantics/methods.k:125:69` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule hasUpper(.IntSeq) => false` |
| `semantics/methods.k:126:70` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)` |
| `semantics/methods.k:128:71` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= hasLower(IntSeq) [function, total]` |
| `semantics/methods.k:129:72` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule hasLower(.IntSeq) => false` |
| `semantics/methods.k:130:73` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)` |
| `semantics/methods.k:132:74` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= allAlpha(IntSeq) [function, total]` |
| `semantics/methods.k:133:75` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule allAlpha(.IntSeq) => true` |
| `semantics/methods.k:134:76` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)` |
| `semantics/methods.k:136:77` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= allDigit(IntSeq) [function, total]` |
| `semantics/methods.k:137:78` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule allDigit(.IntSeq) => true` |
| `semantics/methods.k:138:79` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)` |
| `semantics/methods.k:140:80` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= lowerC(Int) [function, total]` |
| `semantics/methods.k:142:81` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `semantics/methods.k:143:82` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule lowerC(C:Int) => C         [owise]` |
| `semantics/methods.k:145:83` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= upperC(Int) [function, total]` |
| `semantics/methods.k:146:84` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `semantics/methods.k:147:85` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule upperC(C:Int) => C         [owise]` |
| `semantics/methods.k:149:86` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= swapC(Int) [function, total]` |
| `semantics/methods.k:150:87` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)` |
| `semantics/methods.k:151:88` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)` |
| `semantics/methods.k:152:89` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule swapC(C:Int) => C         [owise]` |
| `semantics/methods.k:154:90` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= mapLower(IntSeq) [function, total]` |
| `semantics/methods.k:155:91` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapLower(.IntSeq) => .IntSeq` |
| `semantics/methods.k:156:92` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))` |
| `semantics/methods.k:158:93` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= mapUpper(IntSeq) [function, total]` |
| `semantics/methods.k:159:94` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapUpper(.IntSeq) => .IntSeq` |
| `semantics/methods.k:160:95` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))` |
| `semantics/methods.k:162:96` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= mapSwap(IntSeq) [function, total]` |
| `semantics/methods.k:163:97` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapSwap(.IntSeq) => .IntSeq` |
| `semantics/methods.k:164:98` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))` |
| `semantics/methods.k:166:99` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]` |
| `semantics/methods.k:167:100` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule startsWith(.IntSeq, _:IntSeq)               => true` |
| `semantics/methods.k:168:101` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/methods.k:169:102` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)` |
| `semantics/operators.k:10:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>` |
| `semantics/operators.k:12:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>` |
| `semantics/operators.k:15:3` | `context` / `context-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `context Compare(HOLE, _)` |
| `semantics/operators.k:16:4` | `context` / `context-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `context Compare(_:Val, CmpOp(_, HOLE))` |
| `semantics/operators.k:17:5` | `rule` / `ordinary-semantic-rule` | owise | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]` |
| `semantics/operators.k:19:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("is",     V:Val, noneV) => V ==K noneV` |
| `semantics/operators.k:20:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)` |
| `semantics/operators.k:25:8` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>` |
| `semantics/operators.k:28:9` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>` |
| `semantics/operators.k:34:10` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>` |
| `semantics/operators.k:38:11` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>` |
| `semantics/operators.k:44:12` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>` |
| `semantics/range.k:9:1` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= inRange(Int, Int, Int) [function, total]` |
| `semantics/range.k:10:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)` |
| `semantics/range.k:12:3` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= rangeLen(Int, Int, Int) [function]` |
| `semantics/range.k:13:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST` |
| `semantics/range.k:15:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)` |
| `semantics/range.k:17:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0` |
| `semantics/range.k:20:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))` |
| `semantics/range.k:23:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>` |
| `semantics/set.k:8:1` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= setV(IntSeq)` |
| `semantics/set.k:11:2` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= codeIn(Int, IntSeq) [function, total]` |
| `semantics/set.k:12:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule codeIn(_:Int, .IntSeq)                => false` |
| `semantics/set.k:13:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)` |
| `semantics/set.k:16:5` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]` |
| `semantics/set.k:18:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)` |
| `semantics/set.k:19:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC` |
| `semantics/set.k:20:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)` |
| `semantics/set.k:22:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))` |
| `semantics/set.k:25:10` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]` |
| `semantics/set.k:26:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)` |
| `semantics/set.k:27:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))` |
| `semantics/set.k:31:13` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k:32:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule subsetCodes(.IntSeq, _:IntSeq)                => true` |
| `semantics/set.k:33:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)` |
| `semantics/set.k:35:16` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]` |
| `semantics/set.k:36:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)` |
| `semantics/set.k:39:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)` |
| `semantics/sort.k:18:1` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]` |
| `semantics/sort.k:19:2` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= insVS(Int, ValSeq) [function]` |
| `semantics/sort.k:20:3` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule sortVS(.ValSeq)                => .ValSeq          [concrete]` |
| `semantics/sort.k:21:4` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]` |
| `semantics/sort.k:22:5` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]` |
| `semantics/sort.k:23:6` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]` |
| `semantics/sort.k:24:7` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]` |
| `semantics/sort.k:26:8` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]` |
| `semantics/sort.k:27:9` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]` |
| `semantics/sort.k:28:10` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]` |
| `semantics/sort.k:29:11` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))` |
| `semantics/sort.k:31:12` | `rule` / `concrete-semantic-rule` | concrete | `ACCEPTED_SELECTED_SEMANTICS` | `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))` |
| `semantics/sort.k:36:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))` |
| `semantics/sort.k:40:14` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>` |
| `semantics/sort.k:49:15` | `syntax` / `syntax-declaration` | function, total, symbol, no-evaluators | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]` |
| `semantics/sort.k:51:16` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= revVS(ValSeq) [function, total]` |
| `semantics/sort.k:53:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)` |
| `semantics/sort.k:54:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule revVSAcc(.ValSeq, A:ValSeq) => A` |
| `semantics/sort.k:55:19` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))` |
| `semantics/sort.k:57:20` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]` |
| `semantics/sort.k:58:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule condRev(S:ValSeq, false) => S` |
| `semantics/sort.k:59:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule condRev(S:ValSeq, true)  => revVS(S)` |
| `semantics/sort.k:61:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))` |
| `semantics/sort.k:63:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))` |
| `semantics/sort.k:65:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))` |
| `semantics/str.k:8:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>` |
| `semantics/str.k:9:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))` |
| `semantics/str.k:13:3` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= strToCodes(String) [function]` |
| `semantics/str.k:14:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>` |
| `semantics/str.k:15:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strToCodes("") => .IntSeq` |
| `semantics/str.k:16:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))` |
| `semantics/str.k:20:7` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:21:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqConcat(.IntSeq, T:IntSeq)                => T` |
| `semantics/str.k:22:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))` |
| `semantics/str.k:24:10` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))` |
| `semantics/str.k:25:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B` |
| `semantics/str.k:26:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)` |
| `semantics/str.k:29:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)` |
| `semantics/str.k:30:14` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)` |
| `semantics/str.k:32:15` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:33:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strPrefix(.IntSeq, _:IntSeq)               => true` |
| `semantics/str.k:34:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/str.k:35:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)` |
| `semantics/str.k:37:19` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:38:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)` |
| `semantics/str.k:39:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)` |
| `semantics/str.k:40:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)` |
| `semantics/str.k:48:23` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]` |
| `semantics/str.k:49:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strLt(.IntSeq, .IntSeq)                => false` |
| `semantics/str.k:50:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true` |
| `semantics/str.k:51:26` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false` |
| `semantics/str.k:52:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B` |
| `semantics/str.k:53:28` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B` |
| `semantics/str.k:54:29` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B` |
| `semantics/str.k:56:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)` |
| `semantics/str.k:57:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)` |
| `semantics/str.k:58:32` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)` |
| `semantics/str.k:59:33` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)` |
| `semantics/subscript.k:11:1` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]` |
| `semantics/subscript.k:12:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V` |
| `semantics/subscript.k:13:3` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)` |
| `semantics/subscript.k:16:4` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= intSeqAt(IntSeq, Int) [function]` |
| `semantics/subscript.k:17:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C` |
| `semantics/subscript.k:18:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)` |
| `semantics/subscript.k:21:7` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= normIdx(Int, Int) [function, total]` |
| `semantics/subscript.k:22:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0` |
| `semantics/subscript.k:23:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0` |
| `semantics/subscript.k:27:10` | `context` / `context-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `context Subscript(HOLE, _)` |
| `semantics/subscript.k:28:11` | `context` / `context-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `context Subscript(_:Val, HOLE:Expr)` |
| `semantics/subscript.k:31:12` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>` |
| `semantics/subscript.k:35:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>` |
| `semantics/subscript.k:37:14` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= applyIndex(Val, Int) [function]` |
| `semantics/subscript.k:38:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `semantics/subscript.k:39:16` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))` |
| `semantics/subscript.k:40:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyIndex(str(IS:IntSeq),   I:Int)` |
| `semantics/subscript.k:44:18` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #evalB(Bound) \| "#toSome"` |
| `semantics/subscript.k:49:19` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax OptInt ::= "noB" \| someB(Int)` |
| `semantics/subscript.k:50:20` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #evalB(NoBound)  => noB ... </k>` |
| `semantics/subscript.k:51:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>` |
| `semantics/subscript.k:52:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> I:Int ~> #toSome => someB(I) ... </k>` |
| `semantics/subscript.k:54:23` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>` |
| `semantics/subscript.k:55:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>` |
| `semantics/subscript.k:56:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>` |
| `semantics/subscript.k:58:26` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)` |
| `semantics/subscript.k:61:27` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>` |
| `semantics/subscript.k:63:28` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]` |
| `semantics/subscript.k:64:29` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| `semantics/subscript.k:66:30` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| `semantics/subscript.k:68:31` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)` |
| `semantics/subscript.k:72:32` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= slStep(OptInt) [function, total]` |
| `semantics/subscript.k:73:33` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStep(noB)          => 1` |
| `semantics/subscript.k:74:34` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStep(someB(S:Int)) => S` |
| `semantics/subscript.k:76:35` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= slStart(OptInt, OptInt, Int) [function]` |
| `semantics/subscript.k:77:36` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStart(noB,          ST:OptInt, _LEN:Int) => 0` |
| `semantics/subscript.k:79:37` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1` |
| `semantics/subscript.k:81:38` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| `semantics/subscript.k:83:39` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= slStop(OptInt, OptInt, Int) [function]` |
| `semantics/subscript.k:84:40` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN` |
| `semantics/subscript.k:86:41` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStop(noB,          ST:OptInt, _LEN:Int) => -1` |
| `semantics/subscript.k:88:42` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))` |
| `semantics/subscript.k:90:43` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= slAdjust(Int, Int, Int) [function, total]` |
| `semantics/subscript.k:91:44` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)` |
| `semantics/subscript.k:93:45` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)` |
| `semantics/subscript.k:96:46` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= clampLo(Int, Int) [function, total]` |
| `semantics/subscript.k:97:47` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule clampLo(J:Int, _STEP:Int) => J` |
| `semantics/subscript.k:99:48` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi` |
| `semantics/subscript.k:102:49` | `syntax` / `syntax-declaration` | function, total | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= clampHi(Int, Int, Int) [function, total]` |
| `semantics/subscript.k:103:50` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I` |
| `semantics/subscript.k:105:51` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi` |
| `semantics/subscript.k:109:52` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]` |
| `semantics/subscript.k:110:53` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)` |
| `semantics/subscript.k:113:54` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq` |
| `semantics/subscript.k:116:55` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]` |
| `semantics/subscript.k:117:56` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)` |
| `semantics/subscript.k:120:57` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq` |
| `semantics/syntax.k:9:1` | `syntax` / `syntax-declaration` | macro, strict, seqstrict | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Expr ::= "Int"      "(" Int ")"` |
| `semantics/syntax.k:32:2` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"` |
| `semantics/syntax.k:33:3` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Entry    ::= "Entry" "(" Expr "," Expr ")"` |
| `semantics/syntax.k:34:4` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Entries  ::= List{Entry, ","}` |
| `semantics/syntax.k:35:5` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"` |
| `semantics/syntax.k:36:6` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax CompFors ::= List{CompFor, ""}` |
| `semantics/syntax.k:37:7` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Exprs    ::= List{Expr, ","}` |
| `semantics/syntax.k:38:8` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Index    ::= Expr \| "Slice" "(" Bound "," Bound "," Bound ")"` |
| `semantics/syntax.k:39:9` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Bound    ::= Expr \| "NoBound"` |
| `semantics/syntax.k:41:10` | `syntax` / `syntax-declaration` | strict | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]` |
| `semantics/syntax.k:56:11` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Stmts      ::= List{Stmt, ""}` |
| `semantics/syntax.k:57:12` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Params     ::= "Params" "(" ParamNames ")"` |
| `semantics/syntax.k:58:13` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax CellVars   ::= "CellVars" "(" ParamNames ")"` |
| `semantics/syntax.k:59:14` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"` |
| `semantics/syntax.k:60:15` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ParamNames ::= List{String, ","}` |
| `semantics/syntax.k:61:16` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Module     ::= "Module" "(" Stmts ")"` |
| `semantics/tuple.k:10:1` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>` |
| `semantics/tuple.k:11:2` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>` |
| `semantics/tuple.k:14:3` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax ApplyK ::= "toTuple"` |
| `semantics/tuple.k:15:4` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>` |
| `semantics/tuple.k:16:5` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>` |
| `semantics/tuple.k:18:6` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B` |
| `semantics/tuple.k:20:7` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>` |
| `semantics/tuple.k:21:8` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>` |
| `semantics/tuple.k:23:9` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)` |
| `semantics/tuple.k:24:10` | `syntax` / `syntax-declaration` | function | `ACCEPTED_SELECTED_SEMANTICS` | `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]` |
| `semantics/tuple.k:25:11` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V` |
| `semantics/tuple.k:26:12` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)` |
| `semantics/tuple.k:28:13` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)` |
| `semantics/tuple.k:31:14` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #bindTgt(Expr, Val)` |
| `semantics/tuple.k:32:15` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>` |
| `semantics/tuple.k:35:16` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>` |
| `semantics/tuple.k:42:17` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:43:18` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:44:19` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>` |
| `semantics/tuple.k:49:20` | `syntax` / `syntax-declaration` | — | `ACCEPTED_SELECTED_SEMANTICS` | `syntax KItem ::= #unpackSeq(Exprs, ValSeq)` |
| `semantics/tuple.k:50:21` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:51:22` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>` |
| `semantics/tuple.k:52:23` | `rule` / `ordinary-semantic-rule` | priority | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>` |
| `semantics/tuple.k:55:24` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))` |
| `semantics/tuple.k:57:25` | `rule` / `ordinary-semantic-rule` | — | `ACCEPTED_SELECTED_SEMANTICS` | `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>` |
| `verification.k:8:1` | `syntax` / `syntax-declaration` | macro | `SOUND_PROGRAM_ALIAS_DECLARATION` | `syntax Stmts ::= "maximumBody" [macro]` |
| `verification.k:9:2` | `rule` / `macro-expansion-rule` | — | `SOUND_PROGRAM_ALIAS_EXPANSION` | `rule maximumBody` |
| `verification.k:22:3` | `rule` / `simplification-rule` | simplification | `SOUND_CONDITIONAL_ON_SORT_PRIMITIVE_CONTRACT` | `rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]` |
