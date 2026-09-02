# Exhaustive K source declaration/rule inventory

The inventory is generated from the trusted scratch copy plus the candidate proof sources. Every declaration-start block is reproduced with source lines; file hashes and counts make omissions detectable.

Global declaration kinds: `claim`=3, `configuration`=1, `context`=5, `endmodule`=28, `imports`=90, `module`=28, `requires`=25, `rule`=717, `syntax`=230
Global source attributes: `concrete`=35, `function`=163, `macro`=4, `macro-rec`=1, `no-evaluators`=22, `owise`=26, `priority`=47, `seqstrict`=1, `simplification`=15, `strict`=10, `symbol`=25, `total`=123
## `reference-semantics/semantics/assert.k`

- SHA-256: `4258987a261d24b02ab3abfa52b3b2e013ea6323f9d5eb9a59c8f42cbcba030b`; source lines: 16; declaration blocks: 6
- Kinds: `endmodule`=1, `imports`=1, `module`=1, `rule`=3

### module `reference-semantics/semantics/assert.k:3-3` (attributes: none)

```k
0003: module MPY-ASSERT
```

### imports `reference-semantics/semantics/assert.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### rule `reference-semantics/semantics/assert.k:6-7` (attributes: none)

```k
0006:   rule <k> Assert(V:Val) => .K ... </k>
0007:        requires truthy(V)
```

### rule `reference-semantics/semantics/assert.k:8-11` (attributes: none)

```k
0008:   rule <k> Assert(V:Val) ~> _ => .K </k>
0009:        <exc> NoExc => AssertionError </exc>
0010:        <exit-code> _ => 1 </exit-code>
0011:        requires notBool truthy(V)
```

### rule `reference-semantics/semantics/assert.k:13-15` (attributes: priority)

```k
0013:   rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
0014:        <heap> ... H |-> V:Val ... </heap>
0015:        [priority(40)]
```

### endmodule `reference-semantics/semantics/assert.k:16-16` (attributes: none)

```k
0016: endmodule
```

## `reference-semantics/semantics/bool.k`

- SHA-256: `8d6cfa9cd1ed776e51d776e4d358c418960c57715a6f9654ef9af41aea29f4fd`; source lines: 47; declaration blocks: 17
- Kinds: `context`=1, `endmodule`=1, `imports`=1, `module`=1, `rule`=13

### module `reference-semantics/semantics/bool.k:5-5` (attributes: none)

```k
0005: module MPY-BOOL
```

### imports `reference-semantics/semantics/bool.k:6-6` (attributes: none)

```k
0006:   imports MPY-CORE
```

### rule `reference-semantics/semantics/bool.k:8-8` (attributes: none)

```k
0008:   rule applyUn("not", V:Val) => notBool truthy(V)
```

### rule `reference-semantics/semantics/bool.k:10-10` (attributes: none)

```k
0010:   rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

### rule `reference-semantics/semantics/bool.k:11-11` (attributes: none)

```k
0011:   rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

### context `reference-semantics/semantics/bool.k:16-16` (attributes: none)

```k
0016:   context BoolOp(_, (HOLE:Expr, _:Exprs))
```

### rule `reference-semantics/semantics/bool.k:17-17` (attributes: none)

```k
0017:   rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

### rule `reference-semantics/semantics/bool.k:18-19` (attributes: none)

```k
0018:   rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
0019:        requires truthy(V)
```

### rule `reference-semantics/semantics/bool.k:20-21` (attributes: none)

```k
0020:   rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
0021:        requires notBool truthy(V)
```

### rule `reference-semantics/semantics/bool.k:22-23` (attributes: none)

```k
0022:   rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
0023:        requires truthy(V)
```

### rule `reference-semantics/semantics/bool.k:24-25` (attributes: none)

```k
0024:   rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
0025:        requires notBool truthy(V)
```

### rule `reference-semantics/semantics/bool.k:29-30` (attributes: priority)

```k
0029:   rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
0030:        [priority(40)]
```

### rule `reference-semantics/semantics/bool.k:31-34` (attributes: priority)

```k
0031:   rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
0032:        <heap> ... H |-> V:Val ... </heap>
0033:        requires truthy(V)
0034:        [priority(40)]
```

### rule `reference-semantics/semantics/bool.k:35-38` (attributes: priority)

```k
0035:   rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
0036:        <heap> ... H |-> V:Val ... </heap>
0037:        requires notBool truthy(V)
0038:        [priority(40)]
```

### rule `reference-semantics/semantics/bool.k:39-42` (attributes: priority)

```k
0039:   rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
0040:        <heap> ... H |-> V:Val ... </heap>
0041:        requires truthy(V)
0042:        [priority(40)]
```

### rule `reference-semantics/semantics/bool.k:43-46` (attributes: priority)

```k
0043:   rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
0044:        <heap> ... H |-> V:Val ... </heap>
0045:        requires notBool truthy(V)
0046:        [priority(40)]
```

### endmodule `reference-semantics/semantics/bool.k:47-47` (attributes: none)

```k
0047: endmodule
```

## `reference-semantics/semantics/builtins.k`

- SHA-256: `fa43a855b8a4548f305f3dd210c8f6c6e7aa15b8d1cb0b8296977f061310c2dd`; source lines: 298; declaration blocks: 184
- Kinds: `endmodule`=1, `imports`=7, `module`=1, `rule`=137, `syntax`=38

### module `reference-semantics/semantics/builtins.k:3-3` (attributes: none)

```k
0003: module MPY-BUILTINS
```

### imports `reference-semantics/semantics/builtins.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/builtins.k:5-5` (attributes: none)

```k
0005:   imports MPY-STR
```

### imports `reference-semantics/semantics/builtins.k:6-6` (attributes: none)

```k
0006:   imports MPY-SET
```

### imports `reference-semantics/semantics/builtins.k:7-7` (attributes: none)

```k
0007:   imports MPY-ITER
```

### imports `reference-semantics/semantics/builtins.k:8-8` (attributes: none)

```k
0008:   imports MPY-RANGE
```

### imports `reference-semantics/semantics/builtins.k:9-9` (attributes: none)

```k
0009:   imports MPY-INT
```

### imports `reference-semantics/semantics/builtins.k:10-10` (attributes: none)

```k
0010:   imports MPY-METHODS
```

### syntax `reference-semantics/semantics/builtins.k:17-17` (attributes: function)

```k
0017:   syntax Val ::= applyBuiltin(String, Vals) [function]
```

### syntax `reference-semantics/semantics/builtins.k:20-20` (attributes: function)

```k
0020:   syntax Int ::= seqLen(Val) [function]
```

### rule `reference-semantics/semantics/builtins.k:21-21` (attributes: none)

```k
0021:   rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

### rule `reference-semantics/semantics/builtins.k:22-22` (attributes: none)

```k
0022:   rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

### rule `reference-semantics/semantics/builtins.k:23-23` (attributes: none)

```k
0023:   rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

### rule `reference-semantics/semantics/builtins.k:24-24` (attributes: none)

```k
0024:   rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

### rule `reference-semantics/semantics/builtins.k:25-25` (attributes: none)

```k
0025:   rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

### rule `reference-semantics/semantics/builtins.k:26-26` (attributes: none)

```k
0026:   rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

### rule `reference-semantics/semantics/builtins.k:32-32` (attributes: none)

```k
0032:   rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:33-33` (attributes: none)

```k
0033:   rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:34-34` (attributes: none)

```k
0034:   rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:35-35` (attributes: none)

```k
0035:   rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

### syntax `reference-semantics/semantics/builtins.k:36-36` (attributes: function, total)

```k
0036:   syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:37-37` (attributes: none)

```k
0037:   rule charsOf(.IntSeq)                => .ValSeq
```

### rule `reference-semantics/semantics/builtins.k:38-38` (attributes: none)

```k
0038:   rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

### rule `reference-semantics/semantics/builtins.k:41-41` (attributes: none)

```k
0041:   rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

### rule `reference-semantics/semantics/builtins.k:44-44` (attributes: none)

```k
0044:   rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

### syntax `reference-semantics/semantics/builtins.k:47-47` (attributes: none)

```k
0047:   syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

### rule `reference-semantics/semantics/builtins.k:48-48` (attributes: none)

```k
0048:   rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:49-49` (attributes: none)

```k
0049:   rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

### rule `reference-semantics/semantics/builtins.k:50-52` (attributes: none)

```k
0050:   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
0051:         => #sumAcc(R, ACC +Int intOf(V)) ... </k>
0052:        requires isInt(V) orBool isBool(V)
```

### syntax `reference-semantics/semantics/builtins.k:54-54` (attributes: function)

```k
0054:   syntax Int ::= intOf(Val) [function]
```

### rule `reference-semantics/semantics/builtins.k:55-55` (attributes: none)

```k
0055:   rule intOf(I:Int)  => I
```

### rule `reference-semantics/semantics/builtins.k:56-56` (attributes: none)

```k
0056:   rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

### syntax `reference-semantics/semantics/builtins.k:59-59` (attributes: none)

```k
0059:   syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

### rule `reference-semantics/semantics/builtins.k:60-60` (attributes: none)

```k
0060:   rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

### rule `reference-semantics/semantics/builtins.k:61-61` (attributes: none)

```k
0061:   rule <k> #iterDone ~> #allCont => true ... </k>
```

### rule `reference-semantics/semantics/builtins.k:62-63` (attributes: none)

```k
0062:   rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
0063:        requires truthy(V)
```

### rule `reference-semantics/semantics/builtins.k:64-65` (attributes: none)

```k
0064:   rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
0065:        requires notBool truthy(V)
```

### syntax `reference-semantics/semantics/builtins.k:67-67` (attributes: none)

```k
0067:   syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

### rule `reference-semantics/semantics/builtins.k:68-68` (attributes: none)

```k
0068:   rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

### rule `reference-semantics/semantics/builtins.k:69-69` (attributes: none)

```k
0069:   rule <k> #iterDone ~> #anyCont => false ... </k>
```

### rule `reference-semantics/semantics/builtins.k:70-71` (attributes: none)

```k
0070:   rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
0071:        requires truthy(V)
```

### rule `reference-semantics/semantics/builtins.k:72-73` (attributes: none)

```k
0072:   rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
0073:        requires notBool truthy(V)
```

### syntax `reference-semantics/semantics/builtins.k:76-76` (attributes: none)

```k
0076:   syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

### rule `reference-semantics/semantics/builtins.k:77-77` (attributes: none)

```k
0077:   rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

### rule `reference-semantics/semantics/builtins.k:78-79` (attributes: none)

```k
0078:   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
0079:        requires isInt(V)
```

### rule `reference-semantics/semantics/builtins.k:80-80` (attributes: none)

```k
0080:   rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:81-81` (attributes: none)

```k
0081:   rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

### rule `reference-semantics/semantics/builtins.k:82-84` (attributes: none)

```k
0082:   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
0083:         => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
0084:        requires isInt(V)
```

### syntax `reference-semantics/semantics/builtins.k:86-86` (attributes: none)

```k
0086:   syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

### rule `reference-semantics/semantics/builtins.k:87-87` (attributes: none)

```k
0087:   rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

### rule `reference-semantics/semantics/builtins.k:88-89` (attributes: none)

```k
0088:   rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
0089:        requires isInt(V)
```

### rule `reference-semantics/semantics/builtins.k:90-90` (attributes: none)

```k
0090:   rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:91-91` (attributes: none)

```k
0091:   rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

### rule `reference-semantics/semantics/builtins.k:92-94` (attributes: none)

```k
0092:   rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
0093:         => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
0094:        requires isInt(V)
```

### syntax `reference-semantics/semantics/builtins.k:97-97` (attributes: function)

```k
0097:   syntax Int ::= maxVals(Int, Vals) [function]
```

### rule `reference-semantics/semantics/builtins.k:98-98` (attributes: none)

```k
0098:   rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

### rule `reference-semantics/semantics/builtins.k:99-99` (attributes: none)

```k
0099:   rule maxVals(M:Int, .Vals)           => M
```

### rule `reference-semantics/semantics/builtins.k:100-100` (attributes: none)

```k
0100:   rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

### syntax `reference-semantics/semantics/builtins.k:102-102` (attributes: function)

```k
0102:   syntax Int ::= minVals(Int, Vals) [function]
```

### rule `reference-semantics/semantics/builtins.k:103-103` (attributes: none)

```k
0103:   rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

### rule `reference-semantics/semantics/builtins.k:104-104` (attributes: none)

```k
0104:   rule minVals(M:Int, .Vals)           => M
```

### rule `reference-semantics/semantics/builtins.k:105-105` (attributes: none)

```k
0105:   rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

### rule `reference-semantics/semantics/builtins.k:108-109` (attributes: none)

```k
0108:   rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
0109:        requires N >=Int 0
```

### rule `reference-semantics/semantics/builtins.k:111-113` (attributes: none)

```k
0111:   rule applyBuiltin("bin", N:Int, .Vals)
0112:     => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
0113:        requires N <Int 0
```

### syntax `reference-semantics/semantics/builtins.k:114-114` (attributes: function, total)

```k
0114:   syntax IntSeq ::= binCodes(Int) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:115-115` (attributes: none)

```k
0115:   rule binCodes(0) => iCons(48, .IntSeq)
```

### rule `reference-semantics/semantics/builtins.k:116-116` (attributes: none)

```k
0116:   rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

### syntax `reference-semantics/semantics/builtins.k:117-117` (attributes: function, total)

```k
0117:   syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:118-118` (attributes: none)

```k
0118:   rule binAcc(0, ACC:IntSeq) => ACC
```

### rule `reference-semantics/semantics/builtins.k:119-121` (attributes: none)

```k
0119:   rule binAcc(N:Int, ACC:IntSeq)
0120:     => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
0121:        requires N >Int 0
```

### rule `reference-semantics/semantics/builtins.k:124-125` (attributes: none)

```k
0124:   rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
0125:         => #alloc(list(enumVS(VS, 0))) ... </k>
```

### syntax `reference-semantics/semantics/builtins.k:126-126` (attributes: function, total)

```k
0126:   syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:127-127` (attributes: none)

```k
0127:   rule enumVS(.ValSeq, _:Int) => .ValSeq
```

### rule `reference-semantics/semantics/builtins.k:128-129` (attributes: none)

```k
0128:   rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
0129:     => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

### rule `reference-semantics/semantics/builtins.k:132-133` (attributes: none)

```k
0132:   rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
0133:         => #alloc(list(mapStrVS(VS))) ... </k>
```

### syntax `reference-semantics/semantics/builtins.k:134-134` (attributes: function, total)

```k
0134:   syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:135-135` (attributes: none)

```k
0135:   rule mapStrVS(.ValSeq) => .ValSeq
```

### rule `reference-semantics/semantics/builtins.k:136-136` (attributes: none)

```k
0136:   rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

### rule `reference-semantics/semantics/builtins.k:137-137` (attributes: none)

```k
0137:   rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

### rule `reference-semantics/semantics/builtins.k:140-140` (attributes: none)

```k
0140:   rule applyBuiltin("int", I:Int, .Vals) => I
```

### rule `reference-semantics/semantics/builtins.k:143-143` (attributes: none)

```k
0143:   rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

### rule `reference-semantics/semantics/builtins.k:144-145` (attributes: none)

```k
0144:   rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
0145:        requires 0 <=Int I andBool I <Int 128
```

### rule `reference-semantics/semantics/builtins.k:148-148` (attributes: none)

```k
0148:   rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

### rule `reference-semantics/semantics/builtins.k:149-149` (attributes: none)

```k
0149:   rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

### rule `reference-semantics/semantics/builtins.k:152-153` (attributes: none)

```k
0152:   rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
0153:        requires 48 <=Int C andBool C <=Int 57
```

### rule `reference-semantics/semantics/builtins.k:156-157` (attributes: none)

```k
0156:   rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
0157:        requires isLen(CS) >=Int 2
```

### syntax `reference-semantics/semantics/builtins.k:158-158` (attributes: function, total)

```k
0158:   syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:159-159` (attributes: none)

```k
0159:   rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

### rule `reference-semantics/semantics/builtins.k:160-160` (attributes: none)

```k
0160:   rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

### rule `reference-semantics/semantics/builtins.k:163-163` (attributes: none)

```k
0163:   rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

### rule `reference-semantics/semantics/builtins.k:164-164` (attributes: none)

```k
0164:   rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

### rule `reference-semantics/semantics/builtins.k:167-168` (attributes: none)

```k
0167:   rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
0168:         => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:169-169` (attributes: none)

```k
0169:   rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

### rule `reference-semantics/semantics/builtins.k:170-170` (attributes: none)

```k
0170:   rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

### rule `reference-semantics/semantics/builtins.k:171-172` (attributes: none)

```k
0171:   rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
0172:         => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

### rule `reference-semantics/semantics/builtins.k:173-173` (attributes: none)

```k
0173:   rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

### rule `reference-semantics/semantics/builtins.k:174-174` (attributes: none)

```k
0174:   rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

### rule `reference-semantics/semantics/builtins.k:177-177` (attributes: none)

```k
0177:   rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

### rule `reference-semantics/semantics/builtins.k:178-178` (attributes: none)

```k
0178:   rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

### rule `reference-semantics/semantics/builtins.k:179-180` (attributes: none)

```k
0179:   rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
0180:        requires S =/=Int 0
```

### rule `reference-semantics/semantics/builtins.k:187-187` (attributes: none)

```k
0187:   rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

### syntax `reference-semantics/semantics/builtins.k:188-188` (attributes: function)

```k
0188:   syntax Int ::= evalArith(IntSeq) [function]
```

### rule `reference-semantics/semantics/builtins.k:189-190` (attributes: none)

```k
0189:   rule evalArith(CS:IntSeq)
0190:     => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

### syntax `reference-semantics/semantics/builtins.k:192-192` (attributes: none)

```k
0192:   syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

### syntax `reference-semantics/semantics/builtins.k:194-194` (attributes: function, total)

```k
0194:   syntax Bool ::= evDigit(Int) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:195-195` (attributes: none)

```k
0195:   rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax `reference-semantics/semantics/builtins.k:196-196` (attributes: function, total)

```k
0196:   syntax Bool ::= evHead42(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:197-197` (attributes: none)

```k
0197:   rule evHead42(iCons(42, _:IntSeq)) => true
```

### rule `reference-semantics/semantics/builtins.k:198-198` (attributes: owise)

```k
0198:   rule evHead42(_:IntSeq)            => false [owise]
```

### syntax `reference-semantics/semantics/builtins.k:199-199` (attributes: function, total)

```k
0199:   syntax Bool ::= evHead47(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:200-200` (attributes: none)

```k
0200:   rule evHead47(iCons(47, _:IntSeq)) => true
```

### rule `reference-semantics/semantics/builtins.k:201-201` (attributes: owise)

```k
0201:   rule evHead47(_:IntSeq)            => false [owise]
```

### syntax `reference-semantics/semantics/builtins.k:203-203` (attributes: function, total)

```k
0203:   syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:204-204` (attributes: none)

```k
0204:   rule tokOps(.IntSeq)                 => .OpSeq
```

### rule `reference-semantics/semantics/builtins.k:205-205` (attributes: none)

```k
0205:   rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

### rule `reference-semantics/semantics/builtins.k:206-206` (attributes: none)

```k
0206:   rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

### rule `reference-semantics/semantics/builtins.k:207-207` (attributes: none)

```k
0207:   rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

### rule `reference-semantics/semantics/builtins.k:208-208` (attributes: none)

```k
0208:   rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

### rule `reference-semantics/semantics/builtins.k:209-209` (attributes: none)

```k
0209:   rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

### rule `reference-semantics/semantics/builtins.k:210-210` (attributes: none)

```k
0210:   rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

### rule `reference-semantics/semantics/builtins.k:211-211` (attributes: none)

```k
0211:   rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

### rule `reference-semantics/semantics/builtins.k:212-212` (attributes: none)

```k
0212:   rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

### syntax `reference-semantics/semantics/builtins.k:214-215` (attributes: function, total, function, total)

```k
0214:   syntax IntSeq ::= tokNds(IntSeq) [function, total]
0215:                   | tokNdAcc(Int, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:216-216` (attributes: none)

```k
0216:   rule tokNds(.IntSeq)                => .IntSeq
```

### rule `reference-semantics/semantics/builtins.k:217-217` (attributes: none)

```k
0217:   rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

### rule `reference-semantics/semantics/builtins.k:218-218` (attributes: none)

```k
0218:   rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

### rule `reference-semantics/semantics/builtins.k:219-220` (attributes: none)

```k
0219:   rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
0220:        requires notBool evDigit(C) andBool C =/=Int 32
```

### rule `reference-semantics/semantics/builtins.k:221-222` (attributes: none)

```k
0221:   rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
0222:        requires evDigit(C)
```

### rule `reference-semantics/semantics/builtins.k:223-223` (attributes: owise)

```k
0223:   rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

### syntax `reference-semantics/semantics/builtins.k:225-225` (attributes: none)

```k
0225:   syntax EvPair ::= evp(OpSeq, IntSeq)
```

### syntax `reference-semantics/semantics/builtins.k:226-226` (attributes: function, total)

```k
0226:   syntax Int ::= firstNdE(EvPair) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:227-227` (attributes: none)

```k
0227:   rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

### rule `reference-semantics/semantics/builtins.k:228-228` (attributes: owise)

```k
0228:   rule firstNdE(_:EvPair) => 0 [owise]
```

### syntax `reference-semantics/semantics/builtins.k:230-230` (attributes: function, total)

```k
0230:   syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:231-231` (attributes: none)

```k
0231:   rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

### rule `reference-semantics/semantics/builtins.k:232-232` (attributes: none)

```k
0232:   rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

### rule `reference-semantics/semantics/builtins.k:233-233` (attributes: none)

```k
0233:   rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

### rule `reference-semantics/semantics/builtins.k:234-234` (attributes: none)

```k
0234:   rule applyOpE("//", A:Int, B:Int) => A divInt B
```

### rule `reference-semantics/semantics/builtins.k:235-235` (attributes: none)

```k
0235:   rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

### rule `reference-semantics/semantics/builtins.k:236-236` (attributes: owise)

```k
0236:   rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

### syntax `reference-semantics/semantics/builtins.k:238-238` (attributes: function, total)

```k
0238:   syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:239-239` (attributes: none)

```k
0239:   rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

### rule `reference-semantics/semantics/builtins.k:240-240` (attributes: none)

```k
0240:   rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

### rule `reference-semantics/semantics/builtins.k:241-242` (attributes: none)

```k
0241:   rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
0242:        requires O =/=String "**"
```

### rule `reference-semantics/semantics/builtins.k:243-243` (attributes: owise)

```k
0243:   rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

### syntax `reference-semantics/semantics/builtins.k:244-244` (attributes: function, total)

```k
0244:   syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:245-245` (attributes: none)

```k
0245:   rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

### rule `reference-semantics/semantics/builtins.k:246-246` (attributes: none)

```k
0246:   rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

### syntax `reference-semantics/semantics/builtins.k:247-247` (attributes: function, total)

```k
0247:   syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:248-248` (attributes: none)

```k
0248:   rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

### syntax `reference-semantics/semantics/builtins.k:250-250` (attributes: function, total, function, total)

```k
0250:   syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:251-251` (attributes: none)

```k
0251:   rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule `reference-semantics/semantics/builtins.k:252-252` (attributes: none)

```k
0252:   rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### rule `reference-semantics/semantics/builtins.k:253-253` (attributes: none)

```k
0253:   rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

### rule `reference-semantics/semantics/builtins.k:254-254` (attributes: none)

```k
0254:   rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

### syntax `reference-semantics/semantics/builtins.k:255-255` (attributes: function, total)

```k
0255:   syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:256-256` (attributes: none)

```k
0256:   rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

### rule `reference-semantics/semantics/builtins.k:257-259` (attributes: none)

```k
0257:   rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
0258:     => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
0259:        requires inLevelE(L, O)
```

### rule `reference-semantics/semantics/builtins.k:260-262` (attributes: none)

```k
0260:   rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
0261:     => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
0262:        requires notBool inLevelE(L, O)
```

### rule `reference-semantics/semantics/builtins.k:263-264` (attributes: owise)

```k
0263:   rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
0264:     => evp(OO, appendIE(ON, CUR)) [owise]
```

### syntax `reference-semantics/semantics/builtins.k:265-265` (attributes: function, total)

```k
0265:   syntax Bool ::= inLevelE(String, String) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:266-266` (attributes: none)

```k
0266:   rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

### rule `reference-semantics/semantics/builtins.k:267-267` (attributes: none)

```k
0267:   rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

### rule `reference-semantics/semantics/builtins.k:268-268` (attributes: owise)

```k
0268:   rule inLevelE(_:String, _:String) => false [owise]
```

### syntax `reference-semantics/semantics/builtins.k:269-269` (attributes: function, total)

```k
0269:   syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:270-270` (attributes: none)

```k
0270:   rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

### rule `reference-semantics/semantics/builtins.k:271-271` (attributes: none)

```k
0271:   rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

### syntax `reference-semantics/semantics/builtins.k:272-272` (attributes: function, total)

```k
0272:   syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/builtins.k:273-273` (attributes: none)

```k
0273:   rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

### rule `reference-semantics/semantics/builtins.k:274-274` (attributes: none)

```k
0274:   rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

### syntax `reference-semantics/semantics/builtins.k:279-279` (attributes: none)

```k
0279:   syntax KItem ::= "#md5"
```

### rule `reference-semantics/semantics/builtins.k:280-281` (attributes: priority)

```k
0280:   rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
0281:        [priority(40)]
```

### rule `reference-semantics/semantics/builtins.k:282-282` (attributes: none)

```k
0282:   rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

### syntax `reference-semantics/semantics/builtins.k:283-283` (attributes: none)

```k
0283:   syntax Val ::= md5Obj(IntSeq)
```

### rule `reference-semantics/semantics/builtins.k:284-284` (attributes: none)

```k
0284:   rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

### syntax `reference-semantics/semantics/builtins.k:285-285` (attributes: function, total, symbol, no-evaluators)

```k
0285:   syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

### rule `reference-semantics/semantics/builtins.k:291-291` (attributes: none)

```k
0291:   rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

### rule `reference-semantics/semantics/builtins.k:292-292` (attributes: none)

```k
0292:   rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

### syntax `reference-semantics/semantics/builtins.k:293-293` (attributes: function, function)

```k
0293:   syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

### rule `reference-semantics/semantics/builtins.k:294-294` (attributes: none)

```k
0294:   rule isIntV(_:Int)         => true
```

### rule `reference-semantics/semantics/builtins.k:295-295` (attributes: owise)

```k
0295:   rule isIntV(_:Val)         => false [owise]
```

### rule `reference-semantics/semantics/builtins.k:296-296` (attributes: none)

```k
0296:   rule isStrV(str(_:IntSeq)) => true
```

### rule `reference-semantics/semantics/builtins.k:297-297` (attributes: owise)

```k
0297:   rule isStrV(_:Val)         => false [owise]
```

### endmodule `reference-semantics/semantics/builtins.k:298-298` (attributes: none)

```k
0298: endmodule
```

## `reference-semantics/semantics/call.k`

- SHA-256: `7e4d6c7cabe7bb4ccff52f21c5d5f30920ccb48d42864146ce53146509f736e4`; source lines: 95; declaration blocks: 29
- Kinds: `endmodule`=1, `imports`=3, `module`=1, `rule`=21, `syntax`=3

### module `reference-semantics/semantics/call.k:10-10` (attributes: none)

```k
0010: module MPY-CALL
```

### imports `reference-semantics/semantics/call.k:11-11` (attributes: none)

```k
0011:   imports MPY-METHODS
```

### imports `reference-semantics/semantics/call.k:12-12` (attributes: none)

```k
0012:   imports MPY-BUILTINS
```

### imports `reference-semantics/semantics/call.k:13-13` (attributes: none)

```k
0013:   imports MPY-FUNCTIONS
```

### rule `reference-semantics/semantics/call.k:16-16` (attributes: none)

```k
0016:   rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

### syntax `reference-semantics/semantics/call.k:19-19` (attributes: none)

```k
0019:   syntax KItem ::= #callee(Exprs)
```

### rule `reference-semantics/semantics/call.k:20-20` (attributes: owise)

```k
0020:   rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

### rule `reference-semantics/semantics/call.k:21-21` (attributes: none)

```k
0021:   rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

### rule `reference-semantics/semantics/call.k:24-24` (attributes: none)

```k
0024:   rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

### rule `reference-semantics/semantics/call.k:26-26` (attributes: none)

```k
0026:   rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

### rule `reference-semantics/semantics/call.k:27-27` (attributes: none)

```k
0027:   rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

### rule `reference-semantics/semantics/call.k:28-28` (attributes: none)

```k
0028:   rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

### rule `reference-semantics/semantics/call.k:29-29` (attributes: none)

```k
0029:   rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

### rule `reference-semantics/semantics/call.k:30-30` (attributes: none)

```k
0030:   rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

### rule `reference-semantics/semantics/call.k:31-31` (attributes: owise)

```k
0031:   rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

### rule `reference-semantics/semantics/call.k:32-32` (attributes: none)

```k
0032:   rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

### rule `reference-semantics/semantics/call.k:38-41` (attributes: priority)

```k
0038:   rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
0039:         => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
0040:        <heap> ... H |-> V:Val ... </heap>
0041:        [priority(40)]
```

### rule `reference-semantics/semantics/call.k:42-46` (attributes: priority)

```k
0042:   rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
0043:         => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
0044:        <heap> ... H |-> V:Val ... </heap>
0045:        requires notBool isRefV(A)
0046:        [priority(40)]
```

### rule `reference-semantics/semantics/call.k:47-50` (attributes: priority)

```k
0047:   rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
0048:         => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
0049:        <heap> ... H |-> V:Val ... </heap>
0050:        [priority(40)]
```

### syntax `reference-semantics/semantics/call.k:52-52` (attributes: function, total)

```k
0052:   syntax Bool ::= isMutMethod(String) [function, total]
```

### rule `reference-semantics/semantics/call.k:53-55` (attributes: none)

```k
0053:   rule isMutMethod(M:String)
0054:     => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
0055:        orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

### rule `reference-semantics/semantics/call.k:56-60` (attributes: priority)

```k
0056:   rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
0057:         => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
0058:        <heap> ... H |-> V:Val ... </heap>
0059:        requires notBool isMutMethod(M)
0060:        [priority(40)]
```

### rule `reference-semantics/semantics/call.k:63-67` (attributes: priority)

```k
0063:   rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
0064:         => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
0065:        <heap> ... H |-> V:Val ... </heap>
0066:        requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
0067:        [priority(40)]
```

### rule `reference-semantics/semantics/call.k:69-74` (attributes: none)

```k
0069:   rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
0070:         => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
0071:        <env>     CALLERL:Int => NEWL </env>
0072:        <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
0073:        <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
0074:        <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### rule `reference-semantics/semantics/call.k:80-85` (attributes: none)

```k
0080:   rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
0081:         => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
0082:        <env>     CALLERL:Int => NEWL </env>
0083:        <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
0084:        <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
0085:        <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

### syntax `reference-semantics/semantics/call.k:87-87` (attributes: none)

```k
0087:   syntax KItem ::= #allocCells(ParamNames)
```

### rule `reference-semantics/semantics/call.k:88-88` (attributes: none)

```k
0088:   rule <k> #allocCells(.ParamNames) => .K ... </k>
```

### rule `reference-semantics/semantics/call.k:89-94` (attributes: none)

```k
0089:   rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
0090:        <env> L:Int </env>
0091:        <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
0092:        <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
0093:        <heapLoc> N:Int => N +Int 1 </heapLoc>
0094:        requires notBool N in_keys(H)
```

### endmodule `reference-semantics/semantics/call.k:95-95` (attributes: none)

```k
0095: endmodule
```

## `reference-semantics/semantics/comprehension.k`

- SHA-256: `cf7c38aad5cff698ebb05ecbadf00cbf210ddb2f54ae86f22b328311c027c6a7`; source lines: 27; declaration blocks: 17
- Kinds: `endmodule`=1, `imports`=5, `module`=1, `rule`=7, `syntax`=3

### module `reference-semantics/semantics/comprehension.k:3-3` (attributes: none)

```k
0003: module MPY-COMPREHENSION
```

### imports `reference-semantics/semantics/comprehension.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/comprehension.k:5-5` (attributes: none)

```k
0005:   imports MPY-OPERATORS
```

### imports `reference-semantics/semantics/comprehension.k:6-6` (attributes: none)

```k
0006:   imports MPY-LIST
```

### imports `reference-semantics/semantics/comprehension.k:7-7` (attributes: none)

```k
0007:   imports MPY-CONTROLS
```

### imports `reference-semantics/semantics/comprehension.k:8-8` (attributes: none)

```k
0008:   imports MPY-FUNCTIONS
```

### rule `reference-semantics/semantics/comprehension.k:11-11` (attributes: none)

```k
0011:   rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### rule `reference-semantics/semantics/comprehension.k:12-12` (attributes: none)

```k
0012:   rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

### syntax `reference-semantics/semantics/comprehension.k:14-14` (attributes: macro)

```k
0014:   syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

### rule `reference-semantics/semantics/comprehension.k:15-16` (attributes: none)

```k
0015:   rule compBody(Gs:CompFors, ELT:Expr)
0016:     => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

### syntax `reference-semantics/semantics/comprehension.k:18-18` (attributes: macro-rec)

```k
0018:   syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

### rule `reference-semantics/semantics/comprehension.k:19-20` (attributes: none)

```k
0019:   rule compNest(.CompFors, ELT:Expr)
0020:     => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

### rule `reference-semantics/semantics/comprehension.k:21-22` (attributes: none)

```k
0021:   rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
0022:     => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

### syntax `reference-semantics/semantics/comprehension.k:24-24` (attributes: macro)

```k
0024:   syntax Expr ::= compGuard(Exprs) [macro]
```

### rule `reference-semantics/semantics/comprehension.k:25-25` (attributes: none)

```k
0025:   rule compGuard(.Exprs)             => Bool(true)
```

### rule `reference-semantics/semantics/comprehension.k:26-26` (attributes: none)

```k
0026:   rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

### endmodule `reference-semantics/semantics/comprehension.k:27-27` (attributes: none)

```k
0027: endmodule
```

## `reference-semantics/semantics/concrete.k`

- SHA-256: `1ffea42a32610e9116506d709e9163413aeb5f6deb7824ea554aca8341f2d305`; source lines: 60; declaration blocks: 24
- Kinds: `endmodule`=1, `imports`=1, `module`=1, `rule`=16, `syntax`=5

### module `reference-semantics/semantics/concrete.k:8-8` (attributes: none)

```k
0008: module MPY-CONCRETE
```

### imports `reference-semantics/semantics/concrete.k:9-9` (attributes: none)

```k
0009:   imports MPY
```

### rule `reference-semantics/semantics/concrete.k:13-15` (attributes: none)

```k
0013:   rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
0014:        <heap> HP:Map </heap>
0015:        requires hasRefVS(A) orBool hasRefVS(B)
```

### rule `reference-semantics/semantics/concrete.k:16-18` (attributes: none)

```k
0016:   rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
0017:        <heap> HP:Map </heap>
0018:        requires hasRefVS(A) orBool hasRefVS(B)
```

### syntax `reference-semantics/semantics/concrete.k:25-25` (attributes: none)

```k
0025:   syntax Val ::= kvP(Val, Val)
```

### syntax `reference-semantics/semantics/concrete.k:26-27` (attributes: none)

```k
0026:   syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
0027:                  | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

### rule `reference-semantics/semantics/concrete.k:28-30` (attributes: priority)

```k
0028:   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
0029:         => #ksort(VS, KV, .ValSeq, false) ... </k>
0030:        [priority(40)]
```

### rule `reference-semantics/semantics/concrete.k:31-33` (attributes: priority)

```k
0031:   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
0032:         => #ksort(VS, KV, .ValSeq, RB) ... </k>
0033:        [priority(40)]
```

### rule `reference-semantics/semantics/concrete.k:34-35` (attributes: none)

```k
0034:   rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
0035:         => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

### rule `reference-semantics/semantics/concrete.k:36-37` (attributes: none)

```k
0036:   rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
0037:         => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

### rule `reference-semantics/semantics/concrete.k:38-40` (attributes: none)

```k
0038:   rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
0039:         => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
0040:        requires notBool isKwV(K)
```

### syntax `reference-semantics/semantics/concrete.k:42-42` (attributes: function)

```k
0042:   syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

### rule `reference-semantics/semantics/concrete.k:43-43` (attributes: none)

```k
0043:   rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

### rule `reference-semantics/semantics/concrete.k:44-46` (attributes: none)

```k
0044:   rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
0045:     => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
0046:        requires kLt(K, K2)
```

### rule `reference-semantics/semantics/concrete.k:47-49` (attributes: none)

```k
0047:   rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
0048:     => vCons(kvP(K2, V2), insPair(R, K, V))
0049:        requires notBool kLt(K, K2)
```

### syntax `reference-semantics/semantics/concrete.k:51-51` (attributes: function)

```k
0051:   syntax Bool ::= kLt(Val, Val) [function]
```

### rule `reference-semantics/semantics/concrete.k:52-52` (attributes: none)

```k
0052:   rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

### rule `reference-semantics/semantics/concrete.k:53-53` (attributes: none)

```k
0053:   rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

### rule `reference-semantics/semantics/concrete.k:54-54` (attributes: none)

```k
0054:   rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### syntax `reference-semantics/semantics/concrete.k:56-56` (attributes: function, total)

```k
0056:   syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

### rule `reference-semantics/semantics/concrete.k:57-57` (attributes: none)

```k
0057:   rule unpairVS(.ValSeq) => .ValSeq
```

### rule `reference-semantics/semantics/concrete.k:58-58` (attributes: none)

```k
0058:   rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

### rule `reference-semantics/semantics/concrete.k:59-59` (attributes: owise)

```k
0059:   rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

### endmodule `reference-semantics/semantics/concrete.k:60-60` (attributes: none)

```k
0060: endmodule
```

## `reference-semantics/semantics/controls.k`

- SHA-256: `325c73757d5a7ccf541b93240accd590a2cee90d84470efa3a4a0a14165aafae`; source lines: 109; declaration blocks: 42
- Kinds: `endmodule`=1, `imports`=3, `module`=1, `rule`=34, `syntax`=3

### module `reference-semantics/semantics/controls.k:3-3` (attributes: none)

```k
0003: module MPY-CONTROLS
```

### imports `reference-semantics/semantics/controls.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/controls.k:5-5` (attributes: none)

```k
0005:   imports MPY-TUPLE
```

### imports `reference-semantics/semantics/controls.k:6-6` (attributes: none)

```k
0006:   imports MPY-ITER
```

### rule `reference-semantics/semantics/controls.k:9-11` (attributes: none)

```k
0009:   rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
0010:        <env> L:Int </env>
0011:        <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule `reference-semantics/semantics/controls.k:12-18` (attributes: priority)

```k
0012:   rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
0013:        <env> L:Int </env>
0014:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0015:        requires "$cells" in_keys(M)
0016:         andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
0017:         andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
0018:        [priority(40)]
```

### rule `reference-semantics/semantics/controls.k:20-23` (attributes: none)

```k
0020:   rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
0021:        <env> L:Int </env>
0022:        <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
0023:        requires X in_keys(M)
```

### rule `reference-semantics/semantics/controls.k:27-31` (attributes: priority)

```k
0027:   rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
0028:        <env> L:Int </env>
0029:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0030:        requires X in_keys(M) andBool isRefV({M[X]}:>Val)
0031:        [priority(40)]
```

### rule `reference-semantics/semantics/controls.k:35-35` (attributes: none)

```k
0035:   rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

### rule `reference-semantics/semantics/controls.k:36-36` (attributes: owise)

```k
0036:   rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

### syntax `reference-semantics/semantics/controls.k:37-37` (attributes: none)

```k
0037:   syntax KItem ::= #bindImports(ParamNames)
```

### rule `reference-semantics/semantics/controls.k:38-38` (attributes: none)

```k
0038:   rule <k> #bindImports(.ParamNames) => .K ... </k>
```

### rule `reference-semantics/semantics/controls.k:39-42` (attributes: none)

```k
0039:   rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
0040:        <env> L:Int </env>
0041:        <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
0042:        requires N ==String "floor" orBool N ==String "ceil"
```

### rule `reference-semantics/semantics/controls.k:43-44` (attributes: none)

```k
0043:   rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
0044:        requires notBool (N ==String "floor" orBool N ==String "ceil")
```

### rule `reference-semantics/semantics/controls.k:48-48` (attributes: none)

```k
0048:   rule <k> Expr(_:Val) => .K ... </k>
```

### syntax `reference-semantics/semantics/controls.k:51-51` (attributes: none)

```k
0051:   syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

### rule `reference-semantics/semantics/controls.k:52-52` (attributes: none)

```k
0052:   rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

### rule `reference-semantics/semantics/controls.k:53-53` (attributes: none)

```k
0053:   rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

### rule `reference-semantics/semantics/controls.k:54-54` (attributes: none)

```k
0054:   rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

### rule `reference-semantics/semantics/controls.k:57-58` (attributes: none)

```k
0057:   rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
0058:        requires truthy(V)
```

### rule `reference-semantics/semantics/controls.k:59-60` (attributes: none)

```k
0059:   rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
0060:        requires notBool truthy(V)
```

### syntax `reference-semantics/semantics/controls.k:65-67` (attributes: none)

```k
0065:   syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
0066:                  | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
0067:                  | #loopLbl(K) | "#cont" | "#brk"
```

### rule `reference-semantics/semantics/controls.k:69-69` (attributes: none)

```k
0069:   rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

### rule `reference-semantics/semantics/controls.k:71-71` (attributes: none)

```k
0071:   rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

### rule `reference-semantics/semantics/controls.k:72-72` (attributes: none)

```k
0072:   rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

### rule `reference-semantics/semantics/controls.k:73-74` (attributes: none)

```k
0073:   rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
0074:         => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

### rule `reference-semantics/semantics/controls.k:77-77` (attributes: none)

```k
0077:   rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

### rule `reference-semantics/semantics/controls.k:78-78` (attributes: none)

```k
0078:   rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

### rule `reference-semantics/semantics/controls.k:79-80` (attributes: none)

```k
0079:   rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
0080:        requires truthy(V)
```

### rule `reference-semantics/semantics/controls.k:81-82` (attributes: none)

```k
0081:   rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
0082:        requires notBool truthy(V)
```

### rule `reference-semantics/semantics/controls.k:85-85` (attributes: none)

```k
0085:   rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule `reference-semantics/semantics/controls.k:86-86` (attributes: none)

```k
0086:   rule <k> Continue => #cont ... </k>
```

### rule `reference-semantics/semantics/controls.k:87-87` (attributes: none)

```k
0087:   rule <k> Break => #brk ... </k>
```

### rule `reference-semantics/semantics/controls.k:88-88` (attributes: none)

```k
0088:   rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

### rule `reference-semantics/semantics/controls.k:89-89` (attributes: owise)

```k
0089:   rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

### rule `reference-semantics/semantics/controls.k:90-90` (attributes: none)

```k
0090:   rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

### rule `reference-semantics/semantics/controls.k:91-91` (attributes: owise)

```k
0091:   rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

### rule `reference-semantics/semantics/controls.k:95-97` (attributes: priority)

```k
0095:   rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
0096:        <heap> ... H |-> V:Val ... </heap>
0097:        [priority(40)]
```

### rule `reference-semantics/semantics/controls.k:98-100` (attributes: priority)

```k
0098:   rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
0099:        <heap> ... H |-> V:Val ... </heap>
0100:        [priority(40)]
```

### rule `reference-semantics/semantics/controls.k:101-103` (attributes: priority)

```k
0101:   rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
0102:        <heap> ... H |-> V:Val ... </heap>
0103:        [priority(40)]
```

### rule `reference-semantics/semantics/controls.k:106-108` (attributes: priority)

```k
0106:   rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
0107:        <heap> ... H |-> V:Val ... </heap>
0108:        [priority(40)]
```

### endmodule `reference-semantics/semantics/controls.k:109-109` (attributes: none)

```k
0109: endmodule
```

## `reference-semantics/semantics/core.k`

- SHA-256: `e0fdc11dc2b9cd0acb18fe7c832c1ea1ac0c9e79cadf40c63f34276aca513d7e`; source lines: 240; declaration blocks: 93
- Kinds: `configuration`=1, `endmodule`=1, `imports`=7, `module`=1, `rule`=46, `syntax`=37

### module `reference-semantics/semantics/core.k:3-3` (attributes: none)

```k
0003: module MPY-CORE
```

### imports `reference-semantics/semantics/core.k:4-4` (attributes: none)

```k
0004:   imports MPY-SYNTAX
```

### imports `reference-semantics/semantics/core.k:5-5` (attributes: none)

```k
0005:   imports INT
```

### imports `reference-semantics/semantics/core.k:6-6` (attributes: none)

```k
0006:   imports BOOL
```

### imports `reference-semantics/semantics/core.k:7-7` (attributes: none)

```k
0007:   imports STRING
```

### imports `reference-semantics/semantics/core.k:8-8` (attributes: none)

```k
0008:   imports MAP
```

### imports `reference-semantics/semantics/core.k:9-9` (attributes: none)

```k
0009:   imports LIST
```

### imports `reference-semantics/semantics/core.k:10-10` (attributes: none)

```k
0010:   imports K-EQUAL
```

### syntax `reference-semantics/semantics/core.k:13-13` (attributes: none)

```k
0013:   syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

### syntax `reference-semantics/semantics/core.k:14-14` (attributes: none)

```k
0014:   syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

### syntax `reference-semantics/semantics/core.k:15-15` (attributes: none)

```k
0015:   syntax Str    ::= str(IntSeq)
```

### syntax `reference-semantics/semantics/core.k:18-23` (attributes: none)

```k
0018:   syntax Iterable ::= list(ValSeq)
0019:                     | tuple(ValSeq)
0020:                     | Str
0021:                     | rangeObj(Int, Int, Int)
0022:                     | zipObj(ValSeq, ValSeq)
0023:                     | zipObjS(IntSeq, IntSeq)
```

### syntax `reference-semantics/semantics/core.k:25-34` (attributes: none)

```k
0025:   syntax Val      ::= Int
0026:                     | Bool
0027:                     | "noneV"
0028:                     | Iterable
0029:                     | ref(Int)          // a heap object: <heap> holds its list(VS)
0030:                     | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
0031:                     | closureVal(ParamNames, Stmts, Int)
0032:                     | typeV(String)     // a type object (int/str), resolved from the builtins frame
0033:                     | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
0034:                     | boundMethodV(Val, String)   // a cooled Attribute: obj.method
```

### syntax `reference-semantics/semantics/core.k:36-36` (attributes: none)

```k
0036:   syntax Parent   ::= "root" | parent(Int)
```

### syntax `reference-semantics/semantics/core.k:37-37` (attributes: none)

```k
0037:   syntax Scope    ::= scope(Map, Parent)
```

### syntax `reference-semantics/semantics/core.k:38-38` (attributes: none)

```k
0038:   syntax KResult  ::= Val
```

### syntax `reference-semantics/semantics/core.k:39-39` (attributes: none)

```k
0039:   syntax Expr     ::= Val   // cooling puts results back into expression holes
```

### syntax `reference-semantics/semantics/core.k:40-40` (attributes: none)

```k
0040:   syntax Vals     ::= List{Val, ","}
```

### syntax `reference-semantics/semantics/core.k:41-41` (attributes: none)

```k
0041:   syntax Exc      ::= "NoExc" | "AssertionError"
```

### syntax `reference-semantics/semantics/core.k:42-42` (attributes: none)

```k
0042:   syntax RetState ::= "noRet" | retV(Val)
```

### configuration `reference-semantics/semantics/core.k:49-60` (attributes: none)

```k
0049:   configuration
0050:     <k>       #loadAll($PGM:Module) </k>
0051:     <env>     0 </env>
0052:     <scopes>   0     |-> scope(.Map, parent(-1))
0053:               -1    |-> builtinsScope </scopes>
0054:     <scopeLoc> 1 </scopeLoc>
0055:     <heap>    .Map </heap>
0056:     <heapLoc> 0 </heapLoc>
0057:     <stack>   .List </stack>
0058:     <ret>     noRet </ret>
0059:     <exc>     NoExc </exc>
0060:     <exit-code exit=""> 0 </exit-code>
```

### syntax `reference-semantics/semantics/core.k:68-68` (attributes: function, total)

```k
0068:   syntax Bool ::= isRefV(Val) [function, total]
```

### rule `reference-semantics/semantics/core.k:69-69` (attributes: none)

```k
0069:   rule isRefV(ref(_:Int)) => true
```

### rule `reference-semantics/semantics/core.k:70-70` (attributes: owise)

```k
0070:   rule isRefV(_:Val)      => false [owise]
```

### syntax `reference-semantics/semantics/core.k:75-75` (attributes: none)

```k
0075:   syntax HeapVal ::= cellV(Val)
```

### syntax `reference-semantics/semantics/core.k:76-76` (attributes: function, total)

```k
0076:   syntax Bool ::= isCellRef(Val) [function, total]
```

### rule `reference-semantics/semantics/core.k:77-77` (attributes: none)

```k
0077:   rule isCellRef(cellRef(_:Int)) => true
```

### rule `reference-semantics/semantics/core.k:78-78` (attributes: owise)

```k
0078:   rule isCellRef(_:Val)          => false [owise]
```

### rule `reference-semantics/semantics/core.k:85-90` (attributes: priority)

```k
0085:   rule <k> cellRef(H:Int) => V ... </k>
0086:        <env> L:Int </env>
0087:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0088:        <heap> ... H |-> cellV(V:Val) ... </heap>
0089:        requires "$cells" in_keys(M)
0090:        [priority(40)]
```

### syntax `reference-semantics/semantics/core.k:95-95` (attributes: none)

```k
0095:   syntax Val ::= kwV(String, Val)
```

### syntax `reference-semantics/semantics/core.k:96-96` (attributes: none)

```k
0096:   syntax KItem ::= #kwTag(String)
```

### rule `reference-semantics/semantics/core.k:97-97` (attributes: none)

```k
0097:   rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

### rule `reference-semantics/semantics/core.k:98-99` (attributes: none)

```k
0098:   rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
0099:        requires notBool isKwV(V)
```

### syntax `reference-semantics/semantics/core.k:100-100` (attributes: function, total)

```k
0100:   syntax Bool ::= isKwV(Val) [function, total]
```

### rule `reference-semantics/semantics/core.k:101-101` (attributes: none)

```k
0101:   rule isKwV(kwV(_:String, _:Val)) => true
```

### rule `reference-semantics/semantics/core.k:102-102` (attributes: owise)

```k
0102:   rule isKwV(_:Val)                => false [owise]
```

### syntax `reference-semantics/semantics/core.k:106-106` (attributes: none)

```k
0106:   syntax Val ::= cellsMark(ParamNames)
```

### syntax `reference-semantics/semantics/core.k:107-107` (attributes: function)

```k
0107:   syntax ParamNames ::= cellsOf(Val) [function]
```

### rule `reference-semantics/semantics/core.k:108-108` (attributes: none)

```k
0108:   rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

### syntax `reference-semantics/semantics/core.k:109-109` (attributes: function, total)

```k
0109:   syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

### rule `reference-semantics/semantics/core.k:110-110` (attributes: none)

```k
0110:   rule pnMember(_:String, .ParamNames) => false
```

### rule `reference-semantics/semantics/core.k:111-111` (attributes: none)

```k
0111:   rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

### syntax `reference-semantics/semantics/core.k:113-113` (attributes: none)

```k
0113:   syntax KItem ::= #cellW(Val, Val)
```

### rule `reference-semantics/semantics/core.k:114-115` (attributes: none)

```k
0114:   rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
0115:        <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

### syntax `reference-semantics/semantics/core.k:117-117` (attributes: none)

```k
0117:   syntax KItem ::= #alloc(Val)
```

### rule `reference-semantics/semantics/core.k:118-121` (attributes: none)

```k
0118:   rule <k> #alloc(V:Val) => ref(N) ... </k>
0119:        <heap>    H:Map => (N |-> V) H </heap>
0120:        <heapLoc> N:Int => N +Int 1 </heapLoc>
0121:        requires notBool N in_keys(H)
```

### syntax `reference-semantics/semantics/core.k:124-124` (attributes: none)

```k
0124:   syntax KItem ::= #loadAll(Module)
```

### rule `reference-semantics/semantics/core.k:125-125` (attributes: none)

```k
0125:   rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

### rule `reference-semantics/semantics/core.k:126-126` (attributes: none)

```k
0126:   rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

### rule `reference-semantics/semantics/core.k:127-127` (attributes: none)

```k
0127:   rule <k> .Stmts => .K ... </k>
```

### syntax `reference-semantics/semantics/core.k:130-130` (attributes: none)

```k
0130:   syntax KItem ::= #look(String, Int)
```

### rule `reference-semantics/semantics/core.k:131-131` (attributes: none)

```k
0131:   rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

### rule `reference-semantics/semantics/core.k:132-134` (attributes: none)

```k
0132:   rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
0133:        <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
0134:        requires X in_keys(M)
```

### rule `reference-semantics/semantics/core.k:145-151` (attributes: priority)

```k
0145:   rule <k> #look(X:String, L:Int) => V ... </k>
0146:        <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
0147:        <heap> ... H |-> cellV(V:Val) ... </heap>
0148:        requires X in_keys(M) andBool "$cells" in_keys(M)
0149:         andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
0150:         andBool {M[X]}:>Val ==K cellRef(H)
0151:        [priority(40)]
```

### rule `reference-semantics/semantics/core.k:152-154` (attributes: none)

```k
0152:   rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
0153:        <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
0154:        requires notBool (X in_keys(M))
```

### syntax `reference-semantics/semantics/core.k:157-157` (attributes: function, total)

```k
0157:   syntax Scope ::= "builtinsScope" [function, total]
```

### rule `reference-semantics/semantics/core.k:158-181` (attributes: none)

```k
0158:   rule builtinsScope
0159:     => scope(.Map [ "len"    <- builtinV("len")    ]
0160:                   [ "set"    <- builtinV("set")    ]
0161:                   [ "sum"    <- builtinV("sum")    ]
0162:                   [ "abs"    <- builtinV("abs")    ]
0163:                   [ "min"    <- builtinV("min")    ]
0164:                   [ "max"    <- builtinV("max")    ]
0165:                   [ "ord"    <- builtinV("ord")    ]
0166:                   [ "chr"    <- builtinV("chr")    ]
0167:                   [ "range"  <- builtinV("range")  ]
0168:                   [ "all"    <- builtinV("all")    ]
0169:                   [ "any"    <- builtinV("any")    ]
0170:                   [ "zip"    <- builtinV("zip")    ]
0171:                   [ "isinstance" <- builtinV("isinstance") ]
0172:                   [ "sorted" <- builtinV("sorted") ]
0173:                   [ "list"   <- builtinV("list")   ]
0174:                   [ "round"  <- builtinV("round")  ]
0175:                   [ "bin"    <- builtinV("bin")    ]
0176:                   [ "enumerate" <- builtinV("enumerate") ]
0177:                   [ "map"    <- builtinV("map")    ]
0178:                   [ "eval"   <- builtinV("eval")   ]
0179:                   [ "int"    <- typeV("int")       ]
0180:                   [ "str"    <- typeV("str")       ]
0181:                   [ "float"  <- typeV("float")     ], root)
```

### syntax `reference-semantics/semantics/core.k:185-185` (attributes: none)

```k
0185:   syntax ApplyK ::= toCall(Val)
```

### syntax `reference-semantics/semantics/core.k:186-188` (attributes: none)

```k
0186:   syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
0187:                   | #evalArgCont(Exprs, Vals, ApplyK)
0188:                   | #applyK(ApplyK, Vals)
```

### rule `reference-semantics/semantics/core.k:189-189` (attributes: none)

```k
0189:   rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

### rule `reference-semantics/semantics/core.k:190-190` (attributes: none)

```k
0190:   rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

### rule `reference-semantics/semantics/core.k:191-191` (attributes: none)

```k
0191:   rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

### rule `reference-semantics/semantics/core.k:194-194` (attributes: none)

```k
0194:   rule <k> Int(I:Int)   => I ... </k>
```

### rule `reference-semantics/semantics/core.k:195-195` (attributes: none)

```k
0195:   rule <k> Bool(B:Bool) => B ... </k>
```

### rule `reference-semantics/semantics/core.k:196-196` (attributes: none)

```k
0196:   rule <k> NoneVal      => noneV ... </k>
```

### syntax `reference-semantics/semantics/core.k:199-199` (attributes: function)

```k
0199:   syntax Bool ::= truthy(Val) [function]
```

### rule `reference-semantics/semantics/core.k:200-200` (attributes: none)

```k
0200:   rule truthy(B:Bool)          => B
```

### rule `reference-semantics/semantics/core.k:201-201` (attributes: none)

```k
0201:   rule truthy(noneV)           => false
```

### rule `reference-semantics/semantics/core.k:202-202` (attributes: none)

```k
0202:   rule truthy(I:Int)           => I =/=Int 0
```

### rule `reference-semantics/semantics/core.k:203-203` (attributes: none)

```k
0203:   rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

### rule `reference-semantics/semantics/core.k:204-204` (attributes: none)

```k
0204:   rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

### rule `reference-semantics/semantics/core.k:205-205` (attributes: none)

```k
0205:   rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

### syntax `reference-semantics/semantics/core.k:208-208` (attributes: function)

```k
0208:   syntax Val  ::= applyUn(String, Val) [function]
```

### syntax `reference-semantics/semantics/core.k:209-209` (attributes: function)

```k
0209:   syntax Val  ::= applyBin(String, Val, Val) [function]
```

### syntax `reference-semantics/semantics/core.k:210-210` (attributes: function)

```k
0210:   syntax Bool ::= applyCmp(String, Val, Val) [function]
```

### syntax `reference-semantics/semantics/core.k:213-213` (attributes: function, total)

```k
0213:   syntax Vals ::= appendVal(Vals, Val) [function, total]
```

### rule `reference-semantics/semantics/core.k:214-214` (attributes: none)

```k
0214:   rule appendVal(.Vals, V:Val)              => V , .Vals
```

### rule `reference-semantics/semantics/core.k:215-215` (attributes: none)

```k
0215:   rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

### syntax `reference-semantics/semantics/core.k:217-217` (attributes: function, total)

```k
0217:   syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

### rule `reference-semantics/semantics/core.k:218-218` (attributes: none)

```k
0218:   rule vals2valSeq(.Vals)            => .ValSeq
```

### rule `reference-semantics/semantics/core.k:219-219` (attributes: none)

```k
0219:   rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

### syntax `reference-semantics/semantics/core.k:223-223` (attributes: function, total)

```k
0223:   syntax Int ::= vsLen(ValSeq) [function, total]
```

### rule `reference-semantics/semantics/core.k:224-224` (attributes: none)

```k
0224:   rule vsLen(.ValSeq)                => 0
```

### rule `reference-semantics/semantics/core.k:225-225` (attributes: none)

```k
0225:   rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

### syntax `reference-semantics/semantics/core.k:227-227` (attributes: function, total)

```k
0227:   syntax Int ::= isLen(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/core.k:228-228` (attributes: none)

```k
0228:   rule isLen(.IntSeq)                => 0
```

### rule `reference-semantics/semantics/core.k:229-229` (attributes: none)

```k
0229:   rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

### syntax `reference-semantics/semantics/core.k:233-233` (attributes: function, total)

```k
0233:   syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

### rule `reference-semantics/semantics/core.k:234-234` (attributes: none)

```k
0234:   rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

### rule `reference-semantics/semantics/core.k:235-235` (attributes: none)

```k
0235:   rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

### rule `reference-semantics/semantics/core.k:236-237` (attributes: none)

```k
0236:   rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
0237:        requires I >Int 0
```

### rule `reference-semantics/semantics/core.k:238-239` (attributes: none)

```k
0238:   rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
0239:        requires I <Int 0
```

### endmodule `reference-semantics/semantics/core.k:240-240` (attributes: none)

```k
0240: endmodule
```

## `reference-semantics/semantics/dict.k`

- SHA-256: `779b06e18162464c8422bbd6ac35fa0b9e34ef82807d5c707c6f4552d63c0580`; source lines: 104; declaration blocks: 46
- Kinds: `endmodule`=1, `imports`=4, `module`=1, `rule`=28, `syntax`=12

### module `reference-semantics/semantics/dict.k:13-13` (attributes: none)

```k
0013: module MPY-DICT
```

### imports `reference-semantics/semantics/dict.k:14-14` (attributes: none)

```k
0014:   imports MPY-CORE
```

### imports `reference-semantics/semantics/dict.k:15-15` (attributes: none)

```k
0015:   imports MPY-ITER
```

### imports `reference-semantics/semantics/dict.k:16-16` (attributes: none)

```k
0016:   imports MPY-METHODS
```

### imports `reference-semantics/semantics/dict.k:17-17` (attributes: none)

```k
0017:   imports MPY-LIST
```

### syntax `reference-semantics/semantics/dict.k:20-20` (attributes: none)

```k
0020:   syntax Val ::= dictV(ValSeq, ValSeq)
```

### syntax `reference-semantics/semantics/dict.k:23-25` (attributes: none)

```k
0023:   syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
0024:                  | #dictKey(Expr, Entries, ValSeq, ValSeq)
0025:                  | #dictVal(Val, Entries, ValSeq, ValSeq)
```

### rule `reference-semantics/semantics/dict.k:26-26` (attributes: none)

```k
0026:   rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

### rule `reference-semantics/semantics/dict.k:27-27` (attributes: none)

```k
0027:   rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

### rule `reference-semantics/semantics/dict.k:28-29` (attributes: none)

```k
0028:   rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
0029:         => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

### rule `reference-semantics/semantics/dict.k:30-31` (attributes: none)

```k
0030:   rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
0031:         => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

### rule `reference-semantics/semantics/dict.k:32-33` (attributes: none)

```k
0032:   rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
0033:         => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

### syntax `reference-semantics/semantics/dict.k:37-37` (attributes: function, total)

```k
0037:   syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

### rule `reference-semantics/semantics/dict.k:38-38` (attributes: none)

```k
0038:   rule dHasKey(.ValSeq, _:Val)                => false
```

### rule `reference-semantics/semantics/dict.k:39-39` (attributes: none)

```k
0039:   rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

### rule `reference-semantics/semantics/dict.k:40-40` (attributes: none)

```k
0040:   rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

### syntax `reference-semantics/semantics/dict.k:43-43` (attributes: function, total)

```k
0043:   syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

### rule `reference-semantics/semantics/dict.k:44-44` (attributes: none)

```k
0044:   rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

### rule `reference-semantics/semantics/dict.k:45-45` (attributes: none)

```k
0045:   rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

### syntax `reference-semantics/semantics/dict.k:49-49` (attributes: function, total)

```k
0049:   syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

### rule `reference-semantics/semantics/dict.k:50-51` (attributes: none)

```k
0050:   rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
0051:        requires A ==K K
```

### rule `reference-semantics/semantics/dict.k:52-53` (attributes: none)

```k
0052:   rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
0053:        requires notBool (A ==K K)
```

### rule `reference-semantics/semantics/dict.k:54-54` (attributes: owise)

```k
0054:   rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

### rule `reference-semantics/semantics/dict.k:58-60` (attributes: priority)

```k
0058:   rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
0059:         => #alloc(list(KS)) ... </k>
0060:        [priority(40)]
```

### rule `reference-semantics/semantics/dict.k:63-63` (attributes: none)

```k
0063:   rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

### syntax `reference-semantics/semantics/dict.k:64-64` (attributes: function)

```k
0064:   syntax Val ::= applyIndexD(Val, Val) [function]
```

### rule `reference-semantics/semantics/dict.k:65-66` (attributes: priority)

```k
0065:   rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
0066:        [priority(45)]
```

### syntax `reference-semantics/semantics/dict.k:70-70` (attributes: function)

```k
0070:   syntax Val ::= dictSet(Val, Val, Val) [function]
```

### rule `reference-semantics/semantics/dict.k:71-71` (attributes: none)

```k
0071:   rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

### syntax `reference-semantics/semantics/dict.k:76-76` (attributes: none)

```k
0076:   syntax KItem ::= #dsetK(String, Val)
```

### rule `reference-semantics/semantics/dict.k:77-77` (attributes: none)

```k
0077:   rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

### rule `reference-semantics/semantics/dict.k:78-81` (attributes: none)

```k
0078:   rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
0079:        <env> L:Int </env>
0080:        <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
0081:        requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

### rule `reference-semantics/semantics/dict.k:82-85` (attributes: none)

```k
0082:   rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
0083:        <env> L:Int </env>
0084:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0085:        requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

### syntax `reference-semantics/semantics/dict.k:86-86` (attributes: none)

```k
0086:   syntax KItem ::= #dsetV(Val, Val, Val)
```

### rule `reference-semantics/semantics/dict.k:87-88` (attributes: none)

```k
0087:   rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
0088:        <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

### syntax `reference-semantics/semantics/dict.k:90-90` (attributes: function, total)

```k
0090:   syntax Int ::= normIdxD(Int, Int) [function, total]
```

### rule `reference-semantics/semantics/dict.k:91-91` (attributes: none)

```k
0091:   rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule `reference-semantics/semantics/dict.k:92-92` (attributes: none)

```k
0092:   rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

### rule `reference-semantics/semantics/dict.k:95-96` (attributes: none)

```k
0095:   rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
0096:     => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

### syntax `reference-semantics/semantics/dict.k:97-97` (attributes: function)

```k
0097:   syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

### rule `reference-semantics/semantics/dict.k:98-98` (attributes: none)

```k
0098:   rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

### rule `reference-semantics/semantics/dict.k:99-100` (attributes: none)

```k
0099:   rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
0100:     => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

### syntax `reference-semantics/semantics/dict.k:101-101` (attributes: function)

```k
0101:   syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

### rule `reference-semantics/semantics/dict.k:102-102` (attributes: none)

```k
0102:   rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

### rule `reference-semantics/semantics/dict.k:103-103` (attributes: none)

```k
0103:   rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

### endmodule `reference-semantics/semantics/dict.k:104-104` (attributes: none)

```k
0104: endmodule
```

## `reference-semantics/semantics/float.k`

- SHA-256: `5dfeee8700c90c3aa6dc515b15b74283882845fb6cdcc3627d97ef650124b70f`; source lines: 273; declaration blocks: 160
- Kinds: `endmodule`=1, `imports`=3, `module`=1, `rule`=121, `syntax`=34

### module `reference-semantics/semantics/float.k:14-14` (attributes: none)

```k
0014: module MPY-FLOAT
```

### imports `reference-semantics/semantics/float.k:15-15` (attributes: none)

```k
0015:   imports MPY-OPERATORS
```

### imports `reference-semantics/semantics/float.k:16-16` (attributes: none)

```k
0016:   imports MPY-BUILTINS
```

### imports `reference-semantics/semantics/float.k:17-17` (attributes: none)

```k
0017:   imports FLOAT
```

### syntax `reference-semantics/semantics/float.k:20-20` (attributes: none)

```k
0020:   syntax Val ::= Float
```

### rule `reference-semantics/semantics/float.k:21-21` (attributes: none)

```k
0021:   rule <k> Float(F:Float) => F ... </k>
```

### syntax `reference-semantics/semantics/float.k:24-24` (attributes: function, total, symbol, no-evaluators)

```k
0024:   syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:25-25` (attributes: concrete)

```k
0025:   rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

### rule `reference-semantics/semantics/float.k:27-27` (attributes: none)

```k
0027:   rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

### syntax `reference-semantics/semantics/float.k:30-30` (attributes: function, total, symbol, no-evaluators)

```k
0030:   syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:31-31` (attributes: concrete)

```k
0031:   rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

### rule `reference-semantics/semantics/float.k:32-32` (attributes: none)

```k
0032:   rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

### syntax `reference-semantics/semantics/float.k:37-37` (attributes: function, total, symbol, no-evaluators)

```k
0037:   syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:38-38` (attributes: concrete)

```k
0038:   rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

### rule `reference-semantics/semantics/float.k:39-39` (attributes: none)

```k
0039:   rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

### rule `reference-semantics/semantics/float.k:43-43` (attributes: none)

```k
0043:   rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

### rule `reference-semantics/semantics/float.k:44-44` (attributes: none)

```k
0044:   rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

### syntax `reference-semantics/semantics/float.k:50-50` (attributes: function, total, symbol, no-evaluators)

```k
0050:   syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:51-51` (attributes: concrete)

```k
0051:   rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:52-52` (attributes: none)

```k
0052:   rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

### syntax `reference-semantics/semantics/float.k:54-54` (attributes: function, total, symbol, no-evaluators)

```k
0054:   syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:55-55` (attributes: concrete)

```k
0055:   rule absF(F:Float) => absFloat(F) [concrete]
```

### rule `reference-semantics/semantics/float.k:56-56` (attributes: none)

```k
0056:   rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

### rule `reference-semantics/semantics/float.k:61-61` (attributes: none)

```k
0061:   rule <k> Import(_:String) => .K ... </k>
```

### syntax `reference-semantics/semantics/float.k:65-65` (attributes: none)

```k
0065:   syntax KItem ::= "#mathCeil"
```

### rule `reference-semantics/semantics/float.k:66-66` (attributes: priority)

```k
0066:   rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

### rule `reference-semantics/semantics/float.k:67-67` (attributes: none)

```k
0067:   rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

### syntax `reference-semantics/semantics/float.k:70-70` (attributes: none)

```k
0070:   syntax KItem ::= "#mathFloor"
```

### rule `reference-semantics/semantics/float.k:71-71` (attributes: priority)

```k
0071:   rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

### rule `reference-semantics/semantics/float.k:72-72` (attributes: none)

```k
0072:   rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

### syntax `reference-semantics/semantics/float.k:73-73` (attributes: function, total, symbol)

```k
0073:   syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

### rule `reference-semantics/semantics/float.k:74-74` (attributes: concrete)

```k
0074:   rule floorFI(I:Int)   => I                        [concrete]
```

### rule `reference-semantics/semantics/float.k:75-75` (attributes: concrete)

```k
0075:   rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

### rule `reference-semantics/semantics/float.k:78-78` (attributes: none)

```k
0078:   rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

### rule `reference-semantics/semantics/float.k:79-79` (attributes: none)

```k
0079:   rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

### syntax `reference-semantics/semantics/float.k:82-82` (attributes: none)

```k
0082:   syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

### rule `reference-semantics/semantics/float.k:83-83` (attributes: priority)

```k
0083:   rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

### rule `reference-semantics/semantics/float.k:84-84` (attributes: none)

```k
0084:   rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

### rule `reference-semantics/semantics/float.k:85-85` (attributes: none)

```k
0085:   rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

### syntax `reference-semantics/semantics/float.k:86-86` (attributes: function, total, symbol)

```k
0086:   syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

### rule `reference-semantics/semantics/float.k:87-87` (attributes: concrete)

```k
0087:   rule toF(F:Float) => F        [concrete]
```

### rule `reference-semantics/semantics/float.k:88-88` (attributes: concrete)

```k
0088:   rule toF(I:Int)   => intToF(I) [concrete]
```

### syntax `reference-semantics/semantics/float.k:93-93` (attributes: function, total, symbol)

```k
0093:   syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

### rule `reference-semantics/semantics/float.k:94-94` (attributes: concrete)

```k
0094:   rule ceilF(I:Int)   => I                       [concrete]
```

### rule `reference-semantics/semantics/float.k:95-95` (attributes: concrete)

```k
0095:   rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

### rule `reference-semantics/semantics/float.k:99-99` (attributes: none)

```k
0099:   rule applyUn("-", F:Float) => 0.0 -Float F
```

### syntax `reference-semantics/semantics/float.k:103-103` (attributes: function, total, symbol, no-evaluators)

```k
0103:   syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:104-104` (attributes: concrete)

```k
0104:   rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:105-105` (attributes: none)

```k
0105:   rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

### syntax `reference-semantics/semantics/float.k:107-107` (attributes: function, total, symbol, no-evaluators)

```k
0107:   syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:108-108` (attributes: concrete)

```k
0108:   rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:109-109` (attributes: none)

```k
0109:   rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

### syntax `reference-semantics/semantics/float.k:111-111` (attributes: function, total, symbol, no-evaluators)

```k
0111:   syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:112-112` (attributes: concrete)

```k
0112:   rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:113-113` (attributes: none)

```k
0113:   rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

### syntax `reference-semantics/semantics/float.k:115-115` (attributes: function, total, symbol, no-evaluators)

```k
0115:   syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:116-116` (attributes: concrete)

```k
0116:   rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:117-117` (attributes: none)

```k
0117:   rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

### syntax `reference-semantics/semantics/float.k:119-119` (attributes: function, total, symbol, no-evaluators)

```k
0119:   syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:120-120` (attributes: concrete)

```k
0120:   rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:121-121` (attributes: none)

```k
0121:   rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

### syntax `reference-semantics/semantics/float.k:125-125` (attributes: function, total, symbol, no-evaluators)

```k
0125:   syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:126-126` (attributes: concrete)

```k
0126:   rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:127-127` (attributes: none)

```k
0127:   rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

### rule `reference-semantics/semantics/float.k:128-128` (attributes: none)

```k
0128:   rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

### rule `reference-semantics/semantics/float.k:129-129` (attributes: none)

```k
0129:   rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

### rule `reference-semantics/semantics/float.k:132-132` (attributes: none)

```k
0132:   rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:133-133` (attributes: none)

```k
0133:   rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:134-134` (attributes: none)

```k
0134:   rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:135-135` (attributes: none)

```k
0135:   rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:136-136` (attributes: none)

```k
0136:   rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:137-137` (attributes: none)

```k
0137:   rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:138-138` (attributes: none)

```k
0138:   rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:139-139` (attributes: none)

```k
0139:   rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

### syntax `reference-semantics/semantics/float.k:142-142` (attributes: function, total, symbol, no-evaluators)

```k
0142:   syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:143-143` (attributes: concrete)

```k
0143:   rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

### rule `reference-semantics/semantics/float.k:144-144` (attributes: none)

```k
0144:   rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:145-145` (attributes: none)

```k
0145:   rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:146-146` (attributes: none)

```k
0146:   rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:147-147` (attributes: none)

```k
0147:   rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:148-148` (attributes: none)

```k
0148:   rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:149-149` (attributes: none)

```k
0149:   rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:150-150` (attributes: none)

```k
0150:   rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:151-151` (attributes: none)

```k
0151:   rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:154-154` (attributes: none)

```k
0154:   rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

### rule `reference-semantics/semantics/float.k:155-155` (attributes: none)

```k
0155:   rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

### syntax `reference-semantics/semantics/float.k:160-160` (attributes: function, total, symbol, no-evaluators)

```k
0160:   syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:161-161` (attributes: concrete)

```k
0161:   rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

### rule `reference-semantics/semantics/float.k:162-164` (attributes: concrete)

```k
0162:   rule decStrToF(CS:IntSeq)
0163:     => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
0164:        requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

### syntax `reference-semantics/semantics/float.k:165-165` (attributes: function)

```k
0165:   syntax Int ::= headIS(IntSeq) [function]
```

### rule `reference-semantics/semantics/float.k:166-166` (attributes: none)

```k
0166:   rule headIS(iCons(C:Int, _:IntSeq)) => C
```

### syntax `reference-semantics/semantics/float.k:167-167` (attributes: function, total, function, total)

```k
0167:   syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/float.k:168-168` (attributes: none)

```k
0168:   rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

### rule `reference-semantics/semantics/float.k:169-169` (attributes: none)

```k
0169:   rule intPartAcc(.IntSeq, A:Int) => A
```

### rule `reference-semantics/semantics/float.k:170-170` (attributes: none)

```k
0170:   rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

### rule `reference-semantics/semantics/float.k:171-172` (attributes: none)

```k
0171:   rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
0172:        requires C =/=Int 46
```

### syntax `reference-semantics/semantics/float.k:173-173` (attributes: function, total, function, total)

```k
0173:   syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/float.k:174-174` (attributes: none)

```k
0174:   rule fracPart(.IntSeq) => 0
```

### rule `reference-semantics/semantics/float.k:175-175` (attributes: none)

```k
0175:   rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

### rule `reference-semantics/semantics/float.k:176-176` (attributes: none)

```k
0176:   rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

### rule `reference-semantics/semantics/float.k:177-177` (attributes: none)

```k
0177:   rule fracAcc(.IntSeq, A:Int) => A
```

### rule `reference-semantics/semantics/float.k:178-178` (attributes: none)

```k
0178:   rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

### syntax `reference-semantics/semantics/float.k:179-179` (attributes: function, total, function, total)

```k
0179:   syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/float.k:180-180` (attributes: none)

```k
0180:   rule fracScale(.IntSeq) => 1
```

### rule `reference-semantics/semantics/float.k:181-181` (attributes: none)

```k
0181:   rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

### rule `reference-semantics/semantics/float.k:182-182` (attributes: none)

```k
0182:   rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

### rule `reference-semantics/semantics/float.k:183-183` (attributes: none)

```k
0183:   rule fscAcc(.IntSeq, A:Int) => A
```

### rule `reference-semantics/semantics/float.k:184-184` (attributes: none)

```k
0184:   rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

### rule `reference-semantics/semantics/float.k:185-185` (attributes: none)

```k
0185:   rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

### rule `reference-semantics/semantics/float.k:186-186` (attributes: none)

```k
0186:   rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

### rule `reference-semantics/semantics/float.k:187-187` (attributes: none)

```k
0187:   rule applyBuiltin("float", F:Float, .Vals)        => F
```

### syntax `reference-semantics/semantics/float.k:190-190` (attributes: function, total, symbol, no-evaluators)

```k
0190:   syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:191-191` (attributes: concrete)

```k
0191:   rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

### rule `reference-semantics/semantics/float.k:192-192` (attributes: none)

```k
0192:   rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

### syntax `reference-semantics/semantics/float.k:195-195` (attributes: function, total, symbol, no-evaluators)

```k
0195:   syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:196-196` (attributes: concrete)

```k
0196:   rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

### rule `reference-semantics/semantics/float.k:197-197` (attributes: none)

```k
0197:   rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:198-198` (attributes: none)

```k
0198:   rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:199-199` (attributes: none)

```k
0199:   rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:200-200` (attributes: none)

```k
0200:   rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:201-201` (attributes: none)

```k
0201:   rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:202-202` (attributes: none)

```k
0202:   rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:203-203` (attributes: none)

```k
0203:   rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:204-204` (attributes: none)

```k
0204:   rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

### rule `reference-semantics/semantics/float.k:205-205` (attributes: none)

```k
0205:   rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

### rule `reference-semantics/semantics/float.k:206-206` (attributes: none)

```k
0206:   rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

### syntax `reference-semantics/semantics/float.k:209-209` (attributes: function, total, symbol, no-evaluators)

```k
0209:   syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:210-210` (attributes: concrete)

```k
0210:   rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

### rule `reference-semantics/semantics/float.k:211-211` (attributes: none)

```k
0211:   rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

### rule `reference-semantics/semantics/float.k:213-213` (attributes: none)

```k
0213:   rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

### rule `reference-semantics/semantics/float.k:214-214` (attributes: none)

```k
0214:   rule applyBuiltin("float", F:Float, .Vals) => F
```

### syntax `reference-semantics/semantics/float.k:217-217` (attributes: function, total, symbol, no-evaluators)

```k
0217:   syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:218-222` (attributes: concrete)

```k
0218:   rule roundF(F:Float)
0219:     => #if (F -Float floorFloat(F)) ==Float 0.5
0220:        #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
0221:               #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
0222:        #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

### syntax `reference-semantics/semantics/float.k:223-223` (attributes: function, total, symbol, no-evaluators)

```k
0223:   syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:224-226` (attributes: concrete)

```k
0224:   rule roundFN(F:Float, N:Int)
0225:     => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
0226:        /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

### rule `reference-semantics/semantics/float.k:227-227` (attributes: none)

```k
0227:   rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

### rule `reference-semantics/semantics/float.k:228-228` (attributes: none)

```k
0228:   rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

### syntax `reference-semantics/semantics/float.k:230-230` (attributes: function, total, symbol, no-evaluators)

```k
0230:   syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

### rule `reference-semantics/semantics/float.k:231-231` (attributes: concrete)

```k
0231:   rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

### syntax `reference-semantics/semantics/float.k:232-232` (attributes: none)

```k
0232:   syntax KItem ::= "#mathSqrt"
```

### rule `reference-semantics/semantics/float.k:233-233` (attributes: priority)

```k
0233:   rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

### rule `reference-semantics/semantics/float.k:234-234` (attributes: none)

```k
0234:   rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

### rule `reference-semantics/semantics/float.k:235-235` (attributes: none)

```k
0235:   rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

### syntax `reference-semantics/semantics/float.k:243-243` (attributes: none)

```k
0243:   syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

### rule `reference-semantics/semantics/float.k:244-244` (attributes: none)

```k
0244:   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule `reference-semantics/semantics/float.k:245-245` (attributes: none)

```k
0245:   rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

### rule `reference-semantics/semantics/float.k:246-246` (attributes: none)

```k
0246:   rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

### rule `reference-semantics/semantics/float.k:247-248` (attributes: none)

```k
0247:   rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
0248:        requires isFloat(V)
```

### syntax `reference-semantics/semantics/float.k:250-250` (attributes: none)

```k
0250:   syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

### rule `reference-semantics/semantics/float.k:251-251` (attributes: none)

```k
0251:   rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

### rule `reference-semantics/semantics/float.k:252-252` (attributes: none)

```k
0252:   rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

### rule `reference-semantics/semantics/float.k:253-253` (attributes: none)

```k
0253:   rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

### rule `reference-semantics/semantics/float.k:254-255` (attributes: none)

```k
0254:   rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
0255:        requires isFloat(V)
```

### syntax `reference-semantics/semantics/float.k:261-261` (attributes: none)

```k
0261:   syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

### rule `reference-semantics/semantics/float.k:262-264` (attributes: none)

```k
0262:   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
0263:         => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
0264:        requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

### rule `reference-semantics/semantics/float.k:265-265` (attributes: none)

```k
0265:   rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

### rule `reference-semantics/semantics/float.k:266-266` (attributes: none)

```k
0266:   rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

### rule `reference-semantics/semantics/float.k:267-269` (attributes: none)

```k
0267:   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
0268:         => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
0269:        requires isFloat(V)
```

### rule `reference-semantics/semantics/float.k:270-272` (attributes: none)

```k
0270:   rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
0271:         => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
0272:        requires isInt(V) orBool isBool(V)
```

### endmodule `reference-semantics/semantics/float.k:273-273` (attributes: none)

```k
0273: endmodule
```

## `reference-semantics/semantics/functions.k`

- SHA-256: `e4c8f67741117b29703c3c61d48a5b0f92cf7bd531e78e25c03e794a910ac193`; source lines: 91; declaration blocks: 22
- Kinds: `endmodule`=1, `imports`=1, `module`=1, `rule`=15, `syntax`=4

### module `reference-semantics/semantics/functions.k:3-3` (attributes: none)

```k
0003: module MPY-FUNCTIONS
```

### imports `reference-semantics/semantics/functions.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### syntax `reference-semantics/semantics/functions.k:8-11` (attributes: none)

```k
0008:   syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
0009:                  | #bindP(ParamNames, Vals)
0010:                  | "#pop"
0011:                  | "#endcall"
```

### rule `reference-semantics/semantics/functions.k:14-16` (attributes: none)

```k
0014:   rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
0015:        <env> L:Int </env>
0016:        <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

### syntax `reference-semantics/semantics/functions.k:18-18` (attributes: none)

```k
0018:   syntax Expr ::= closureExpr(ParamNames, Stmts)
```

### rule `reference-semantics/semantics/functions.k:19-20` (attributes: none)

```k
0019:   rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
0020:        <env> L:Int </env>
```

### syntax `reference-semantics/semantics/functions.k:27-27` (attributes: none)

```k
0027:   syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

### syntax `reference-semantics/semantics/functions.k:31-32` (attributes: none)

```k
0031:   syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
0032:                  | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

### rule `reference-semantics/semantics/functions.k:33-35` (attributes: none)

```k
0033:   rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
0034:                    FreeVars(FVS:ParamNames), BODY:Stmts)
0035:         => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

### rule `reference-semantics/semantics/functions.k:36-41` (attributes: none)

```k
0036:   rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
0037:                       (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
0038:         => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
0039:        <env> L:Int </env>
0040:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0041:        requires FV in_keys(M)
```

### rule `reference-semantics/semantics/functions.k:42-45` (attributes: none)

```k
0042:   rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
0043:                       .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
0044:        <env> L:Int </env>
0045:        <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

### rule `reference-semantics/semantics/functions.k:47-49` (attributes: none)

```k
0047:   rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
0048:         => closureVal(PNS, Return(E) .Stmts, L) ... </k>
0049:        <env> L:Int </env>
```

### rule `reference-semantics/semantics/functions.k:50-52` (attributes: none)

```k
0050:   rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
0051:                   FreeVars(FVS:ParamNames), E:Expr)
0052:         => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

### rule `reference-semantics/semantics/functions.k:53-58` (attributes: none)

```k
0053:   rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
0054:                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
0055:         => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
0056:        <env> L:Int </env>
0057:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0058:        requires FV in_keys(M)
```

### rule `reference-semantics/semantics/functions.k:59-60` (attributes: none)

```k
0059:   rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
0060:         => closureValC(PNS, CVS, BODY, CM) ... </k>
```

### rule `reference-semantics/semantics/functions.k:63-63` (attributes: none)

```k
0063:   rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

### rule `reference-semantics/semantics/functions.k:64-66` (attributes: none)

```k
0064:   rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
0065:        <env> L:Int </env>
0066:        <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

### rule `reference-semantics/semantics/functions.k:68-75` (attributes: priority)

```k
0068:   rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
0069:         => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
0070:        <env> L:Int </env>
0071:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0072:        requires "$cells" in_keys(M)
0073:         andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
0074:         andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
0075:        [priority(40)]
```

### rule `reference-semantics/semantics/functions.k:78-79` (attributes: none)

```k
0078:   rule <k> Return(V:Val) ~> _ => #pop </k>
0079:        <ret> noRet => retV(V) </ret>
```

### rule `reference-semantics/semantics/functions.k:80-81` (attributes: none)

```k
0080:   rule <k> #endcall => #pop ... </k>
0081:        <ret> noRet => retV(noneV) </ret>
```

### rule `reference-semantics/semantics/functions.k:85-90` (attributes: none)

```k
0085:   rule <k> #pop => V ~> CONT </k>
0086:        <ret>   retV(V) => noRet </ret>
0087:        <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
0088:        <env>   L:Int => CALLERL </env>
0089:        <scopes> SC:Map => SC [ L <- undef ] </scopes>
0090:        <scopeLoc> _ => SAVEDL </scopeLoc>
```

### endmodule `reference-semantics/semantics/functions.k:91-91` (attributes: none)

```k
0091: endmodule
```

## `reference-semantics/semantics/int.k`

- SHA-256: `dc2da7d81578370651ecb6905b69cb44443cdd8db3869441242b81420382abe5`; source lines: 28; declaration blocks: 20
- Kinds: `endmodule`=1, `imports`=1, `module`=1, `rule`=16, `syntax`=1

### module `reference-semantics/semantics/int.k:4-4` (attributes: none)

```k
0004: module MPY-INT
```

### imports `reference-semantics/semantics/int.k:5-5` (attributes: none)

```k
0005:   imports MPY-CORE
```

### rule `reference-semantics/semantics/int.k:7-7` (attributes: none)

```k
0007:   rule applyUn("-", I:Int) => 0 -Int I
```

### rule `reference-semantics/semantics/int.k:9-9` (attributes: none)

```k
0009:   rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

### rule `reference-semantics/semantics/int.k:11-11` (attributes: none)

```k
0011:   rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

### rule `reference-semantics/semantics/int.k:12-12` (attributes: none)

```k
0012:   rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

### rule `reference-semantics/semantics/int.k:13-13` (attributes: none)

```k
0013:   rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

### rule `reference-semantics/semantics/int.k:14-14` (attributes: none)

```k
0014:   rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

### rule `reference-semantics/semantics/int.k:15-15` (attributes: none)

```k
0015:   rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

### rule `reference-semantics/semantics/int.k:16-16` (attributes: none)

```k
0016:   rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

### rule `reference-semantics/semantics/int.k:17-17` (attributes: none)

```k
0017:   rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

### syntax `reference-semantics/semantics/int.k:19-19` (attributes: function)

```k
0019:   syntax Int ::= pyMod(Int, Int) [function]
```

### rule `reference-semantics/semantics/int.k:20-20` (attributes: none)

```k
0020:   rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

### rule `reference-semantics/semantics/int.k:22-22` (attributes: none)

```k
0022:   rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

### rule `reference-semantics/semantics/int.k:23-23` (attributes: none)

```k
0023:   rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

### rule `reference-semantics/semantics/int.k:24-24` (attributes: none)

```k
0024:   rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

### rule `reference-semantics/semantics/int.k:25-25` (attributes: none)

```k
0025:   rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

### rule `reference-semantics/semantics/int.k:26-26` (attributes: none)

```k
0026:   rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

### rule `reference-semantics/semantics/int.k:27-27` (attributes: none)

```k
0027:   rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

### endmodule `reference-semantics/semantics/int.k:28-28` (attributes: none)

```k
0028: endmodule
```

## `reference-semantics/semantics/iter.k`

- SHA-256: `5085db2fed67b7bbd39f6289ec275905aaee742690895d7b3f843f73bd62f77f`; source lines: 9; declaration blocks: 4
- Kinds: `endmodule`=1, `imports`=1, `module`=1, `syntax`=1

### module `reference-semantics/semantics/iter.k:6-6` (attributes: none)

```k
0006: module MPY-ITER
```

### imports `reference-semantics/semantics/iter.k:7-7` (attributes: none)

```k
0007:   imports MPY-CORE
```

### syntax `reference-semantics/semantics/iter.k:8-8` (attributes: none)

```k
0008:   syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

### endmodule `reference-semantics/semantics/iter.k:9-9` (attributes: none)

```k
0009: endmodule
```

## `reference-semantics/semantics/list.k`

- SHA-256: `870c72341c25e2c16283726191a71bf5b571ed2995c8ae12e3e2923cdce5a9aa`; source lines: 68; declaration blocks: 37
- Kinds: `endmodule`=1, `imports`=3, `module`=1, `rule`=27, `syntax`=5

### module `reference-semantics/semantics/list.k:3-3` (attributes: none)

```k
0003: module MPY-LIST
```

### imports `reference-semantics/semantics/list.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/list.k:5-5` (attributes: none)

```k
0005:   imports MPY-ITER
```

### imports `reference-semantics/semantics/list.k:6-6` (attributes: none)

```k
0006:   imports MPY-OPERATORS
```

### rule `reference-semantics/semantics/list.k:9-9` (attributes: none)

```k
0009:   rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

### rule `reference-semantics/semantics/list.k:10-10` (attributes: none)

```k
0010:   rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

### syntax `reference-semantics/semantics/list.k:13-13` (attributes: none)

```k
0013:   syntax ApplyK ::= "toList"
```

### rule `reference-semantics/semantics/list.k:14-14` (attributes: none)

```k
0014:   rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

### rule `reference-semantics/semantics/list.k:15-15` (attributes: none)

```k
0015:   rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

### syntax `reference-semantics/semantics/list.k:18-18` (attributes: function, total)

```k
0018:   syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

### rule `reference-semantics/semantics/list.k:19-19` (attributes: none)

```k
0019:   rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

### rule `reference-semantics/semantics/list.k:20-20` (attributes: none)

```k
0020:   rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

### rule `reference-semantics/semantics/list.k:24-25` (attributes: priority)

```k
0024:   rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
0025:        [priority(45)]
```

### rule `reference-semantics/semantics/list.k:27-27` (attributes: none)

```k
0027:   rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

### rule `reference-semantics/semantics/list.k:28-28` (attributes: none)

```k
0028:   rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

### syntax `reference-semantics/semantics/list.k:33-33` (attributes: function, total)

```k
0033:   syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

### rule `reference-semantics/semantics/list.k:34-34` (attributes: none)

```k
0034:   rule hasRefVS(.ValSeq)                => false
```

### rule `reference-semantics/semantics/list.k:35-35` (attributes: none)

```k
0035:   rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

### syntax `reference-semantics/semantics/list.k:37-38` (attributes: function, function)

```k
0037:   syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
0038:                 | deepEqV(Val, Val, Map)        [function]
```

### rule `reference-semantics/semantics/list.k:39-39` (attributes: none)

```k
0039:   rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

### rule `reference-semantics/semantics/list.k:40-40` (attributes: none)

```k
0040:   rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

### rule `reference-semantics/semantics/list.k:41-41` (attributes: none)

```k
0041:   rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

### rule `reference-semantics/semantics/list.k:42-43` (attributes: none)

```k
0042:   rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
0043:     => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

### rule `reference-semantics/semantics/list.k:45-46` (attributes: none)

```k
0045:   rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
0046:        requires H in_keys(HP)
```

### rule `reference-semantics/semantics/list.k:47-48` (attributes: none)

```k
0047:   rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
0048:        requires notBool isRefV(A) andBool H in_keys(HP)
```

### rule `reference-semantics/semantics/list.k:49-49` (attributes: none)

```k
0049:   rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

### rule `reference-semantics/semantics/list.k:50-50` (attributes: owise)

```k
0050:   rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

### rule `reference-semantics/semantics/list.k:53-55` (attributes: priority)

```k
0053:   rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
0054:        <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
0055:        [priority(40)]
```

### syntax `reference-semantics/semantics/list.k:58-58` (attributes: none)

```k
0058:   syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

### rule `reference-semantics/semantics/list.k:59-59` (attributes: none)

```k
0059:   rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

### rule `reference-semantics/semantics/list.k:60-60` (attributes: none)

```k
0060:   rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

### rule `reference-semantics/semantics/list.k:61-61` (attributes: none)

```k
0061:   rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

### rule `reference-semantics/semantics/list.k:62-62` (attributes: none)

```k
0062:   rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

### rule `reference-semantics/semantics/list.k:63-64` (attributes: none)

```k
0063:   rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
0064:        requires E ==K V
```

### rule `reference-semantics/semantics/list.k:65-66` (attributes: none)

```k
0065:   rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
0066:        requires notBool (E ==K V)
```

### rule `reference-semantics/semantics/list.k:67-67` (attributes: none)

```k
0067:   rule <k> B:Bool ~> #notB => notBool B ... </k>
```

### endmodule `reference-semantics/semantics/list.k:68-68` (attributes: none)

```k
0068: endmodule
```

## `reference-semantics/semantics/methods.k`

- SHA-256: `ff9acc6dab2d1cc99ec4f2d234f27ae4526d752aae62bcfd7f9fd2a0399f7743`; source lines: 170; declaration blocks: 108
- Kinds: `endmodule`=1, `imports`=4, `module`=1, `rule`=75, `syntax`=27

### module `reference-semantics/semantics/methods.k:3-3` (attributes: none)

```k
0003: module MPY-METHODS
```

### imports `reference-semantics/semantics/methods.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/methods.k:5-5` (attributes: none)

```k
0005:   imports K-EQUAL
```

### imports `reference-semantics/semantics/methods.k:6-6` (attributes: none)

```k
0006:   imports MPY-STR
```

### imports `reference-semantics/semantics/methods.k:7-7` (attributes: none)

```k
0007:   imports MPY-LIST
```

### syntax `reference-semantics/semantics/methods.k:10-10` (attributes: function)

```k
0010:   syntax Val ::= applyMethod(Val, String, Vals) [function]
```

### rule `reference-semantics/semantics/methods.k:13-13` (attributes: none)

```k
0013:   rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

### rule `reference-semantics/semantics/methods.k:14-14` (attributes: none)

```k
0014:   rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

### rule `reference-semantics/semantics/methods.k:15-15` (attributes: none)

```k
0015:   rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

### rule `reference-semantics/semantics/methods.k:16-16` (attributes: none)

```k
0016:   rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

### rule `reference-semantics/semantics/methods.k:19-19` (attributes: none)

```k
0019:   rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

### rule `reference-semantics/semantics/methods.k:20-20` (attributes: none)

```k
0020:   rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

### rule `reference-semantics/semantics/methods.k:21-21` (attributes: none)

```k
0021:   rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

### rule `reference-semantics/semantics/methods.k:26-26` (attributes: none)

```k
0026:   rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

### syntax `reference-semantics/semantics/methods.k:27-27` (attributes: function, total)

```k
0027:   syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:28-28` (attributes: none)

```k
0028:   rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

### rule `reference-semantics/semantics/methods.k:29-29` (attributes: none)

```k
0029:   rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

### rule `reference-semantics/semantics/methods.k:30-31` (attributes: none)

```k
0030:   rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
0031:     => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

### rule `reference-semantics/semantics/methods.k:34-34` (attributes: none)

```k
0034:   rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

### syntax `reference-semantics/semantics/methods.k:35-35` (attributes: function)

```k
0035:   syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

### rule `reference-semantics/semantics/methods.k:36-36` (attributes: none)

```k
0036:   rule cntSub(.IntSeq, _:IntSeq) => 0
```

### rule `reference-semantics/semantics/methods.k:37-38` (attributes: none)

```k
0037:   rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
0038:        requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

### rule `reference-semantics/semantics/methods.k:39-40` (attributes: none)

```k
0039:   rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
0040:        requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

### syntax `reference-semantics/semantics/methods.k:41-41` (attributes: function, total)

```k
0041:   syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:42-42` (attributes: none)

```k
0042:   rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

### rule `reference-semantics/semantics/methods.k:43-43` (attributes: owise)

```k
0043:   rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

### rule `reference-semantics/semantics/methods.k:44-44` (attributes: none)

```k
0044:   rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

### rule `reference-semantics/semantics/methods.k:47-47` (attributes: none)

```k
0047:   rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

### syntax `reference-semantics/semantics/methods.k:48-48` (attributes: function, total)

```k
0048:   syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:49-49` (attributes: none)

```k
0049:   rule trimWS(.IntSeq) => .IntSeq
```

### rule `reference-semantics/semantics/methods.k:50-50` (attributes: none)

```k
0050:   rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

### rule `reference-semantics/semantics/methods.k:51-51` (attributes: none)

```k
0051:   rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

### syntax `reference-semantics/semantics/methods.k:52-52` (attributes: function, total, function, total)

```k
0052:   syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:53-53` (attributes: none)

```k
0053:   rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

### rule `reference-semantics/semantics/methods.k:54-54` (attributes: none)

```k
0054:   rule revISAcc(.IntSeq, A:IntSeq) => A
```

### rule `reference-semantics/semantics/methods.k:55-55` (attributes: none)

```k
0055:   rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

### rule `reference-semantics/semantics/methods.k:58-58` (attributes: none)

```k
0058:   rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

### rule `reference-semantics/semantics/methods.k:61-61` (attributes: none)

```k
0061:   rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

### rule `reference-semantics/semantics/methods.k:64-64` (attributes: none)

```k
0064:   rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

### syntax `reference-semantics/semantics/methods.k:65-65` (attributes: function, total)

```k
0065:   syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

### rule `reference-semantics/semantics/methods.k:66-66` (attributes: none)

```k
0066:   rule cntOccVS(.ValSeq, _:Val)                => 0
```

### rule `reference-semantics/semantics/methods.k:67-67` (attributes: none)

```k
0067:   rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

### rule `reference-semantics/semantics/methods.k:68-68` (attributes: none)

```k
0068:   rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

### rule `reference-semantics/semantics/methods.k:72-74` (attributes: priority)

```k
0072:   rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
0073:         => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
0074:        [priority(40)]
```

### syntax `reference-semantics/semantics/methods.k:75-75` (attributes: function)

```k
0075:   syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

### rule `reference-semantics/semantics/methods.k:76-76` (attributes: none)

```k
0076:   rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

### rule `reference-semantics/semantics/methods.k:77-78` (attributes: none)

```k
0077:   rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
0078:        requires isWSC(C)
```

### rule `reference-semantics/semantics/methods.k:79-80` (attributes: none)

```k
0079:   rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
0080:        requires notBool isWSC(C)
```

### syntax `reference-semantics/semantics/methods.k:82-82` (attributes: function)

```k
0082:   syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

### rule `reference-semantics/semantics/methods.k:83-83` (attributes: none)

```k
0083:   rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

### rule `reference-semantics/semantics/methods.k:84-84` (attributes: none)

```k
0084:   rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

### syntax `reference-semantics/semantics/methods.k:85-85` (attributes: function, total)

```k
0085:   syntax Bool ::= isWSC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:86-86` (attributes: none)

```k
0086:   rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

### rule `reference-semantics/semantics/methods.k:89-91` (attributes: priority)

```k
0089:   rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
0090:         => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
0091:        [priority(39)]
```

### rule `reference-semantics/semantics/methods.k:94-96` (attributes: priority)

```k
0094:   rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
0095:         => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
0096:        [priority(40)]
```

### syntax `reference-semantics/semantics/methods.k:97-97` (attributes: function)

```k
0097:   syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

### rule `reference-semantics/semantics/methods.k:98-98` (attributes: none)

```k
0098:   rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

### rule `reference-semantics/semantics/methods.k:99-100` (attributes: none)

```k
0099:   rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
0100:        requires C ==Int SEP
```

### rule `reference-semantics/semantics/methods.k:101-102` (attributes: none)

```k
0101:   rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
0102:        requires notBool (C ==Int SEP)
```

### rule `reference-semantics/semantics/methods.k:104-105` (attributes: none)

```k
0104:   rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
0105:     => str(replaceC(CS, A, B))
```

### syntax `reference-semantics/semantics/methods.k:106-106` (attributes: function, total)

```k
0106:   syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:107-107` (attributes: none)

```k
0107:   rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

### rule `reference-semantics/semantics/methods.k:108-108` (attributes: none)

```k
0108:   rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

### rule `reference-semantics/semantics/methods.k:109-109` (attributes: none)

```k
0109:   rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

### syntax `reference-semantics/semantics/methods.k:112-112` (attributes: function, total)

```k
0112:   syntax Bool ::= isUpperC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:113-113` (attributes: none)

```k
0113:   rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

### syntax `reference-semantics/semantics/methods.k:115-115` (attributes: function, total)

```k
0115:   syntax Bool ::= isLowerC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:116-116` (attributes: none)

```k
0116:   rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

### syntax `reference-semantics/semantics/methods.k:118-118` (attributes: function, total)

```k
0118:   syntax Bool ::= isAlphaC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:119-119` (attributes: none)

```k
0119:   rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

### syntax `reference-semantics/semantics/methods.k:121-121` (attributes: function, total)

```k
0121:   syntax Bool ::= isDigitC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:122-122` (attributes: none)

```k
0122:   rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

### syntax `reference-semantics/semantics/methods.k:124-124` (attributes: function, total)

```k
0124:   syntax Bool ::= hasUpper(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:125-125` (attributes: none)

```k
0125:   rule hasUpper(.IntSeq) => false
```

### rule `reference-semantics/semantics/methods.k:126-126` (attributes: none)

```k
0126:   rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

### syntax `reference-semantics/semantics/methods.k:128-128` (attributes: function, total)

```k
0128:   syntax Bool ::= hasLower(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:129-129` (attributes: none)

```k
0129:   rule hasLower(.IntSeq) => false
```

### rule `reference-semantics/semantics/methods.k:130-130` (attributes: none)

```k
0130:   rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

### syntax `reference-semantics/semantics/methods.k:132-132` (attributes: function, total)

```k
0132:   syntax Bool ::= allAlpha(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:133-133` (attributes: none)

```k
0133:   rule allAlpha(.IntSeq) => true
```

### rule `reference-semantics/semantics/methods.k:134-134` (attributes: none)

```k
0134:   rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

### syntax `reference-semantics/semantics/methods.k:136-136` (attributes: function, total)

```k
0136:   syntax Bool ::= allDigit(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:137-137` (attributes: none)

```k
0137:   rule allDigit(.IntSeq) => true
```

### rule `reference-semantics/semantics/methods.k:138-138` (attributes: none)

```k
0138:   rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

### syntax `reference-semantics/semantics/methods.k:140-140` (attributes: function, total)

```k
0140:   syntax Int ::= lowerC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:142-142` (attributes: none)

```k
0142:   rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule `reference-semantics/semantics/methods.k:143-143` (attributes: owise)

```k
0143:   rule lowerC(C:Int) => C         [owise]
```

### syntax `reference-semantics/semantics/methods.k:145-145` (attributes: function, total)

```k
0145:   syntax Int ::= upperC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:146-146` (attributes: none)

```k
0146:   rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule `reference-semantics/semantics/methods.k:147-147` (attributes: owise)

```k
0147:   rule upperC(C:Int) => C         [owise]
```

### syntax `reference-semantics/semantics/methods.k:149-149` (attributes: function, total)

```k
0149:   syntax Int ::= swapC(Int) [function, total]
```

### rule `reference-semantics/semantics/methods.k:150-150` (attributes: none)

```k
0150:   rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

### rule `reference-semantics/semantics/methods.k:151-151` (attributes: none)

```k
0151:   rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

### rule `reference-semantics/semantics/methods.k:152-152` (attributes: owise)

```k
0152:   rule swapC(C:Int) => C         [owise]
```

### syntax `reference-semantics/semantics/methods.k:154-154` (attributes: function, total)

```k
0154:   syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:155-155` (attributes: none)

```k
0155:   rule mapLower(.IntSeq) => .IntSeq
```

### rule `reference-semantics/semantics/methods.k:156-156` (attributes: none)

```k
0156:   rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

### syntax `reference-semantics/semantics/methods.k:158-158` (attributes: function, total)

```k
0158:   syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:159-159` (attributes: none)

```k
0159:   rule mapUpper(.IntSeq) => .IntSeq
```

### rule `reference-semantics/semantics/methods.k:160-160` (attributes: none)

```k
0160:   rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

### syntax `reference-semantics/semantics/methods.k:162-162` (attributes: function, total)

```k
0162:   syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:163-163` (attributes: none)

```k
0163:   rule mapSwap(.IntSeq) => .IntSeq
```

### rule `reference-semantics/semantics/methods.k:164-164` (attributes: none)

```k
0164:   rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

### syntax `reference-semantics/semantics/methods.k:166-166` (attributes: function, total)

```k
0166:   syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/methods.k:167-167` (attributes: none)

```k
0167:   rule startsWith(.IntSeq, _:IntSeq)               => true
```

### rule `reference-semantics/semantics/methods.k:168-168` (attributes: none)

```k
0168:   rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule `reference-semantics/semantics/methods.k:169-169` (attributes: none)

```k
0169:   rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

### endmodule `reference-semantics/semantics/methods.k:170-170` (attributes: none)

```k
0170: endmodule
```

## `reference-semantics/semantics/operators.k`

- SHA-256: `f3d1fd85734f5e1757307e606cbfb8d6d4bf0893ee85ce20ec99606ade910e8b`; source lines: 47; declaration blocks: 16
- Kinds: `context`=2, `endmodule`=1, `imports`=2, `module`=1, `rule`=10

### module `reference-semantics/semantics/operators.k:6-6` (attributes: none)

```k
0006: module MPY-OPERATORS
```

### imports `reference-semantics/semantics/operators.k:7-7` (attributes: none)

```k
0007:   imports MPY-CORE
```

### imports `reference-semantics/semantics/operators.k:8-8` (attributes: none)

```k
0008:   imports MPY-ITER
```

### rule `reference-semantics/semantics/operators.k:10-10` (attributes: none)

```k
0010:   rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

### rule `reference-semantics/semantics/operators.k:12-12` (attributes: none)

```k
0012:   rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

### context `reference-semantics/semantics/operators.k:15-15` (attributes: none)

```k
0015:   context Compare(HOLE, _)
```

### context `reference-semantics/semantics/operators.k:16-16` (attributes: none)

```k
0016:   context Compare(_:Val, CmpOp(_, HOLE))
```

### rule `reference-semantics/semantics/operators.k:17-17` (attributes: owise)

```k
0017:   rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

### rule `reference-semantics/semantics/operators.k:19-19` (attributes: none)

```k
0019:   rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

### rule `reference-semantics/semantics/operators.k:20-20` (attributes: none)

```k
0020:   rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

### rule `reference-semantics/semantics/operators.k:25-27` (attributes: priority)

```k
0025:   rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
0026:        <heap> ... H |-> V:Val ... </heap>
0027:        [priority(40)]
```

### rule `reference-semantics/semantics/operators.k:28-31` (attributes: priority)

```k
0028:   rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
0029:        <heap> ... H |-> V:Val ... </heap>
0030:        requires notBool isRefV(L)
0031:        [priority(40)]
```

### rule `reference-semantics/semantics/operators.k:34-37` (attributes: priority)

```k
0034:   rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
0035:        <heap> ... H |-> V:Val ... </heap>
0036:        requires OP =/=String "in" andBool OP =/=String "not in"
0037:        [priority(40)]
```

### rule `reference-semantics/semantics/operators.k:38-42` (attributes: priority)

```k
0038:   rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
0039:        <heap> ... H |-> V:Val ... </heap>
0040:        requires notBool isRefV(L)
0041:         orBool OP ==String "in" orBool OP ==String "not in"
0042:        [priority(40)]
```

### rule `reference-semantics/semantics/operators.k:44-46` (attributes: priority)

```k
0044:   rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
0045:        <heap> ... H |-> V:Val ... </heap>
0046:        [priority(40)]
```

### endmodule `reference-semantics/semantics/operators.k:47-47` (attributes: none)

```k
0047: endmodule
```

## `reference-semantics/semantics/range.k`

- SHA-256: `810e4c04b757445c03592aef25c97d6b2cc7c6fffa646288bc6cd15a3cae643d`; source lines: 25; declaration blocks: 12
- Kinds: `endmodule`=1, `imports`=2, `module`=1, `rule`=6, `syntax`=2

### module `reference-semantics/semantics/range.k:5-5` (attributes: none)

```k
0005: module MPY-RANGE
```

### imports `reference-semantics/semantics/range.k:6-6` (attributes: none)

```k
0006:   imports MPY-CORE
```

### imports `reference-semantics/semantics/range.k:7-7` (attributes: none)

```k
0007:   imports MPY-ITER
```

### syntax `reference-semantics/semantics/range.k:9-9` (attributes: function, total)

```k
0009:   syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

### rule `reference-semantics/semantics/range.k:10-10` (attributes: none)

```k
0010:   rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

### syntax `reference-semantics/semantics/range.k:12-12` (attributes: function)

```k
0012:   syntax Int ::= rangeLen(Int, Int, Int) [function]
```

### rule `reference-semantics/semantics/range.k:13-14` (attributes: none)

```k
0013:   rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
0014:        requires ST >Int 0 andBool HI >Int LO
```

### rule `reference-semantics/semantics/range.k:15-16` (attributes: none)

```k
0015:   rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
0016:        requires ST <Int 0 andBool HI <Int LO
```

### rule `reference-semantics/semantics/range.k:17-18` (attributes: none)

```k
0017:   rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
0018:        requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

### rule `reference-semantics/semantics/range.k:20-22` (attributes: none)

```k
0020:   rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
0021:         => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
0022:        requires inRange(I, HI, ST)
```

### rule `reference-semantics/semantics/range.k:23-24` (attributes: none)

```k
0023:   rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
0024:        requires notBool inRange(I, HI, ST)
```

### endmodule `reference-semantics/semantics/range.k:25-25` (attributes: none)

```k
0025: endmodule
```

## `reference-semantics/semantics/set.k`

- SHA-256: `b822c3c6944f9940a4477fa6b7a42490c407663f2a314394e9c146e8951f1ac7`; source lines: 40; declaration blocks: 21
- Kinds: `endmodule`=1, `imports`=1, `module`=1, `rule`=12, `syntax`=6

### module `reference-semantics/semantics/set.k:3-3` (attributes: none)

```k
0003: module MPY-SET
```

### imports `reference-semantics/semantics/set.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### syntax `reference-semantics/semantics/set.k:8-8` (attributes: none)

```k
0008:   syntax Val ::= setV(IntSeq)
```

### syntax `reference-semantics/semantics/set.k:11-11` (attributes: function, total)

```k
0011:   syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/set.k:12-12` (attributes: none)

```k
0012:   rule codeIn(_:Int, .IntSeq)                => false
```

### rule `reference-semantics/semantics/set.k:13-13` (attributes: none)

```k
0013:   rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

### syntax `reference-semantics/semantics/set.k:16-17` (attributes: function, total, function, total)

```k
0016:   syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
0017:                   | dedupFrom(IntSeq, IntSeq)  [function, total]
```

### rule `reference-semantics/semantics/set.k:18-18` (attributes: none)

```k
0018:   rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

### rule `reference-semantics/semantics/set.k:19-19` (attributes: none)

```k
0019:   rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

### rule `reference-semantics/semantics/set.k:20-21` (attributes: none)

```k
0020:   rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
0021:        requires codeIn(C, ACC)
```

### rule `reference-semantics/semantics/set.k:22-23` (attributes: none)

```k
0022:   rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
0023:        requires notBool codeIn(C, ACC)
```

### syntax `reference-semantics/semantics/set.k:25-25` (attributes: function, total)

```k
0025:   syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/set.k:26-26` (attributes: none)

```k
0026:   rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

### rule `reference-semantics/semantics/set.k:27-27` (attributes: none)

```k
0027:   rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

### syntax `reference-semantics/semantics/set.k:31-31` (attributes: function, total)

```k
0031:   syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/set.k:32-32` (attributes: none)

```k
0032:   rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

### rule `reference-semantics/semantics/set.k:33-33` (attributes: none)

```k
0033:   rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

### syntax `reference-semantics/semantics/set.k:35-35` (attributes: function, total)

```k
0035:   syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/set.k:36-36` (attributes: none)

```k
0036:   rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

### rule `reference-semantics/semantics/set.k:39-39` (attributes: none)

```k
0039:   rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

### endmodule `reference-semantics/semantics/set.k:40-40` (attributes: none)

```k
0040: endmodule
```

## `reference-semantics/semantics/sort.k`

- SHA-256: `df79670e4794a92e96ffc824857fbc34d3a65b6b6a3026d1dcf322128fbaba5a`; source lines: 72; declaration blocks: 29
- Kinds: `endmodule`=1, `imports`=2, `module`=1, `rule`=19, `syntax`=6

### module `reference-semantics/semantics/sort.k:10-10` (attributes: none)

```k
0010: module MPY-SORT
```

### imports `reference-semantics/semantics/sort.k:11-11` (attributes: none)

```k
0011:   imports MPY-BUILTINS
```

### imports `reference-semantics/semantics/sort.k:12-12` (attributes: none)

```k
0012:   imports MPY-SUBSCRIPT
```

### syntax `reference-semantics/semantics/sort.k:18-18` (attributes: function, total, symbol, no-evaluators)

```k
0018:   syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

### syntax `reference-semantics/semantics/sort.k:19-19` (attributes: function)

```k
0019:   syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

### rule `reference-semantics/semantics/sort.k:20-20` (attributes: concrete)

```k
0020:   rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

### rule `reference-semantics/semantics/sort.k:21-21` (attributes: concrete)

```k
0021:   rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

### rule `reference-semantics/semantics/sort.k:22-22` (attributes: concrete)

```k
0022:   rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

### rule `reference-semantics/semantics/sort.k:23-23` (attributes: concrete)

```k
0023:   rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

### rule `reference-semantics/semantics/sort.k:24-24` (attributes: concrete)

```k
0024:   rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

### syntax `reference-semantics/semantics/sort.k:26-26` (attributes: function)

```k
0026:   syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

### rule `reference-semantics/semantics/sort.k:27-27` (attributes: concrete)

```k
0027:   rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

### rule `reference-semantics/semantics/sort.k:28-28` (attributes: concrete)

```k
0028:   rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

### rule `reference-semantics/semantics/sort.k:29-30` (attributes: concrete)

```k
0029:   rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
0030:        requires strLt(A, B) orBool A ==K B [concrete]
```

### rule `reference-semantics/semantics/sort.k:31-32` (attributes: concrete)

```k
0031:   rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
0032:        requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

### rule `reference-semantics/semantics/sort.k:36-37` (attributes: none)

```k
0036:   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
0037:         => #alloc(list(sortVS(VS))) ... </k>
```

### rule `reference-semantics/semantics/sort.k:40-42` (attributes: priority)

```k
0040:   rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
0041:        <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
0042:        [priority(40)]
```

### syntax `reference-semantics/semantics/sort.k:49-49` (attributes: function, total, symbol, no-evaluators)

```k
0049:   syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

### syntax `reference-semantics/semantics/sort.k:51-52` (attributes: function, total, function, total)

```k
0051:   syntax ValSeq ::= revVS(ValSeq) [function, total]
0052:                   | revVSAcc(ValSeq, ValSeq) [function, total]
```

### rule `reference-semantics/semantics/sort.k:53-53` (attributes: none)

```k
0053:   rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

### rule `reference-semantics/semantics/sort.k:54-54` (attributes: none)

```k
0054:   rule revVSAcc(.ValSeq, A:ValSeq) => A
```

### rule `reference-semantics/semantics/sort.k:55-55` (attributes: none)

```k
0055:   rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

### syntax `reference-semantics/semantics/sort.k:57-57` (attributes: function, total)

```k
0057:   syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

### rule `reference-semantics/semantics/sort.k:58-58` (attributes: none)

```k
0058:   rule condRev(S:ValSeq, false) => S
```

### rule `reference-semantics/semantics/sort.k:59-59` (attributes: none)

```k
0059:   rule condRev(S:ValSeq, true)  => revVS(S)
```

### rule `reference-semantics/semantics/sort.k:61-62` (attributes: none)

```k
0061:   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
0062:         => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

### rule `reference-semantics/semantics/sort.k:63-64` (attributes: none)

```k
0063:   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
0064:         => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

### rule `reference-semantics/semantics/sort.k:65-66` (attributes: none)

```k
0065:   rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
0066:         => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

### endmodule `reference-semantics/semantics/sort.k:72-72` (attributes: none)

```k
0072: endmodule
```

## `reference-semantics/semantics/str.k`

- SHA-256: `1bf0abf61d7c5df6301433a89c79d2ef4259d47a68d98385ff74618c4c310e0f`; source lines: 60; declaration blocks: 37
- Kinds: `endmodule`=1, `imports`=2, `module`=1, `rule`=28, `syntax`=5

### module `reference-semantics/semantics/str.k:3-3` (attributes: none)

```k
0003: module MPY-STR
```

### imports `reference-semantics/semantics/str.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/str.k:5-5` (attributes: none)

```k
0005:   imports MPY-ITER
```

### rule `reference-semantics/semantics/str.k:8-8` (attributes: none)

```k
0008:   rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

### rule `reference-semantics/semantics/str.k:9-10` (attributes: none)

```k
0009:   rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
0010:         => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

### syntax `reference-semantics/semantics/str.k:13-13` (attributes: function)

```k
0013:   syntax IntSeq ::= strToCodes(String) [function]
```

### rule `reference-semantics/semantics/str.k:14-14` (attributes: none)

```k
0014:   rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

### rule `reference-semantics/semantics/str.k:15-15` (attributes: none)

```k
0015:   rule strToCodes("") => .IntSeq
```

### rule `reference-semantics/semantics/str.k:16-17` (attributes: none)

```k
0016:   rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
0017:     requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

### syntax `reference-semantics/semantics/str.k:20-20` (attributes: function, total)

```k
0020:   syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/str.k:21-21` (attributes: none)

```k
0021:   rule seqConcat(.IntSeq, T:IntSeq)                => T
```

### rule `reference-semantics/semantics/str.k:22-22` (attributes: none)

```k
0022:   rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

### rule `reference-semantics/semantics/str.k:24-24` (attributes: none)

```k
0024:   rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

### rule `reference-semantics/semantics/str.k:25-25` (attributes: none)

```k
0025:   rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

### rule `reference-semantics/semantics/str.k:26-26` (attributes: none)

```k
0026:   rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

### rule `reference-semantics/semantics/str.k:29-29` (attributes: none)

```k
0029:   rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

### rule `reference-semantics/semantics/str.k:30-30` (attributes: none)

```k
0030:   rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

### syntax `reference-semantics/semantics/str.k:32-32` (attributes: function, total)

```k
0032:   syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/str.k:33-33` (attributes: none)

```k
0033:   rule strPrefix(.IntSeq, _:IntSeq)               => true
```

### rule `reference-semantics/semantics/str.k:34-34` (attributes: none)

```k
0034:   rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule `reference-semantics/semantics/str.k:35-35` (attributes: none)

```k
0035:   rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

### syntax `reference-semantics/semantics/str.k:37-37` (attributes: function, total)

```k
0037:   syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/str.k:38-38` (attributes: none)

```k
0038:   rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

### rule `reference-semantics/semantics/str.k:39-39` (attributes: none)

```k
0039:   rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

### rule `reference-semantics/semantics/str.k:40-41` (attributes: none)

```k
0040:   rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
0041:        requires notBool strPrefix(P, iCons(C, Xs))
```

### syntax `reference-semantics/semantics/str.k:48-48` (attributes: function, total)

```k
0048:   syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

### rule `reference-semantics/semantics/str.k:49-49` (attributes: none)

```k
0049:   rule strLt(.IntSeq, .IntSeq)                => false
```

### rule `reference-semantics/semantics/str.k:50-50` (attributes: none)

```k
0050:   rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

### rule `reference-semantics/semantics/str.k:51-51` (attributes: none)

```k
0051:   rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

### rule `reference-semantics/semantics/str.k:52-52` (attributes: none)

```k
0052:   rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

### rule `reference-semantics/semantics/str.k:53-53` (attributes: none)

```k
0053:   rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

### rule `reference-semantics/semantics/str.k:54-54` (attributes: none)

```k
0054:   rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

### rule `reference-semantics/semantics/str.k:56-56` (attributes: none)

```k
0056:   rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

### rule `reference-semantics/semantics/str.k:57-57` (attributes: none)

```k
0057:   rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

### rule `reference-semantics/semantics/str.k:58-58` (attributes: none)

```k
0058:   rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

### rule `reference-semantics/semantics/str.k:59-59` (attributes: none)

```k
0059:   rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

### endmodule `reference-semantics/semantics/str.k:60-60` (attributes: none)

```k
0060: endmodule
```

## `reference-semantics/semantics/subscript.k`

- SHA-256: `dba04c0acf213bef4f9f7b11243ca00a2b3ca5fa8666c544ede7d382d27d36a7`; source lines: 122; declaration blocks: 60
- Kinds: `context`=2, `endmodule`=1, `imports`=1, `module`=1, `rule`=40, `syntax`=15

### module `reference-semantics/semantics/subscript.k:3-3` (attributes: none)

```k
0003: module MPY-SUBSCRIPT
```

### imports `reference-semantics/semantics/subscript.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### syntax `reference-semantics/semantics/subscript.k:11-11` (attributes: function, total)

```k
0011:   syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

### rule `reference-semantics/semantics/subscript.k:12-12` (attributes: none)

```k
0012:   rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

### rule `reference-semantics/semantics/subscript.k:13-14` (attributes: none)

```k
0013:   rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
0014:        requires I >Int 0
```

### syntax `reference-semantics/semantics/subscript.k:16-16` (attributes: function)

```k
0016:   syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

### rule `reference-semantics/semantics/subscript.k:17-17` (attributes: none)

```k
0017:   rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

### rule `reference-semantics/semantics/subscript.k:18-19` (attributes: none)

```k
0018:   rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
0019:        requires I >Int 0
```

### syntax `reference-semantics/semantics/subscript.k:21-21` (attributes: function, total)

```k
0021:   syntax Int ::= normIdx(Int, Int) [function, total]
```

### rule `reference-semantics/semantics/subscript.k:22-22` (attributes: none)

```k
0022:   rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

### rule `reference-semantics/semantics/subscript.k:23-23` (attributes: none)

```k
0023:   rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

### context `reference-semantics/semantics/subscript.k:27-27` (attributes: none)

```k
0027:   context Subscript(HOLE, _)
```

### context `reference-semantics/semantics/subscript.k:28-28` (attributes: none)

```k
0028:   context Subscript(_:Val, HOLE:Expr)
```

### rule `reference-semantics/semantics/subscript.k:31-33` (attributes: priority)

```k
0031:   rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
0032:        <heap> ... H |-> V:Val ... </heap>
0033:        [priority(40)]
```

### rule `reference-semantics/semantics/subscript.k:35-35` (attributes: none)

```k
0035:   rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

### syntax `reference-semantics/semantics/subscript.k:37-37` (attributes: function)

```k
0037:   syntax Val ::= applyIndex(Val, Int) [function]
```

### rule `reference-semantics/semantics/subscript.k:38-38` (attributes: none)

```k
0038:   rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule `reference-semantics/semantics/subscript.k:39-39` (attributes: none)

```k
0039:   rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

### rule `reference-semantics/semantics/subscript.k:40-41` (attributes: none)

```k
0040:   rule applyIndex(str(IS:IntSeq),   I:Int)
0041:     => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

### syntax `reference-semantics/semantics/subscript.k:44-47` (attributes: none)

```k
0044:   syntax KItem ::= #evalB(Bound) | "#toSome"
0045:                  | #slLo(Val, Bound, Bound)
0046:                  | #slHi(Val, OptInt, Bound)
0047:                  | #slStep(Val, OptInt, OptInt)
```

### syntax `reference-semantics/semantics/subscript.k:49-49` (attributes: none)

```k
0049:   syntax OptInt ::= "noB" | someB(Int)
```

### rule `reference-semantics/semantics/subscript.k:50-50` (attributes: none)

```k
0050:   rule <k> #evalB(NoBound)  => noB ... </k>
```

### rule `reference-semantics/semantics/subscript.k:51-51` (attributes: none)

```k
0051:   rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

### rule `reference-semantics/semantics/subscript.k:52-52` (attributes: none)

```k
0052:   rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

### rule `reference-semantics/semantics/subscript.k:54-54` (attributes: none)

```k
0054:   rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

### rule `reference-semantics/semantics/subscript.k:55-55` (attributes: none)

```k
0055:   rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

### rule `reference-semantics/semantics/subscript.k:56-56` (attributes: none)

```k
0056:   rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

### rule `reference-semantics/semantics/subscript.k:58-60` (attributes: priority)

```k
0058:   rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
0059:         => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
0060:        [priority(45)]
```

### rule `reference-semantics/semantics/subscript.k:61-61` (attributes: none)

```k
0061:   rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

### syntax `reference-semantics/semantics/subscript.k:63-63` (attributes: function)

```k
0063:   syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

### rule `reference-semantics/semantics/subscript.k:64-65` (attributes: none)

```k
0064:   rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
0065:     => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule `reference-semantics/semantics/subscript.k:66-67` (attributes: none)

```k
0066:   rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
0067:     => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

### rule `reference-semantics/semantics/subscript.k:68-69` (attributes: none)

```k
0068:   rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
0069:     => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

### syntax `reference-semantics/semantics/subscript.k:72-72` (attributes: function, total)

```k
0072:   syntax Int ::= slStep(OptInt) [function, total]
```

### rule `reference-semantics/semantics/subscript.k:73-73` (attributes: none)

```k
0073:   rule slStep(noB)          => 1
```

### rule `reference-semantics/semantics/subscript.k:74-74` (attributes: none)

```k
0074:   rule slStep(someB(S:Int)) => S
```

### syntax `reference-semantics/semantics/subscript.k:76-76` (attributes: function)

```k
0076:   syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

### rule `reference-semantics/semantics/subscript.k:77-78` (attributes: none)

```k
0077:   rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
0078:        requires slStep(ST) >Int 0
```

### rule `reference-semantics/semantics/subscript.k:79-80` (attributes: none)

```k
0079:   rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
0080:        requires slStep(ST) <Int 0
```

### rule `reference-semantics/semantics/subscript.k:81-81` (attributes: none)

```k
0081:   rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax `reference-semantics/semantics/subscript.k:83-83` (attributes: function)

```k
0083:   syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

### rule `reference-semantics/semantics/subscript.k:84-85` (attributes: none)

```k
0084:   rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
0085:        requires slStep(ST) >Int 0
```

### rule `reference-semantics/semantics/subscript.k:86-87` (attributes: none)

```k
0086:   rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
0087:        requires slStep(ST) <Int 0
```

### rule `reference-semantics/semantics/subscript.k:88-88` (attributes: none)

```k
0088:   rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

### syntax `reference-semantics/semantics/subscript.k:90-90` (attributes: function, total)

```k
0090:   syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

### rule `reference-semantics/semantics/subscript.k:91-92` (attributes: none)

```k
0091:   rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
0092:        requires I  <Int 0
```

### rule `reference-semantics/semantics/subscript.k:93-94` (attributes: none)

```k
0093:   rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
0094:        requires I >=Int 0
```

### syntax `reference-semantics/semantics/subscript.k:96-96` (attributes: function, total)

```k
0096:   syntax Int ::= clampLo(Int, Int) [function, total]
```

### rule `reference-semantics/semantics/subscript.k:97-98` (attributes: none)

```k
0097:   rule clampLo(J:Int, _STEP:Int) => J
0098:        requires J >=Int 0
```

### rule `reference-semantics/semantics/subscript.k:99-100` (attributes: none)

```k
0099:   rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
0100:        requires J <Int 0
```

### syntax `reference-semantics/semantics/subscript.k:102-102` (attributes: function, total)

```k
0102:   syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

### rule `reference-semantics/semantics/subscript.k:103-104` (attributes: none)

```k
0103:   rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
0104:        requires I  <Int LEN
```

### rule `reference-semantics/semantics/subscript.k:105-106` (attributes: none)

```k
0105:   rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
0106:        requires I >=Int LEN
```

### syntax `reference-semantics/semantics/subscript.k:109-109` (attributes: function)

```k
0109:   syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

### rule `reference-semantics/semantics/subscript.k:110-112` (attributes: none)

```k
0110:   rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
0111:     => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
0112:        requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### rule `reference-semantics/semantics/subscript.k:113-114` (attributes: none)

```k
0113:   rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
0114:        requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### syntax `reference-semantics/semantics/subscript.k:116-116` (attributes: function)

```k
0116:   syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

### rule `reference-semantics/semantics/subscript.k:117-119` (attributes: none)

```k
0117:   rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
0118:     => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
0119:        requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

### rule `reference-semantics/semantics/subscript.k:120-121` (attributes: none)

```k
0120:   rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
0121:        requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

### endmodule `reference-semantics/semantics/subscript.k:122-122` (attributes: none)

```k
0122: endmodule
```

## `reference-semantics/semantics/syntax.k`

- SHA-256: `1e9e629e5e6e14bdd7f4d530375e8655a89366b5ecd0c24a3c57ad3b5708f2a6`; source lines: 62; declaration blocks: 22
- Kinds: `endmodule`=1, `imports`=4, `module`=1, `syntax`=16

### module `reference-semantics/semantics/syntax.k:3-3` (attributes: none)

```k
0003: module MPY-SYNTAX
```

### imports `reference-semantics/semantics/syntax.k:4-4` (attributes: none)

```k
0004:   imports INT-SYNTAX
```

### imports `reference-semantics/semantics/syntax.k:5-5` (attributes: none)

```k
0005:   imports FLOAT-SYNTAX
```

### imports `reference-semantics/semantics/syntax.k:6-6` (attributes: none)

```k
0006:   imports BOOL-SYNTAX
```

### imports `reference-semantics/semantics/syntax.k:7-7` (attributes: none)

```k
0007:   imports STRING-SYNTAX
```

### syntax `reference-semantics/semantics/syntax.k:9-30` (attributes: strict, seqstrict, macro, macro, strict, strict)

```k
0009:   syntax Expr ::= "Int"      "(" Int ")"
0010:                 | "Float"    "(" Float ")"
0011:                 | "Bool"     "(" Bool ")"
0012:                 | "Name"     "(" String ")"
0013:                 | "Str"      "(" String ")"
0014:                 | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
0015:                 | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
0016:                 | "BoolOp"    "(" String "," Exprs ")"
0017:                 | "ListExpr"  "(" Exprs ")"
0018:                 | "DictExpr"  "(" Entries ")"
0019:                 | "ListComp"  "(" Expr "," CompFors ")" [macro]
0020:                 | "GenExp"    "(" Expr "," CompFors ")" [macro]
0021:                 | "TupleExpr" "(" Exprs ")"
0022:                 | "Subscript" "(" Expr "," Index ")"
0023:                 | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
0024:                 | "Lambda"    "(" Params "," Expr ")"
0025:                 | "KwArg"     "(" String "," Expr ")"
0026:                 | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
0027:                 | "NoneVal"
0028:                 | "Call"      "(" Expr "," Exprs ")"
0029:                 | "Attribute" "(" Expr "," String ")" [strict(1)]
0030:                 | "Compare"   "(" Expr "," CmpOp ")"
```

### syntax `reference-semantics/semantics/syntax.k:32-32` (attributes: none)

```k
0032:   syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

### syntax `reference-semantics/semantics/syntax.k:33-33` (attributes: none)

```k
0033:   syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

### syntax `reference-semantics/semantics/syntax.k:34-34` (attributes: none)

```k
0034:   syntax Entries  ::= List{Entry, ","}
```

### syntax `reference-semantics/semantics/syntax.k:35-35` (attributes: none)

```k
0035:   syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

### syntax `reference-semantics/semantics/syntax.k:36-36` (attributes: none)

```k
0036:   syntax CompFors ::= List{CompFor, ""}
```

### syntax `reference-semantics/semantics/syntax.k:37-37` (attributes: none)

```k
0037:   syntax Exprs    ::= List{Expr, ","}
```

### syntax `reference-semantics/semantics/syntax.k:38-38` (attributes: none)

```k
0038:   syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

### syntax `reference-semantics/semantics/syntax.k:39-39` (attributes: none)

```k
0039:   syntax Bound    ::= Expr | "NoBound"
```

### syntax `reference-semantics/semantics/syntax.k:41-54` (attributes: strict, strict, strict, strict, strict, strict, strict)

```k
0041:   syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
0042:                 | "Import"    "(" String ")"
0043:                 | "ImportFrom" "(" String "," ParamNames ")"
0044:                 | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
0045:                 | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
0046:                 | "While"     "(" Expr "," Stmts ")"
0047:                 | "Break"
0048:                 | "Continue"
0049:                 | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
0050:                 | "Return"    "(" Expr ")" [strict]
0051:                 | "Assert"    "(" Expr ")" [strict]
0052:                 | "Expr"      "(" Expr ")" [strict]
0053:                 | "FuncDef"   "(" String "," Params "," Stmts ")"
0054:                 | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
```

### syntax `reference-semantics/semantics/syntax.k:56-56` (attributes: none)

```k
0056:   syntax Stmts      ::= List{Stmt, ""}
```

### syntax `reference-semantics/semantics/syntax.k:57-57` (attributes: none)

```k
0057:   syntax Params     ::= "Params" "(" ParamNames ")"
```

### syntax `reference-semantics/semantics/syntax.k:58-58` (attributes: none)

```k
0058:   syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

### syntax `reference-semantics/semantics/syntax.k:59-59` (attributes: none)

```k
0059:   syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

### syntax `reference-semantics/semantics/syntax.k:60-60` (attributes: none)

```k
0060:   syntax ParamNames ::= List{String, ","}
```

### syntax `reference-semantics/semantics/syntax.k:61-61` (attributes: none)

```k
0061:   syntax Module     ::= "Module" "(" Stmts ")"
```

### endmodule `reference-semantics/semantics/syntax.k:62-62` (attributes: none)

```k
0062: endmodule
```

## `reference-semantics/semantics/tuple.k`

- SHA-256: `41395a1ec6a58129c78facb15b44206907c54d79e86ea363ae68cb37bfc64abb`; source lines: 58; declaration blocks: 31
- Kinds: `endmodule`=1, `imports`=4, `module`=1, `rule`=21, `syntax`=4

### module `reference-semantics/semantics/tuple.k:3-3` (attributes: none)

```k
0003: module MPY-TUPLE
```

### imports `reference-semantics/semantics/tuple.k:4-4` (attributes: none)

```k
0004:   imports MPY-CORE
```

### imports `reference-semantics/semantics/tuple.k:5-5` (attributes: none)

```k
0005:   imports MPY-ITER
```

### imports `reference-semantics/semantics/tuple.k:6-6` (attributes: none)

```k
0006:   imports MPY-LIST
```

### imports `reference-semantics/semantics/tuple.k:7-7` (attributes: none)

```k
0007:   imports MPY-METHODS
```

### rule `reference-semantics/semantics/tuple.k:10-10` (attributes: none)

```k
0010:   rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

### rule `reference-semantics/semantics/tuple.k:11-11` (attributes: none)

```k
0011:   rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

### syntax `reference-semantics/semantics/tuple.k:14-14` (attributes: none)

```k
0014:   syntax ApplyK ::= "toTuple"
```

### rule `reference-semantics/semantics/tuple.k:15-15` (attributes: none)

```k
0015:   rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:16-16` (attributes: none)

```k
0016:   rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:18-18` (attributes: none)

```k
0018:   rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

### rule `reference-semantics/semantics/tuple.k:20-20` (attributes: none)

```k
0020:   rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:21-21` (attributes: none)

```k
0021:   rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

### rule `reference-semantics/semantics/tuple.k:23-23` (attributes: none)

```k
0023:   rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

### syntax `reference-semantics/semantics/tuple.k:24-24` (attributes: function)

```k
0024:   syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

### rule `reference-semantics/semantics/tuple.k:25-25` (attributes: none)

```k
0025:   rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

### rule `reference-semantics/semantics/tuple.k:26-27` (attributes: none)

```k
0026:   rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
0027:        requires notBool (A ==K V)
```

### rule `reference-semantics/semantics/tuple.k:28-28` (attributes: none)

```k
0028:   rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

### syntax `reference-semantics/semantics/tuple.k:31-31` (attributes: none)

```k
0031:   syntax KItem ::= #bindTgt(Expr, Val)
```

### rule `reference-semantics/semantics/tuple.k:32-34` (attributes: none)

```k
0032:   rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
0033:        <env> L:Int </env>
0034:        <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

### rule `reference-semantics/semantics/tuple.k:35-41` (attributes: priority)

```k
0035:   rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
0036:        <env> L:Int </env>
0037:        <scopes> ... L |-> scope(M:Map, _) ... </scopes>
0038:        requires "$cells" in_keys(M)
0039:         andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
0040:         andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
0041:        [priority(40)]
```

### rule `reference-semantics/semantics/tuple.k:42-42` (attributes: none)

```k
0042:   rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:43-43` (attributes: none)

```k
0043:   rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:44-46` (attributes: priority)

```k
0044:   rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
0045:        <heap> ... H |-> V:Val ... </heap>
0046:        [priority(40)]
```

### syntax `reference-semantics/semantics/tuple.k:49-49` (attributes: none)

```k
0049:   syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

### rule `reference-semantics/semantics/tuple.k:50-50` (attributes: none)

```k
0050:   rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:51-51` (attributes: none)

```k
0051:   rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:52-54` (attributes: priority)

```k
0052:   rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
0053:        <heap> ... H |-> V:Val ... </heap>
0054:        [priority(40)]
```

### rule `reference-semantics/semantics/tuple.k:55-56` (attributes: none)

```k
0055:   rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
0056:         => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

### rule `reference-semantics/semantics/tuple.k:57-57` (attributes: none)

```k
0057:   rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

### endmodule `reference-semantics/semantics/tuple.k:58-58` (attributes: none)

```k
0058: endmodule
```

## `reference-semantics/semantics.k`

- SHA-256: `57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97`; source lines: 90; declaration blocks: 50
- Kinds: `endmodule`=2, `imports`=23, `module`=2, `requires`=23

### requires `reference-semantics/semantics.k:34-34` (attributes: none)

```k
0034: requires "semantics/syntax.k"
```

### requires `reference-semantics/semantics.k:35-35` (attributes: none)

```k
0035: requires "semantics/core.k"
```

### requires `reference-semantics/semantics.k:36-36` (attributes: none)

```k
0036: requires "semantics/iter.k"
```

### requires `reference-semantics/semantics.k:37-37` (attributes: none)

```k
0037: requires "semantics/range.k"
```

### requires `reference-semantics/semantics.k:38-38` (attributes: none)

```k
0038: requires "semantics/operators.k"
```

### requires `reference-semantics/semantics.k:39-39` (attributes: none)

```k
0039: requires "semantics/int.k"
```

### requires `reference-semantics/semantics.k:40-40` (attributes: none)

```k
0040: requires "semantics/bool.k"
```

### requires `reference-semantics/semantics.k:41-41` (attributes: none)

```k
0041: requires "semantics/float.k"
```

### requires `reference-semantics/semantics.k:42-42` (attributes: none)

```k
0042: requires "semantics/str.k"
```

### requires `reference-semantics/semantics.k:43-43` (attributes: none)

```k
0043: requires "semantics/set.k"
```

### requires `reference-semantics/semantics.k:44-44` (attributes: none)

```k
0044: requires "semantics/list.k"
```

### requires `reference-semantics/semantics.k:45-45` (attributes: none)

```k
0045: requires "semantics/tuple.k"
```

### requires `reference-semantics/semantics.k:46-46` (attributes: none)

```k
0046: requires "semantics/subscript.k"
```

### requires `reference-semantics/semantics.k:47-47` (attributes: none)

```k
0047: requires "semantics/comprehension.k"
```

### requires `reference-semantics/semantics.k:48-48` (attributes: none)

```k
0048: requires "semantics/methods.k"
```

### requires `reference-semantics/semantics.k:49-49` (attributes: none)

```k
0049: requires "semantics/controls.k"
```

### requires `reference-semantics/semantics.k:50-50` (attributes: none)

```k
0050: requires "semantics/functions.k"
```

### requires `reference-semantics/semantics.k:51-51` (attributes: none)

```k
0051: requires "semantics/builtins.k"
```

### requires `reference-semantics/semantics.k:52-52` (attributes: none)

```k
0052: requires "semantics/call.k"
```

### requires `reference-semantics/semantics.k:53-53` (attributes: none)

```k
0053: requires "semantics/sort.k"
```

### requires `reference-semantics/semantics.k:54-54` (attributes: none)

```k
0054: requires "semantics/assert.k"
```

### requires `reference-semantics/semantics.k:55-55` (attributes: none)

```k
0055: requires "semantics/dict.k"
```

### requires `reference-semantics/semantics.k:56-56` (attributes: none)

```k
0056: requires "semantics/concrete.k"
```

### module `reference-semantics/semantics.k:58-58` (attributes: none)

```k
0058: module MPY
```

### imports `reference-semantics/semantics.k:59-59` (attributes: none)

```k
0059:   imports MPY-CORE
```

### imports `reference-semantics/semantics.k:60-60` (attributes: none)

```k
0060:   imports MPY-ITER
```

### imports `reference-semantics/semantics.k:61-61` (attributes: none)

```k
0061:   imports MPY-RANGE
```

### imports `reference-semantics/semantics.k:62-62` (attributes: none)

```k
0062:   imports MPY-OPERATORS
```

### imports `reference-semantics/semantics.k:63-63` (attributes: none)

```k
0063:   imports MPY-INT
```

### imports `reference-semantics/semantics.k:64-64` (attributes: none)

```k
0064:   imports MPY-BOOL
```

### imports `reference-semantics/semantics.k:65-65` (attributes: none)

```k
0065:   imports MPY-FLOAT
```

### imports `reference-semantics/semantics.k:66-66` (attributes: none)

```k
0066:   imports MPY-STR
```

### imports `reference-semantics/semantics.k:67-67` (attributes: none)

```k
0067:   imports MPY-SET
```

### imports `reference-semantics/semantics.k:68-68` (attributes: none)

```k
0068:   imports MPY-LIST
```

### imports `reference-semantics/semantics.k:69-69` (attributes: none)

```k
0069:   imports MPY-TUPLE
```

### imports `reference-semantics/semantics.k:70-70` (attributes: none)

```k
0070:   imports MPY-SUBSCRIPT
```

### imports `reference-semantics/semantics.k:71-71` (attributes: none)

```k
0071:   imports MPY-COMPREHENSION
```

### imports `reference-semantics/semantics.k:72-72` (attributes: none)

```k
0072:   imports MPY-METHODS
```

### imports `reference-semantics/semantics.k:73-73` (attributes: none)

```k
0073:   imports MPY-CONTROLS
```

### imports `reference-semantics/semantics.k:74-74` (attributes: none)

```k
0074:   imports MPY-FUNCTIONS
```

### imports `reference-semantics/semantics.k:75-75` (attributes: none)

```k
0075:   imports MPY-BUILTINS
```

### imports `reference-semantics/semantics.k:76-76` (attributes: none)

```k
0076:   imports MPY-CALL
```

### imports `reference-semantics/semantics.k:77-77` (attributes: none)

```k
0077:   imports MPY-SORT
```

### imports `reference-semantics/semantics.k:78-78` (attributes: none)

```k
0078:   imports MPY-ASSERT
```

### imports `reference-semantics/semantics.k:79-79` (attributes: none)

```k
0079:   imports MPY-DICT
```

### endmodule `reference-semantics/semantics.k:80-80` (attributes: none)

```k
0080: endmodule
```

### module `reference-semantics/semantics.k:87-87` (attributes: none)

```k
0087: module MPY-KRUN
```

### imports `reference-semantics/semantics.k:88-88` (attributes: none)

```k
0088:   imports MPY
```

### imports `reference-semantics/semantics.k:89-89` (attributes: none)

```k
0089:   imports MPY-CONCRETE
```

### endmodule `reference-semantics/semantics.k:90-90` (attributes: none)

```k
0090: endmodule
```

## `verification.k`

- SHA-256: `e1f5771d906a02579bf78f5f2feb0209deec45711a3f5a7ee0582a33a5916bf7`; source lines: 158; declaration blocks: 33
- Kinds: `endmodule`=2, `imports`=3, `module`=2, `requires`=1, `rule`=22, `syntax`=3

### requires `verification.k:1-1` (attributes: none)

```k
0001: requires "reference-semantics/semantics.k"
```

### module `verification.k:3-3` (attributes: none)

```k
0003: module VERIFICATION-SYNTAX
```

### imports `verification.k:4-4` (attributes: none)

```k
0004:   imports MPY-SYNTAX
```

### syntax `verification.k:6-6` (attributes: function, total)

```k
0006:   syntax Val ::= "antiClosure" [function, total]
```

### syntax `verification.k:7-12` (attributes: function, total, function, total, function, total, function, total, function, total, function, total)

```k
0007:   syntax IntSeq ::= innerWord(IntSeq, Bool, Int, IntSeq) [function, total]
0008:                   | finishWord(IntSeq, Bool, Int) [function, total]
0009:                   | insertCode(IntSeq, Int) [function, total]
0010:                   | scanResult(IntSeq, IntSeq, IntSeq) [function, total]
0011:                   | scanWord(IntSeq, IntSeq) [function, total]
0012:                   | antiShuffle(IntSeq) [function, total]
```

### syntax `verification.k:13-13` (attributes: function, total)

```k
0013:   syntax Bool ::= innerFlag(Bool, Int, IntSeq) [function, total]
```

### endmodule `verification.k:14-14` (attributes: none)

```k
0014: endmodule
```

### module `verification.k:16-16` (attributes: none)

```k
0016: module VERIFICATION
```

### imports `verification.k:17-17` (attributes: none)

```k
0017:   imports MPY
```

### imports `verification.k:18-18` (attributes: none)

```k
0018:   imports VERIFICATION-SYNTAX
```

### rule `verification.k:22-24` (attributes: simplification)

```k
0022:   rule strLt(iCons(A, .IntSeq), iCons(B, .IntSeq))
0023:     => A <Int B
0024:     [simplification]
```

### rule `verification.k:29-31` (attributes: priority)

```k
0029:   rule <k> #branch(B:Bool, T:Stmts, _E:Stmts) => T ... </k>
0030:     requires B
0031:     [priority(60)]
```

### rule `verification.k:32-34` (attributes: priority)

```k
0032:   rule <k> #branch(B:Bool, _T:Stmts, E:Stmts) => E ... </k>
0033:     requires notBool B
0034:     [priority(60)]
```

### rule `verification.k:38-77` (attributes: none)

```k
0038:   rule antiClosure
0039:     => closureVal(
0040:          "s", .ParamNames,
0041:          Assign(Name("result"), Str(""))
0042:          Assign(Name("word"), Str(""))
0043:          Assign(Name("character"), Str(""))
0044:          Assign(Name("existing"), Str(""))
0045:          Assign(Name("new_word"), Str(""))
0046:          Assign(Name("inserted"), Bool(false))
0047:          For(
0048:            Name("character"),
0049:            Name("s"),
0050:            If(
0051:              Compare(Name("character"), CmpOp("==", Str(" "))),
0052:              AugAssign(Name("result"), "+", Name("word"))
0053:              AugAssign(Name("result"), "+", Str(" "))
0054:              Assign(Name("word"), Str("")),
0055:              Assign(Name("new_word"), Str(""))
0056:              Assign(Name("inserted"), Bool(false))
0057:              For(
0058:                Name("existing"),
0059:                Name("word"),
0060:                If(
0061:                  Name("inserted"),
0062:                  AugAssign(Name("new_word"), "+", Name("existing")),
0063:                  If(
0064:                    Compare(Name("character"), CmpOp("<", Name("existing"))),
0065:                    AugAssign(Name("new_word"), "+", Name("character"))
0066:                    Assign(Name("inserted"), Bool(true)),
0067:                    .Stmts)
0068:                  AugAssign(Name("new_word"), "+", Name("existing"))))
0069:              If(
0070:                Name("inserted"),
0071:                Assign(Name("word"), Name("new_word")),
0072:                Assign(
0073:                  Name("word"),
0074:                  BinOp("+", Name("new_word"), Name("character"))))))
0075:          AugAssign(Name("result"), "+", Name("word"))
0076:          Return(Name("result")),
0077:          0)
```

### rule `verification.k:80-80` (attributes: simplification)

```k
0080:   rule innerWord(NW, _B, _C, .IntSeq) => NW [simplification]
```

### rule `verification.k:81-87` (attributes: simplification)

```k
0081:   rule innerWord(NW, true, C, iCons(E, R))
0082:     => innerWord(
0083:          seqConcat(NW, iCons(E, .IntSeq)),
0084:          true,
0085:          C,
0086:          R)
0087:     [simplification]
```

### rule `verification.k:88-97` (attributes: simplification)

```k
0088:   rule innerWord(NW, false, C, iCons(E, R))
0089:     => innerWord(
0090:          seqConcat(
0091:            seqConcat(NW, iCons(C, .IntSeq)),
0092:            iCons(E, .IntSeq)),
0093:          true,
0094:          C,
0095:          R)
0096:     requires C <Int E
0097:     [simplification]
```

### rule `verification.k:98-105` (attributes: simplification)

```k
0098:   rule innerWord(NW, false, C, iCons(E, R))
0099:     => innerWord(
0100:          seqConcat(NW, iCons(E, .IntSeq)),
0101:          false,
0102:          C,
0103:          R)
0104:     requires notBool (C <Int E)
0105:     [simplification]
```

### rule `verification.k:107-107` (attributes: simplification)

```k
0107:   rule innerFlag(B, _C, .IntSeq) => B [simplification]
```

### rule `verification.k:108-110` (attributes: simplification)

```k
0108:   rule innerFlag(true, C, iCons(_E, R))
0109:     => innerFlag(true, C, R)
0110:     [simplification]
```

### rule `verification.k:111-114` (attributes: simplification)

```k
0111:   rule innerFlag(false, C, iCons(E, R))
0112:     => innerFlag(true, C, R)
0113:     requires C <Int E
0114:     [simplification]
```

### rule `verification.k:115-118` (attributes: simplification)

```k
0115:   rule innerFlag(false, C, iCons(E, R))
0116:     => innerFlag(false, C, R)
0117:     requires notBool (C <Int E)
0118:     [simplification]
```

### rule `verification.k:120-120` (attributes: none)

```k
0120:   rule finishWord(NW, true, _C) => NW
```

### rule `verification.k:121-122` (attributes: none)

```k
0121:   rule finishWord(NW, false, C)
0122:     => seqConcat(NW, iCons(C, .IntSeq))
```

### rule `verification.k:124-128` (attributes: none)

```k
0124:   rule insertCode(W, C)
0125:     => finishWord(
0126:          innerWord(.IntSeq, false, C, W),
0127:          innerFlag(false, C, W),
0128:          C)
```

### rule `verification.k:131-131` (attributes: simplification)

```k
0131:   rule scanResult(A, _W, .IntSeq) => A [simplification]
```

### rule `verification.k:132-138` (attributes: simplification)

```k
0132:   rule scanResult(A, W, iCons(C, R))
0133:     => scanResult(
0134:          seqConcat(seqConcat(A, W), iCons(32, .IntSeq)),
0135:          .IntSeq,
0136:          R)
0137:     requires C ==Int 32
0138:     [simplification]
```

### rule `verification.k:139-142` (attributes: simplification)

```k
0139:   rule scanResult(A, W, iCons(C, R))
0140:     => scanResult(A, insertCode(W, C), R)
0141:     requires notBool (C ==Int 32)
0142:     [simplification]
```

### rule `verification.k:144-144` (attributes: simplification)

```k
0144:   rule scanWord(W, .IntSeq) => W [simplification]
```

### rule `verification.k:145-148` (attributes: simplification)

```k
0145:   rule scanWord(_W, iCons(C, R))
0146:     => scanWord(.IntSeq, R)
0147:     requires C ==Int 32
0148:     [simplification]
```

### rule `verification.k:149-152` (attributes: simplification)

```k
0149:   rule scanWord(W, iCons(C, R))
0150:     => scanWord(insertCode(W, C), R)
0151:     requires notBool (C ==Int 32)
0152:     [simplification]
```

### rule `verification.k:154-157` (attributes: none)

```k
0154:   rule antiShuffle(S)
0155:     => seqConcat(
0156:          scanResult(.IntSeq, .IntSeq, S),
0157:          scanWord(.IntSeq, S))
```

### endmodule `verification.k:158-158` (attributes: none)

```k
0158: endmodule
```

## `spec.k`

- SHA-256: `7ec6e2525ed6af0a3eb3a396113b8384d0d8e12b3f39c44fcfaf1b6f1417e748`; source lines: 157; declaration blocks: 7
- Kinds: `claim`=3, `endmodule`=1, `imports`=1, `module`=1, `requires`=1

### requires `spec.k:1-1` (attributes: none)

```k
0001: requires "verification.k"
```

### module `spec.k:3-3` (attributes: none)

```k
0003: module SPEC
```

### imports `spec.k:4-4` (attributes: none)

```k
0004:   imports VERIFICATION
```

### claim `spec.k:6-42` (attributes: none)

```k
0006:   claim [insertion-loop]:
0007:     <k>
0008:       #loop(
0009:         str(S:IntSeq),
0010:         Name("existing"),
0011:         If(
0012:           Name("inserted"),
0013:           AugAssign(Name("new_word"), "+", Name("existing")),
0014:           If(
0015:             Compare(Name("character"), CmpOp("<", Name("existing"))),
0016:             AugAssign(Name("new_word"), "+", Name("character"))
0017:             Assign(Name("inserted"), Bool(true)),
0018:             .Stmts)
0019:           AugAssign(Name("new_word"), "+", Name("existing"))))
0020:       => .K
0021:       ...
0022:     </k>
0023:     <env> 1 </env>
0024:     <scopes>
0025:       -1 |-> builtinsScope
0026:       0  |-> scope("anti_shuffle" |-> antiClosure, parent(-1))
0027:       1  |-> scope(
0028:               "s"         |-> str(INPUT:IntSeq)
0029:               "result"    |-> str(A:IntSeq)
0030:               "word"      |-> str(W:IntSeq)
0031:               "character" |-> str(iCons(C:Int, .IntSeq))
0032:               "existing"  |-> (EX:Val => ?EX:Val)
0033:               "new_word"  |-> (str(NW:IntSeq) => str(innerWord(NW, B, C, S)))
0034:               "inserted"  |-> (B:Bool => innerFlag(B, C, S)),
0035:               parent(0))
0036:     </scopes>
0037:     <scopeLoc> 2 </scopeLoc>
0038:     <heap> .Map </heap>
0039:     <heapLoc> 0 </heapLoc>
0040:     <stack> STACK:List </stack>
0041:     <ret> noRet </ret>
0042:     <exc> NoExc </exc>
```

### claim `spec.k:44-96` (attributes: none)

```k
0044:   claim [character-loop]:
0045:     <k>
0046:       #loop(
0047:         str(S:IntSeq),
0048:         Name("character"),
0049:         If(
0050:           Compare(Name("character"), CmpOp("==", Str(" "))),
0051:           AugAssign(Name("result"), "+", Name("word"))
0052:           AugAssign(Name("result"), "+", Str(" "))
0053:           Assign(Name("word"), Str("")),
0054:           Assign(Name("new_word"), Str(""))
0055:           Assign(Name("inserted"), Bool(false))
0056:           For(
0057:             Name("existing"),
0058:             Name("word"),
0059:             If(
0060:               Name("inserted"),
0061:               AugAssign(Name("new_word"), "+", Name("existing")),
0062:               If(
0063:                 Compare(Name("character"), CmpOp("<", Name("existing"))),
0064:                 AugAssign(Name("new_word"), "+", Name("character"))
0065:                 Assign(Name("inserted"), Bool(true)),
0066:                 .Stmts)
0067:               AugAssign(Name("new_word"), "+", Name("existing"))))
0068:           If(
0069:             Name("inserted"),
0070:             Assign(Name("word"), Name("new_word")),
0071:             Assign(
0072:               Name("word"),
0073:               BinOp("+", Name("new_word"), Name("character"))))))
0074:       => .K
0075:       ...
0076:     </k>
0077:     <env> 1 </env>
0078:     <scopes>
0079:       -1 |-> builtinsScope
0080:       0  |-> scope("anti_shuffle" |-> antiClosure, parent(-1))
0081:       1  |-> scope(
0082:               "s"         |-> str(INPUT:IntSeq)
0083:               "result"    |-> (str(A:IntSeq) => str(scanResult(A, W, S)))
0084:               "word"      |-> (str(W:IntSeq) => str(scanWord(W, S)))
0085:               "character" |-> (CH:Val => ?CH:Val)
0086:               "existing"  |-> (EX:Val => ?EX:Val)
0087:               "new_word"  |-> (str(NW:IntSeq) => ?NW:Val)
0088:               "inserted"  |-> (B:Bool => ?B:Bool),
0089:               parent(0))
0090:     </scopes>
0091:     <scopeLoc> 2 </scopeLoc>
0092:     <heap> .Map </heap>
0093:     <heapLoc> 0 </heapLoc>
0094:     <stack> STACK:List </stack>
0095:     <ret> noRet </ret>
0096:     <exc> NoExc </exc>
```

### claim `spec.k:98-156` (attributes: none)

```k
0098:   claim [anti-shuffle]:
0099:     <k>
0100:       #loadAll(
0101:         Module(
0102:           FuncDef(
0103:             "anti_shuffle",
0104:             Params("s"),
0105:             Assign(Name("result"), Str(""))
0106:             Assign(Name("word"), Str(""))
0107:             Assign(Name("character"), Str(""))
0108:             Assign(Name("existing"), Str(""))
0109:             Assign(Name("new_word"), Str(""))
0110:             Assign(Name("inserted"), Bool(false))
0111:             For(
0112:               Name("character"),
0113:               Name("s"),
0114:               If(
0115:                 Compare(Name("character"), CmpOp("==", Str(" "))),
0116:                 AugAssign(Name("result"), "+", Name("word"))
0117:                 AugAssign(Name("result"), "+", Str(" "))
0118:                 Assign(Name("word"), Str("")),
0119:                 Assign(Name("new_word"), Str(""))
0120:                 Assign(Name("inserted"), Bool(false))
0121:                 For(
0122:                   Name("existing"),
0123:                   Name("word"),
0124:                   If(
0125:                     Name("inserted"),
0126:                     AugAssign(Name("new_word"), "+", Name("existing")),
0127:                     If(
0128:                       Compare(Name("character"), CmpOp("<", Name("existing"))),
0129:                       AugAssign(Name("new_word"), "+", Name("character"))
0130:                       Assign(Name("inserted"), Bool(true)),
0131:                       .Stmts)
0132:                     AugAssign(Name("new_word"), "+", Name("existing"))))
0133:                 If(
0134:                   Name("inserted"),
0135:                   Assign(Name("word"), Name("new_word")),
0136:                   Assign(
0137:                     Name("word"),
0138:                     BinOp("+", Name("new_word"), Name("character"))))))
0139:             AugAssign(Name("result"), "+", Name("word"))
0140:             Return(Name("result")))))
0141:       ~> Call(Name("anti_shuffle"), str(S:IntSeq))
0142:       => str(antiShuffle(S))
0143:     </k>
0144:     <env> 0 </env>
0145:     <scopes>
0146:       -1 |-> builtinsScope
0147:       0  |-> (scope(.Map, parent(-1))
0148:               => scope("anti_shuffle" |-> antiClosure, parent(-1)))
0149:     </scopes>
0150:     <scopeLoc> 1 </scopeLoc>
0151:     <heap> .Map </heap>
0152:     <heapLoc> 0 </heapLoc>
0153:     <stack> .List </stack>
0154:     <ret> noRet </ret>
0155:     <exc> NoExc </exc>
0156:     <exit-code> 0 </exit-code>
```

### endmodule `spec.k:157-157` (attributes: none)

```k
0157: endmodule
```

