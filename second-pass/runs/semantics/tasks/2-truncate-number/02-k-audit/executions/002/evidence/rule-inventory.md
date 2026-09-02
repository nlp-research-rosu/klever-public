# Exhaustive K declaration and rule inventory

Source scope: supplied `reference-semantics/semantics.k`, every supplied
`reference-semantics/semantics/*.k` helper, `verification.k`, and `spec.k`.

Counts: claim=1, configuration=1, context=5, rule=696, syntax=228, total_items=931
Attribute/category counts: function=145, total=107, functional=0, symbol=25, no-evaluators=22, macro=5, macro-rec=1, priority=45, simplification=0, concrete=35, owise=26, strict=2, seqstrict=1, hook=0, operational=238, equation-or-macro=458

## reference-semantics/semantics/assert.k

0001. `rule` line 6; tags: operational; `rule <k> Assert(V:Val) => .K ... </k> requires truthy(V)`
0002. `rule` line 8; tags: operational; `rule <k> Assert(V:Val) ~> _ => .K </k> <exc> NoExc => AssertionError </exc> <exit-code> _ => 1 </exit-code> requires notBool truthy(V)`
0003. `rule` line 13; tags: priority, operational; `rule <k> Assert(ref(H:Int)) => Assert(V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
## reference-semantics/semantics/bool.k

0004. `rule` line 8; tags: equation-or-macro; `rule applyUn("not", V:Val) => notBool truthy(V)`
0005. `rule` line 10; tags: equation-or-macro; `rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2`
0006. `rule` line 11; tags: equation-or-macro; `rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2`
0007. `context` line 16; tags: none; `context BoolOp(_, (HOLE:Expr, _:Exprs))`
0008. `rule` line 17; tags: operational; `rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>`
0009. `rule` line 18; tags: operational; `rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> requires truthy(V)`
0010. `rule` line 20; tags: operational; `rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires notBool truthy(V)`
0011. `rule` line 22; tags: operational; `rule <k> BoolOp("or", (V:Val, _:Expr, _:Exprs)) => V ... </k> requires truthy(V)`
0012. `rule` line 24; tags: operational; `rule <k> BoolOp("or", (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> requires notBool truthy(V)`
0013. `rule` line 29; tags: priority, operational; `rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k> [priority(40)]`
0014. `rule` line 31; tags: priority, operational; `rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
0015. `rule` line 35; tags: priority, operational; `rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`
0016. `rule` line 39; tags: priority, operational; `rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k> <heap> ... H |-> V:Val ... </heap> requires truthy(V) [priority(40)]`
0017. `rule` line 43; tags: priority, operational; `rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool truthy(V) [priority(40)]`
## reference-semantics/semantics/builtins.k

0018. `syntax` line 17; tags: function; `syntax Val ::= applyBuiltin(String, Vals) [function]`
0019. `syntax` line 20; tags: function; `syntax Int ::= seqLen(Val) [function]`
0020. `rule` line 21; tags: equation-or-macro; `rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)`
0021. `rule` line 22; tags: equation-or-macro; `rule seqLen(list(VS:ValSeq)) => vsLen(VS)`
0022. `rule` line 23; tags: equation-or-macro; `rule seqLen(tuple(VS:ValSeq)) => vsLen(VS)`
0023. `rule` line 24; tags: equation-or-macro; `rule seqLen(str(IS:IntSeq)) => isLen(IS)`
0024. `rule` line 25; tags: equation-or-macro; `rule seqLen(setV(DS:IntSeq)) => isLen(DS)`
0025. `rule` line 26; tags: equation-or-macro; `rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)`
0026. `rule` line 32; tags: operational; `rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
0027. `rule` line 33; tags: operational; `rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>`
0028. `rule` line 34; tags: operational; `rule <k> #applyK(toCall(builtinV("list")), .Vals) => #alloc(list(.ValSeq)) ... </k>`
0029. `rule` line 35; tags: operational; `rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals)) => #alloc(list(charsOf(CS))) ... </k>`
0030. `syntax` line 36; tags: function, total; `syntax ValSeq ::= charsOf(IntSeq) [function, total]`
0031. `rule` line 37; tags: equation-or-macro; `rule charsOf(.IntSeq) => .ValSeq`
0032. `rule` line 38; tags: equation-or-macro; `rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))`
0033. `rule` line 41; tags: equation-or-macro; `rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))`
0034. `rule` line 44; tags: equation-or-macro; `rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)`
0035. `syntax` line 47; tags: none; `syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)`
0036. `rule` line 48; tags: operational; `rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>`
0037. `rule` line 49; tags: operational; `rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>`
0038. `rule` line 50; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAcc(R, ACC +Int intOf(V)) ... </k> requires isInt(V) orBool isBool(V)`
0039. `syntax` line 54; tags: function; `syntax Int ::= intOf(Val) [function]`
0040. `rule` line 55; tags: equation-or-macro; `rule intOf(I:Int) => I`
0041. `rule` line 56; tags: equation-or-macro; `rule intOf(B:Bool) => #if B #then 1 #else 0 #fi`
0042. `syntax` line 59; tags: none; `syntax KItem ::= #allAcc(Iterable) | "#allCont"`
0043. `rule` line 60; tags: operational; `rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>`
0044. `rule` line 61; tags: operational; `rule <k> #iterDone ~> #allCont => true ... </k>`
0045. `rule` line 62; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k> requires truthy(V)`
0046. `rule` line 64; tags: operational; `rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k> requires notBool truthy(V)`
0047. `syntax` line 67; tags: none; `syntax KItem ::= #anyAcc(Iterable) | "#anyCont"`
0048. `rule` line 68; tags: operational; `rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>`
0049. `rule` line 69; tags: operational; `rule <k> #iterDone ~> #anyCont => false ... </k>`
0050. `rule` line 70; tags: operational; `rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k> requires truthy(V)`
0051. `rule` line 72; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k> requires notBool truthy(V)`
0052. `syntax` line 76; tags: none; `syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)`
0053. `rule` line 77; tags: operational; `rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>`
0054. `rule` line 78; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k> requires isInt(V)`
0055. `rule` line 80; tags: operational; `rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>`
0056. `rule` line 81; tags: operational; `rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>`
0057. `rule` line 82; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int) => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k> requires isInt(V)`
0058. `syntax` line 86; tags: none; `syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)`
0059. `rule` line 87; tags: operational; `rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>`
0060. `rule` line 88; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k> requires isInt(V)`
0061. `rule` line 90; tags: operational; `rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>`
0062. `rule` line 91; tags: operational; `rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>`
0063. `rule` line 92; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int) => #minAcc(R, minInt(M, {V}:>Int)) ... </k> requires isInt(V)`
0064. `syntax` line 97; tags: function; `syntax Int ::= maxVals(Int, Vals) [function]`
0065. `rule` line 98; tags: equation-or-macro; `rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)`
0066. `rule` line 99; tags: equation-or-macro; `rule maxVals(M:Int, .Vals) => M`
0067. `rule` line 100; tags: equation-or-macro; `rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)`
0068. `syntax` line 102; tags: function; `syntax Int ::= minVals(Int, Vals) [function]`
0069. `rule` line 103; tags: equation-or-macro; `rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)`
0070. `rule` line 104; tags: equation-or-macro; `rule minVals(M:Int, .Vals) => M`
0071. `rule` line 105; tags: equation-or-macro; `rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)`
0072. `rule` line 108; tags: equation-or-macro; `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N)))) requires N >=Int 0`
0073. `rule` line 111; tags: equation-or-macro; `rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N))))) requires N <Int 0`
0074. `syntax` line 114; tags: function, total; `syntax IntSeq ::= binCodes(Int) [function, total]`
0075. `rule` line 115; tags: equation-or-macro; `rule binCodes(0) => iCons(48, .IntSeq)`
0076. `rule` line 116; tags: equation-or-macro; `rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0`
0077. `syntax` line 117; tags: function, total; `syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]`
0078. `rule` line 118; tags: equation-or-macro; `rule binAcc(0, ACC:IntSeq) => ACC`
0079. `rule` line 119; tags: equation-or-macro; `rule binAcc(N:Int, ACC:IntSeq) => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC)) requires N >Int 0`
0080. `rule` line 124; tags: operational; `rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals)) => #alloc(list(enumVS(VS, 0))) ... </k>`
0081. `syntax` line 126; tags: function, total; `syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]`
0082. `rule` line 127; tags: equation-or-macro; `rule enumVS(.ValSeq, _:Int) => .ValSeq`
0083. `rule` line 128; tags: equation-or-macro; `rule enumVS(vCons(V:Val, R:ValSeq), I:Int) => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))`
0084. `rule` line 132; tags: operational; `rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals)) => #alloc(list(mapStrVS(VS))) ... </k>`
0085. `syntax` line 134; tags: function, total; `syntax ValSeq ::= mapStrVS(ValSeq) [function, total]`
0086. `rule` line 135; tags: equation-or-macro; `rule mapStrVS(.ValSeq) => .ValSeq`
0087. `rule` line 136; tags: equation-or-macro; `rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))`
0088. `rule` line 137; tags: equation-or-macro; `rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))`
0089. `rule` line 140; tags: equation-or-macro; `rule applyBuiltin("int", I:Int, .Vals) => I`
0090. `rule` line 143; tags: equation-or-macro; `rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C`
0091. `rule` line 144; tags: equation-or-macro; `rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq)) requires 0 <=Int I andBool I <Int 128`
0092. `rule` line 148; tags: equation-or-macro; `rule applyBuiltin("str", I:Int, .Vals) => str(strToCodes(Int2String(I)))`
0093. `rule` line 149; tags: equation-or-macro; `rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)`
0094. `rule` line 152; tags: equation-or-macro; `rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48 requires 48 <=Int C andBool C <=Int 57`
0095. `rule` line 156; tags: equation-or-macro; `rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0) requires isLen(CS) >=Int 2`
0096. `syntax` line 158; tags: function, total; `syntax Int ::= intDigAcc(IntSeq, Int) [function, total]`
0097. `rule` line 159; tags: equation-or-macro; `rule intDigAcc(.IntSeq, ACC:Int) => ACC`
0098. `rule` line 160; tags: equation-or-macro; `rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))`
0099. `rule` line 163; tags: equation-or-macro; `rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)`
0100. `rule` line 164; tags: equation-or-macro; `rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals) => zipObjS(A, B)`
0101. `rule` line 167; tags: operational; `rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq))) => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>`
0102. `rule` line 169; tags: operational; `rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq)) => #iterDone ... </k>`
0103. `rule` line 170; tags: operational; `rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>`
0104. `rule` line 171; tags: operational; `rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))) => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>`
0105. `rule` line 173; tags: operational; `rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq)) => #iterDone ... </k>`
0106. `rule` line 174; tags: operational; `rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>`
0107. `rule` line 177; tags: equation-or-macro; `rule applyBuiltin("range", I:Int, .Vals) => rangeObj(0, I, 1)`
0108. `rule` line 178; tags: equation-or-macro; `rule applyBuiltin("range", A:Int, B:Int, .Vals) => rangeObj(A, B, 1)`
0109. `rule` line 179; tags: equation-or-macro; `rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S) requires S =/=Int 0`
0110. `rule` line 187; tags: equation-or-macro; `rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)`
0111. `syntax` line 188; tags: function; `syntax Int ::= evalArith(IntSeq) [function]`
0112. `rule` line 189; tags: equation-or-macro; `rule evalArith(CS:IntSeq) => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))`
0113. `syntax` line 192; tags: none; `syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)`
0114. `syntax` line 194; tags: function, total; `syntax Bool ::= evDigit(Int) [function, total]`
0115. `rule` line 195; tags: equation-or-macro; `rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57`
0116. `syntax` line 196; tags: function, total; `syntax Bool ::= evHead42(IntSeq) [function, total]`
0117. `rule` line 197; tags: equation-or-macro; `rule evHead42(iCons(42, _:IntSeq)) => true`
0118. `rule` line 198; tags: owise, equation-or-macro; `rule evHead42(_:IntSeq) => false [owise]`
0119. `syntax` line 199; tags: function, total; `syntax Bool ::= evHead47(IntSeq) [function, total]`
0120. `rule` line 200; tags: equation-or-macro; `rule evHead47(iCons(47, _:IntSeq)) => true`
0121. `rule` line 201; tags: owise, equation-or-macro; `rule evHead47(_:IntSeq) => false [owise]`
0122. `syntax` line 203; tags: function, total; `syntax OpSeq ::= tokOps(IntSeq) [function, total]`
0123. `rule` line 204; tags: equation-or-macro; `rule tokOps(.IntSeq) => .OpSeq`
0124. `rule` line 205; tags: equation-or-macro; `rule tokOps(iCons(32, R:IntSeq)) => tokOps(R)`
0125. `rule` line 206; tags: equation-or-macro; `rule tokOps(iCons(C:Int, R:IntSeq)) => tokOps(R) requires evDigit(C)`
0126. `rule` line 207; tags: equation-or-macro; `rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))`
0127. `rule` line 208; tags: equation-or-macro; `rule tokOps(iCons(42, R:IntSeq)) => oCons("*", tokOps(R)) requires notBool evHead42(R)`
0128. `rule` line 209; tags: equation-or-macro; `rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("`
0129. `rule` line 210; tags: equation-or-macro; `rule tokOps(iCons(47, R:IntSeq)) => oCons("/", tokOps(R)) requires notBool evHead47(R)`
0130. `rule` line 211; tags: equation-or-macro; `rule tokOps(iCons(43, R:IntSeq)) => oCons("+", tokOps(R))`
0131. `rule` line 212; tags: equation-or-macro; `rule tokOps(iCons(45, R:IntSeq)) => oCons("-", tokOps(R))`
0132. `syntax` line 214; tags: function, total; `syntax IntSeq ::= tokNds(IntSeq) [function, total] | tokNdAcc(Int, IntSeq) [function, total]`
0133. `rule` line 216; tags: equation-or-macro; `rule tokNds(.IntSeq) => .IntSeq`
0134. `rule` line 217; tags: equation-or-macro; `rule tokNds(iCons(32, R:IntSeq)) => tokNds(R)`
0135. `rule` line 218; tags: equation-or-macro; `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)`
0136. `rule` line 219; tags: equation-or-macro; `rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R) requires notBool evDigit(C) andBool C =/=Int 32`
0137. `rule` line 221; tags: equation-or-macro; `rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R) requires evDigit(C)`
0138. `rule` line 223; tags: owise, equation-or-macro; `rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]`
0139. `syntax` line 225; tags: none; `syntax EvPair ::= evp(OpSeq, IntSeq)`
0140. `syntax` line 226; tags: function, total; `syntax Int ::= firstNdE(EvPair) [function, total]`
0141. `rule` line 227; tags: equation-or-macro; `rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N`
0142. `rule` line 228; tags: owise, equation-or-macro; `rule firstNdE(_:EvPair) => 0 [owise]`
0143. `syntax` line 230; tags: function, total; `syntax Int ::= applyOpE(String, Int, Int) [function, total]`
0144. `rule` line 231; tags: equation-or-macro; `rule applyOpE("+", A:Int, B:Int) => A +Int B`
0145. `rule` line 232; tags: equation-or-macro; `rule applyOpE("-", A:Int, B:Int) => A -Int B`
0146. `rule` line 233; tags: equation-or-macro; `rule applyOpE("*", A:Int, B:Int) => A *Int B`
0147. `rule` line 234; tags: equation-or-macro; `rule applyOpE("`
0148. `rule` line 235; tags: equation-or-macro; `rule applyOpE("**", A:Int, B:Int) => A ^Int B`
0149. `rule` line 236; tags: owise, equation-or-macro; `rule applyOpE(_:String, A:Int, _:Int) => A [owise]`
0150. `syntax` line 238; tags: function, total; `syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]`
0151. `rule` line 239; tags: equation-or-macro; `rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)`
0152. `rule` line 240; tags: equation-or-macro; `rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))`
0153. `rule` line 241; tags: equation-or-macro; `rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS)) requires O =/=String "**"`
0154. `rule` line 243; tags: owise, equation-or-macro; `rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]`
0155. `syntax` line 244; tags: function, total; `syntax EvPair ::= powCombE(Int, EvPair) [function, total]`
0156. `rule` line 245; tags: equation-or-macro; `rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))`
0157. `rule` line 246; tags: equation-or-macro; `rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))`
0158. `syntax` line 247; tags: function, total; `syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]`
0159. `rule` line 248; tags: equation-or-macro; `rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))`
0160. `syntax` line 250; tags: function, total; `syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]`
0161. `rule` line 251; tags: equation-or-macro; `rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)`
0162. `rule` line 252; tags: equation-or-macro; `rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
0163. `rule` line 253; tags: equation-or-macro; `rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)`
0164. `rule` line 254; tags: equation-or-macro; `rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)`
0165. `syntax` line 255; tags: function, total; `syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]`
0166. `rule` line 256; tags: equation-or-macro; `rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))`
0167. `rule` line 257; tags: equation-or-macro; `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON) requires inLevelE(L, O)`
0168. `rule` line 260; tags: equation-or-macro; `rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq) => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR)) requires notBool inLevelE(L, O)`
0169. `rule` line 263; tags: owise, equation-or-macro; `rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR)) [owise]`
0170. `syntax` line 265; tags: function, total; `syntax Bool ::= inLevelE(String, String) [function, total]`
0171. `rule` line 266; tags: equation-or-macro; `rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "`
0172. `rule` line 267; tags: equation-or-macro; `rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"`
0173. `rule` line 268; tags: owise, equation-or-macro; `rule inLevelE(_:String, _:String) => false [owise]`
0174. `syntax` line 269; tags: function, total; `syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]`
0175. `rule` line 270; tags: equation-or-macro; `rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)`
0176. `rule` line 271; tags: equation-or-macro; `rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))`
0177. `syntax` line 272; tags: function, total; `syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]`
0178. `rule` line 273; tags: equation-or-macro; `rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)`
0179. `rule` line 274; tags: equation-or-macro; `rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))`
0180. `syntax` line 279; tags: none; `syntax KItem ::= "#md5"`
0181. `rule` line 280; tags: priority, operational; `rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k> [priority(40)]`
0182. `rule` line 282; tags: operational; `rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>`
0183. `syntax` line 283; tags: none; `syntax Val ::= md5Obj(IntSeq)`
0184. `rule` line 284; tags: equation-or-macro; `rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))`
0185. `syntax` line 285; tags: function, total, symbol, no-evaluators; `syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]`
0186. `rule` line 291; tags: equation-or-macro; `rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)`
0187. `rule` line 292; tags: equation-or-macro; `rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)`
0188. `syntax` line 293; tags: function; `syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]`
0189. `rule` line 294; tags: equation-or-macro; `rule isIntV(_:Int) => true`
0190. `rule` line 295; tags: owise, equation-or-macro; `rule isIntV(_:Val) => false [owise]`
0191. `rule` line 296; tags: equation-or-macro; `rule isStrV(str(_:IntSeq)) => true`
0192. `rule` line 297; tags: owise, equation-or-macro; `rule isStrV(_:Val) => false [owise]`
## reference-semantics/semantics/call.k

0193. `rule` line 16; tags: operational; `rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>`
0194. `syntax` line 19; tags: none; `syntax KItem ::= #callee(Exprs)`
0195. `rule` line 20; tags: owise, operational; `rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]`
0196. `rule` line 21; tags: operational; `rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>`
0197. `rule` line 24; tags: operational; `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>`
0198. `rule` line 26; tags: operational; `rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>`
0199. `rule` line 27; tags: operational; `rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ) ... </k>`
0200. `rule` line 28; tags: operational; `rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ) ... </k>`
0201. `rule` line 29; tags: operational; `rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ) ... </k>`
0202. `rule` line 30; tags: operational; `rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ) ... </k>`
0203. `rule` line 31; tags: owise, operational; `rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]`
0204. `rule` line 32; tags: operational; `rule <k> #applyK(toCall(typeV(T:String)), ACC:Vals) => applyBuiltin(T, ACC) ... </k>`
0205. `rule` line 38; tags: priority, operational; `rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0206. `rule` line 42; tags: priority, operational; `rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals)) => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(A) [priority(40)]`
0207. `rule` line 47; tags: priority, operational; `rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(typeV(T)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0208. `syntax` line 52; tags: function, total; `syntax Bool ::= isMutMethod(String) [function, total]`
0209. `rule` line 53; tags: equation-or-macro; `rule isMutMethod(M:String) => M ==String "append" orBool M ==String "sort" orBool M ==String "extend" orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"`
0210. `rule` line 56; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals) => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) [priority(40)]`
0211. `rule` line 63; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals)) => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isMutMethod(M) andBool notBool isRefV(OBJ) [priority(40)]`
0212. `rule` line 69; tags: operational; `rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT => #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
0213. `rule` line 80; tags: operational; `rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k> <env> CALLERL:Int => NEWL </env> <scopes> STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes> <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc> <stack> .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>`
0214. `syntax` line 87; tags: none; `syntax KItem ::= #allocCells(ParamNames)`
0215. `rule` line 88; tags: operational; `rule <k> #allocCells(.ParamNames) => .K ... </k>`
0216. `rule` line 89; tags: operational; `rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes> <heap> H:Map => (N |-> cellV(noneV)) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`
## reference-semantics/semantics/comprehension.k

0217. `rule` line 11; tags: equation-or-macro; `rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
0218. `rule` line 12; tags: equation-or-macro; `rule GenExp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)`
0219. `syntax` line 14; tags: macro; `syntax Stmts ::= compBody(CompFors, Expr) [macro]`
0220. `rule` line 15; tags: equation-or-macro; `rule compBody(Gs:CompFors, ELT:Expr) => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))`
0221. `syntax` line 18; tags: macro, macro-rec; `syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]`
0222. `rule` line 19; tags: equation-or-macro; `rule compNest(.CompFors, ELT:Expr) => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))`
0223. `rule` line 21; tags: equation-or-macro; `rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr) => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))`
0224. `syntax` line 24; tags: macro; `syntax Expr ::= compGuard(Exprs) [macro]`
0225. `rule` line 25; tags: equation-or-macro; `rule compGuard(.Exprs) => Bool(true)`
0226. `rule` line 26; tags: equation-or-macro; `rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))`
## reference-semantics/semantics/concrete.k

0227. `rule` line 13; tags: operational; `rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`
0228. `rule` line 16; tags: operational; `rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k> <heap> HP:Map </heap> requires hasRefVS(A) orBool hasRefVS(B)`
0229. `syntax` line 25; tags: none; `syntax Val ::= kvP(Val, Val)`
0230. `syntax` line 26; tags: none; `syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool) | #ksIns(Val, ValSeq, Val, ValSeq, Bool)`
0231. `rule` line 28; tags: priority, operational; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #ksort(VS, KV, .ValSeq, false) ... </k> [priority(40)]`
0232. `rule` line 31; tags: priority, operational; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #ksort(VS, KV, .ValSeq, RB) ... </k> [priority(40)]`
0233. `rule` line 34; tags: operational; `rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool) => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>`
0234. `rule` line 36; tags: operational; `rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool) => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>`
0235. `rule` line 38; tags: operational; `rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool) => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k> requires notBool isKwV(K)`
0236. `syntax` line 42; tags: function; `syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]`
0237. `rule` line 43; tags: equation-or-macro; `rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)`
0238. `rule` line 44; tags: equation-or-macro; `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K, V), vCons(kvP(K2, V2), R)) requires kLt(K, K2)`
0239. `rule` line 47; tags: equation-or-macro; `rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val) => vCons(kvP(K2, V2), insPair(R, K, V)) requires notBool kLt(K, K2)`
0240. `syntax` line 51; tags: function; `syntax Bool ::= kLt(Val, Val) [function]`
0241. `rule` line 52; tags: equation-or-macro; `rule kLt(I1:Int, I2:Int) => I1 <Int I2`
0242. `rule` line 53; tags: equation-or-macro; `rule kLt(F1:Float, F2:Float) => F1 <Float F2`
0243. `rule` line 54; tags: equation-or-macro; `rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
0244. `syntax` line 56; tags: function, total; `syntax ValSeq ::= unpairVS(ValSeq) [function, total]`
0245. `rule` line 57; tags: equation-or-macro; `rule unpairVS(.ValSeq) => .ValSeq`
0246. `rule` line 58; tags: equation-or-macro; `rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))`
0247. `rule` line 59; tags: owise, equation-or-macro; `rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]`
## reference-semantics/semantics/controls.k

0248. `rule` line 9; tags: operational; `rule <k> Assign(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
0249. `rule` line 12; tags: priority, operational; `rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
0250. `rule` line 20; tags: operational; `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes> requires X in_keys(M)`
0251. `rule` line 27; tags: priority, operational; `rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val) [priority(40)]`
0252. `rule` line 35; tags: operational; `rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>`
0253. `rule` line 36; tags: owise, operational; `rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]`
0254. `syntax` line 37; tags: none; `syntax KItem ::= #bindImports(ParamNames)`
0255. `rule` line 38; tags: operational; `rule <k> #bindImports(.ParamNames) => .K ... </k>`
0256. `rule` line 39; tags: operational; `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes> requires N ==String "floor" orBool N ==String "ceil"`
0257. `rule` line 43; tags: operational; `rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k> requires notBool (N ==String "floor" orBool N ==String "ceil")`
0258. `rule` line 48; tags: operational; `rule <k> Expr(_:Val) => .K ... </k>`
0259. `syntax` line 51; tags: none; `syntax KItem ::= #branch(Bool, Stmts, Stmts)`
0260. `rule` line 52; tags: operational; `rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>`
0261. `rule` line 53; tags: operational; `rule <k> #branch(true, T:Stmts, _:Stmts) => T ... </k>`
0262. `rule` line 54; tags: operational; `rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>`
0263. `rule` line 57; tags: operational; `rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k> requires truthy(V)`
0264. `rule` line 59; tags: operational; `rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k> requires notBool truthy(V)`
0265. `syntax` line 65; tags: none; `syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts) | #while(Expr, Stmts) | #whileCond(Expr, Stmts) | #loopLbl(K) | "#cont" | "#brk"`
0266. `rule` line 69; tags: operational; `rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>`
0267. `rule` line 71; tags: operational; `rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>`
0268. `rule` line 72; tags: operational; `rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>`
0269. `rule` line 73; tags: operational; `rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts) => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>`
0270. `rule` line 77; tags: operational; `rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>`
0271. `rule` line 78; tags: operational; `rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>`
0272. `rule` line 79; tags: operational; `rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k> requires truthy(V)`
0273. `rule` line 81; tags: operational; `rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k> requires notBool truthy(V)`
0274. `rule` line 85; tags: operational; `rule <k> #loopLbl(NEXT:K) => NEXT ... </k>`
0275. `rule` line 86; tags: operational; `rule <k> Continue => #cont ... </k>`
0276. `rule` line 87; tags: operational; `rule <k> Break => #brk ... </k>`
0277. `rule` line 88; tags: operational; `rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>`
0278. `rule` line 89; tags: owise, operational; `rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]`
0279. `rule` line 90; tags: operational; `rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>`
0280. `rule` line 91; tags: owise, operational; `rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]`
0281. `rule` line 95; tags: priority, operational; `rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0282. `rule` line 98; tags: priority, operational; `rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0283. `rule` line 101; tags: priority, operational; `rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0284. `rule` line 106; tags: priority, operational; `rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
## reference-semantics/semantics/core.k

0285. `syntax` line 13; tags: none; `syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)`
0286. `syntax` line 14; tags: none; `syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)`
0287. `syntax` line 15; tags: none; `syntax Str ::= str(IntSeq)`
0288. `syntax` line 18; tags: none; `syntax Iterable ::= list(ValSeq) | tuple(ValSeq) | Str | rangeObj(Int, Int, Int) | zipObj(ValSeq, ValSeq) | zipObjS(IntSeq, IntSeq)`
0289. `syntax` line 25; tags: none; `syntax Val ::= Int | Bool | "noneV" | Iterable | ref(Int) | cellRef(Int) | closureVal(ParamNames, Stmts, Int) | typeV(String) | builtinV(String) | boundMethodV(Val, String)`
0290. `syntax` line 36; tags: none; `syntax Parent ::= "root" | parent(Int)`
0291. `syntax` line 37; tags: none; `syntax Scope ::= scope(Map, Parent)`
0292. `syntax` line 38; tags: none; `syntax KResult ::= Val`
0293. `syntax` line 39; tags: none; `syntax Expr ::= Val`
0294. `syntax` line 40; tags: none; `syntax Vals ::= List{Val, ","}`
0295. `syntax` line 41; tags: none; `syntax Exc ::= "NoExc" | "AssertionError"`
0296. `syntax` line 42; tags: none; `syntax RetState ::= "noRet" | retV(Val)`
0297. `configuration` line 49; tags: none; `configuration <k> #loadAll($PGM:Module) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code exit=""> 0 </exit-code>`
0298. `syntax` line 68; tags: function, total; `syntax Bool ::= isRefV(Val) [function, total]`
0299. `rule` line 69; tags: equation-or-macro; `rule isRefV(ref(_:Int)) => true`
0300. `rule` line 70; tags: owise, equation-or-macro; `rule isRefV(_:Val) => false [owise]`
0301. `syntax` line 75; tags: none; `syntax HeapVal ::= cellV(Val)`
0302. `syntax` line 76; tags: function, total; `syntax Bool ::= isCellRef(Val) [function, total]`
0303. `rule` line 77; tags: equation-or-macro; `rule isCellRef(cellRef(_:Int)) => true`
0304. `rule` line 78; tags: owise, equation-or-macro; `rule isCellRef(_:Val) => false [owise]`
0305. `rule` line 85; tags: priority, operational; `rule <k> cellRef(H:Int) => V ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires "$cells" in_keys(M) [priority(40)]`
0306. `syntax` line 95; tags: none; `syntax Val ::= kwV(String, Val)`
0307. `syntax` line 96; tags: none; `syntax KItem ::= #kwTag(String)`
0308. `rule` line 97; tags: operational; `rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>`
0309. `rule` line 98; tags: operational; `rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k> requires notBool isKwV(V)`
0310. `syntax` line 100; tags: function, total; `syntax Bool ::= isKwV(Val) [function, total]`
0311. `rule` line 101; tags: equation-or-macro; `rule isKwV(kwV(_:String, _:Val)) => true`
0312. `rule` line 102; tags: owise, equation-or-macro; `rule isKwV(_:Val) => false [owise]`
0313. `syntax` line 106; tags: none; `syntax Val ::= cellsMark(ParamNames)`
0314. `syntax` line 107; tags: function; `syntax ParamNames ::= cellsOf(Val) [function]`
0315. `rule` line 108; tags: equation-or-macro; `rule cellsOf(cellsMark(CVS:ParamNames)) => CVS`
0316. `syntax` line 109; tags: function, total; `syntax Bool ::= pnMember(String, ParamNames) [function, total]`
0317. `rule` line 110; tags: equation-or-macro; `rule pnMember(_:String, .ParamNames) => false`
0318. `rule` line 111; tags: equation-or-macro; `rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)`
0319. `syntax` line 113; tags: none; `syntax KItem ::= #cellW(Val, Val)`
0320. `rule` line 114; tags: operational; `rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k> <heap> ... H |-> cellV(_:Val => V) ... </heap>`
0321. `syntax` line 117; tags: none; `syntax KItem ::= #alloc(Val)`
0322. `rule` line 118; tags: operational; `rule <k> #alloc(V:Val) => ref(N) ... </k> <heap> H:Map => (N |-> V) H </heap> <heapLoc> N:Int => N +Int 1 </heapLoc> requires notBool N in_keys(H)`
0323. `syntax` line 124; tags: none; `syntax KItem ::= #loadAll(Module)`
0324. `rule` line 125; tags: operational; `rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>`
0325. `rule` line 126; tags: operational; `rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>`
0326. `rule` line 127; tags: operational; `rule <k> .Stmts => .K ... </k>`
0327. `syntax` line 130; tags: none; `syntax KItem ::= #look(String, Int)`
0328. `rule` line 131; tags: operational; `rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>`
0329. `rule` line 132; tags: operational; `rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> requires X in_keys(M)`
0330. `rule` line 145; tags: priority, operational; `rule <k> #look(X:String, L:Int) => V ... </k> <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes> <heap> ... H |-> cellV(V:Val) ... </heap> requires X in_keys(M) andBool "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool {M[X]}:>Val ==K cellRef(H) [priority(40)]`
0331. `rule` line 152; tags: operational; `rule <k> #look(X:String, L:Int) => #look(X, P) ... </k> <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes> requires notBool (X in_keys(M))`
0332. `syntax` line 157; tags: function, total; `syntax Scope ::= "builtinsScope" [function, total]`
0333. `rule` line 158; tags: equation-or-macro; `rule builtinsScope => scope(.Map [ "len" <- builtinV("len") ] [ "set" <- builtinV("set") ] [ "sum" <- builtinV("sum") ] [ "abs" <- builtinV("abs") ] [ "min" <- builtinV("min") ] [ "max" <- builtinV("max") ] [ "ord" <- builtinV("ord") ] [ "chr" <- builtinV("chr") ] [ "range" <- builtinV("range") ] [ "all" <- builtinV("all") ] [ "any" <- builtinV("any") ] [ "zip" <- builtinV("zip") ] [ "isinstance" <- builtinV("isinstance") ] [ "sorted" <- builtinV("sorted") ] [ "list" <- builtinV("list") ] [ "round" <- builtinV("round") ] [ "bin" <- builtinV("bin") ] [ "enumerate" <- builtinV("enumerate") ] [ "map" <- builtinV("map") ] [ "eval" <- builtinV("eval") ] [ "int" <- typeV("int") ] [ "str" <- typeV("str") ] [ "float" <- typeV("float") ], root)`
0334. `syntax` line 185; tags: none; `syntax ApplyK ::= toCall(Val)`
0335. `syntax` line 186; tags: none; `syntax KItem ::= #evalArgs(Exprs, Vals, ApplyK) | #evalArgCont(Exprs, Vals, ApplyK) | #applyK(ApplyK, Vals)`
0336. `rule` line 189; tags: operational; `rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>`
0337. `rule` line 190; tags: operational; `rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>`
0338. `rule` line 191; tags: operational; `rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>`
0339. `rule` line 194; tags: operational; `rule <k> Int(I:Int) => I ... </k>`
0340. `rule` line 195; tags: operational; `rule <k> Bool(B:Bool) => B ... </k>`
0341. `rule` line 196; tags: operational; `rule <k> NoneVal => noneV ... </k>`
0342. `syntax` line 199; tags: function; `syntax Bool ::= truthy(Val) [function]`
0343. `rule` line 200; tags: equation-or-macro; `rule truthy(B:Bool) => B`
0344. `rule` line 201; tags: equation-or-macro; `rule truthy(noneV) => false`
0345. `rule` line 202; tags: equation-or-macro; `rule truthy(I:Int) => I =/=Int 0`
0346. `rule` line 203; tags: equation-or-macro; `rule truthy(str(S:IntSeq)) => notBool (S ==K .IntSeq)`
0347. `rule` line 204; tags: equation-or-macro; `rule truthy(list(V:ValSeq)) => notBool (V ==K .ValSeq)`
0348. `rule` line 205; tags: equation-or-macro; `rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)`
0349. `syntax` line 208; tags: function; `syntax Val ::= applyUn(String, Val) [function]`
0350. `syntax` line 209; tags: function; `syntax Val ::= applyBin(String, Val, Val) [function]`
0351. `syntax` line 210; tags: function; `syntax Bool ::= applyCmp(String, Val, Val) [function]`
0352. `syntax` line 213; tags: function, total; `syntax Vals ::= appendVal(Vals, Val) [function, total]`
0353. `rule` line 214; tags: equation-or-macro; `rule appendVal(.Vals, V:Val) => V , .Vals`
0354. `rule` line 215; tags: equation-or-macro; `rule appendVal((V0:Val, VS:Vals), V:Val) => V0 , appendVal(VS, V)`
0355. `syntax` line 217; tags: function, total; `syntax ValSeq ::= vals2valSeq(Vals) [function, total]`
0356. `rule` line 218; tags: equation-or-macro; `rule vals2valSeq(.Vals) => .ValSeq`
0357. `rule` line 219; tags: equation-or-macro; `rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))`
0358. `syntax` line 223; tags: function, total; `syntax Int ::= vsLen(ValSeq) [function, total]`
0359. `rule` line 224; tags: equation-or-macro; `rule vsLen(.ValSeq) => 0`
0360. `rule` line 225; tags: equation-or-macro; `rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)`
0361. `syntax` line 227; tags: function, total; `syntax Int ::= isLen(IntSeq) [function, total]`
0362. `rule` line 228; tags: equation-or-macro; `rule isLen(.IntSeq) => 0`
0363. `rule` line 229; tags: equation-or-macro; `rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)`
0364. `syntax` line 233; tags: function, total; `syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]`
0365. `rule` line 234; tags: equation-or-macro; `rule setVSAt(.ValSeq, _:Int, _:Val) => .ValSeq`
0366. `rule` line 235; tags: equation-or-macro; `rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val) => vCons(V, S)`
0367. `rule` line 236; tags: equation-or-macro; `rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V)) requires I >Int 0`
0368. `rule` line 238; tags: equation-or-macro; `rule setVSAt(VS:ValSeq, I:Int, _:Val) => VS requires I <Int 0`
## reference-semantics/semantics/dict.k

0369. `syntax` line 20; tags: none; `syntax Val ::= dictV(ValSeq, ValSeq)`
0370. `syntax` line 23; tags: none; `syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq) | #dictKey(Expr, Entries, ValSeq, ValSeq) | #dictVal(Val, Entries, ValSeq, ValSeq)`
0371. `rule` line 26; tags: operational; `rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>`
0372. `rule` line 27; tags: operational; `rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>`
0373. `rule` line 28; tags: operational; `rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq) => K ~> #dictKey(V, REST, KS, VS) ... </k>`
0374. `rule` line 30; tags: operational; `rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq) => V ~> #dictVal(KV, REST, KS, VS) ... </k>`
0375. `rule` line 32; tags: operational; `rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq) => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>`
0376. `syntax` line 37; tags: function, total; `syntax Bool ::= dHasKey(ValSeq, Val) [function, total]`
0377. `rule` line 38; tags: equation-or-macro; `rule dHasKey(.ValSeq, _:Val) => false`
0378. `rule` line 39; tags: equation-or-macro; `rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true requires A ==K K`
0379. `rule` line 40; tags: equation-or-macro; `rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)`
0380. `syntax` line 43; tags: function, total; `syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]`
0381. `rule` line 44; tags: equation-or-macro; `rule dPutK(KS:ValSeq, K:Val) => KS requires dHasKey(KS, K)`
0382. `rule` line 45; tags: equation-or-macro; `rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)`
0383. `syntax` line 49; tags: function, total; `syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]`
0384. `rule` line 50; tags: equation-or-macro; `rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val) => vCons(V, VR) requires A ==K K`
0385. `rule` line 52; tags: equation-or-macro; `rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V)) requires notBool (A ==K K)`
0386. `rule` line 54; tags: owise, equation-or-macro; `rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]`
0387. `rule` line 58; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals) => #alloc(list(KS)) ... </k> [priority(40)]`
0388. `rule` line 63; tags: equation-or-macro; `rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)`
0389. `syntax` line 64; tags: function; `syntax Val ::= applyIndexD(Val, Val) [function]`
0390. `rule` line 65; tags: priority, operational; `rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k> [priority(45)]`
0391. `syntax` line 70; tags: function; `syntax Val ::= dictSet(Val, Val, Val) [function]`
0392. `rule` line 71; tags: equation-or-macro; `rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))`
0393. `syntax` line 76; tags: none; `syntax KItem ::= #dsetK(String, Val)`
0394. `rule` line 77; tags: operational; `rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>`
0395. `rule` line 78; tags: operational; `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes> requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)`
0396. `rule` line 82; tags: operational; `rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires X in_keys(M) andBool isRefV({M[X]}:>Val)`
0397. `syntax` line 86; tags: none; `syntax KItem ::= #dsetV(Val, Val, Val)`
0398. `rule` line 87; tags: operational; `rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k> <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>`
0399. `syntax` line 90; tags: function, total; `syntax Int ::= normIdxD(Int, Int) [function, total]`
0400. `rule` line 91; tags: equation-or-macro; `rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`
0401. `rule` line 92; tags: equation-or-macro; `rule normIdxD(I:Int, _:Int) => I requires I >=Int 0`
0402. `rule` line 95; tags: equation-or-macro; `rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq)) => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)`
0403. `syntax` line 97; tags: function; `syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]`
0404. `rule` line 98; tags: equation-or-macro; `rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true`
0405. `rule` line 99; tags: equation-or-macro; `rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq) => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)`
0406. `syntax` line 101; tags: function; `syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]`
0407. `rule` line 102; tags: equation-or-macro; `rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B requires A ==K K`
0408. `rule` line 103; tags: equation-or-macro; `rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)`
## reference-semantics/semantics/float.k

0409. `syntax` line 20; tags: none; `syntax Val ::= Float`
0410. `rule` line 21; tags: operational; `rule <k> Float(F:Float) => F ... </k>`
0411. `syntax` line 24; tags: function, total, symbol, no-evaluators; `syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]`
0412. `rule` line 25; tags: concrete, equation-or-macro; `rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]`
0413. `rule` line 27; tags: equation-or-macro; `rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)`
0414. `syntax` line 30; tags: function, total, symbol, no-evaluators; `syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]`
0415. `rule` line 31; tags: concrete, equation-or-macro; `rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]`
0416. `rule` line 32; tags: equation-or-macro; `rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)`
0417. `syntax` line 37; tags: function, total, symbol, no-evaluators; `syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]`
0418. `rule` line 38; tags: concrete, equation-or-macro; `rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]`
0419. `rule` line 39; tags: equation-or-macro; `rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)`
0420. `rule` line 43; tags: equation-or-macro; `rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2`
0421. `rule` line 44; tags: equation-or-macro; `rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)`
0422. `syntax` line 50; tags: function, total, symbol, no-evaluators; `syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]`
0423. `rule` line 51; tags: concrete, equation-or-macro; `rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]`
0424. `rule` line 52; tags: equation-or-macro; `rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)`
0425. `syntax` line 54; tags: function, total, symbol, no-evaluators; `syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]`
0426. `rule` line 55; tags: concrete, equation-or-macro; `rule absF(F:Float) => absFloat(F) [concrete]`
0427. `rule` line 56; tags: equation-or-macro; `rule applyBuiltin("abs", F:Float, .Vals) => absF(F)`
0428. `rule` line 61; tags: operational; `rule <k> Import(_:String) => .K ... </k>`
0429. `syntax` line 65; tags: none; `syntax KItem ::= "#mathCeil"`
0430. `rule` line 66; tags: priority, operational; `rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]`
0431. `rule` line 67; tags: operational; `rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>`
0432. `syntax` line 70; tags: none; `syntax KItem ::= "#mathFloor"`
0433. `rule` line 71; tags: priority, operational; `rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]`
0434. `rule` line 72; tags: operational; `rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>`
0435. `syntax` line 73; tags: function, total, symbol; `syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]`
0436. `rule` line 74; tags: concrete, equation-or-macro; `rule floorFI(I:Int) => I [concrete]`
0437. `rule` line 75; tags: concrete, equation-or-macro; `rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]`
0438. `rule` line 78; tags: equation-or-macro; `rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)`
0439. `rule` line 79; tags: equation-or-macro; `rule applyBuiltin("ceil", V:Val, .Vals) => ceilF(V)`
0440. `syntax` line 82; tags: none; `syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)`
0441. `rule` line 83; tags: priority, operational; `rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]`
0442. `rule` line 84; tags: operational; `rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>`
0443. `rule` line 85; tags: operational; `rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>`
0444. `syntax` line 86; tags: function, total, symbol; `syntax Float ::= toF(Val) [function, total, symbol(toF)]`
0445. `rule` line 87; tags: concrete, equation-or-macro; `rule toF(F:Float) => F [concrete]`
0446. `rule` line 88; tags: concrete, equation-or-macro; `rule toF(I:Int) => intToF(I) [concrete]`
0447. `syntax` line 93; tags: function, total, symbol; `syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]`
0448. `rule` line 94; tags: concrete, equation-or-macro; `rule ceilF(I:Int) => I [concrete]`
0449. `rule` line 95; tags: concrete, equation-or-macro; `rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]`
0450. `rule` line 99; tags: equation-or-macro; `rule applyUn("-", F:Float) => 0.0 -Float F`
0451. `syntax` line 103; tags: function, total, symbol, no-evaluators; `syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]`
0452. `rule` line 104; tags: concrete, equation-or-macro; `rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]`
0453. `rule` line 105; tags: equation-or-macro; `rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)`
0454. `syntax` line 107; tags: function, total, symbol, no-evaluators; `syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]`
0455. `rule` line 108; tags: concrete, equation-or-macro; `rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]`
0456. `rule` line 109; tags: equation-or-macro; `rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)`
0457. `syntax` line 111; tags: function, total, symbol, no-evaluators; `syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]`
0458. `rule` line 112; tags: concrete, equation-or-macro; `rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]`
0459. `rule` line 113; tags: equation-or-macro; `rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)`
0460. `syntax` line 115; tags: function, total, symbol, no-evaluators; `syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]`
0461. `rule` line 116; tags: concrete, equation-or-macro; `rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]`
0462. `rule` line 117; tags: equation-or-macro; `rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)`
0463. `syntax` line 119; tags: function, total, symbol, no-evaluators; `syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]`
0464. `rule` line 120; tags: concrete, equation-or-macro; `rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]`
0465. `rule` line 121; tags: equation-or-macro; `rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)`
0466. `syntax` line 125; tags: function, total, symbol, no-evaluators; `syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]`
0467. `rule` line 126; tags: concrete, equation-or-macro; `rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]`
0468. `rule` line 127; tags: equation-or-macro; `rule applyCmp(">", F1:Float, F2:Float) => gtF(F1, F2)`
0469. `rule` line 128; tags: equation-or-macro; `rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)`
0470. `rule` line 129; tags: equation-or-macro; `rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)`
0471. `rule` line 132; tags: equation-or-macro; `rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)`
0472. `rule` line 133; tags: equation-or-macro; `rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))`
0473. `rule` line 134; tags: equation-or-macro; `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
0474. `rule` line 135; tags: equation-or-macro; `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
0475. `rule` line 136; tags: equation-or-macro; `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
0476. `rule` line 137; tags: equation-or-macro; `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
0477. `rule` line 138; tags: equation-or-macro; `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
0478. `rule` line 139; tags: equation-or-macro; `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
0479. `syntax` line 142; tags: function, total, symbol, no-evaluators; `syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]`
0480. `rule` line 143; tags: concrete, equation-or-macro; `rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]`
0481. `rule` line 144; tags: equation-or-macro; `rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)`
0482. `rule` line 145; tags: equation-or-macro; `rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))`
0483. `rule` line 146; tags: equation-or-macro; `rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)`
0484. `rule` line 147; tags: equation-or-macro; `rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))`
0485. `rule` line 148; tags: equation-or-macro; `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
0486. `rule` line 149; tags: equation-or-macro; `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
0487. `rule` line 150; tags: equation-or-macro; `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
0488. `rule` line 151; tags: equation-or-macro; `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`
0489. `rule` line 154; tags: equation-or-macro; `rule applyCmp("==", V:Val, noneV) => V ==K noneV`
0490. `rule` line 155; tags: equation-or-macro; `rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)`
0491. `syntax` line 160; tags: function, total, symbol, no-evaluators; `syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]`
0492. `rule` line 161; tags: concrete, equation-or-macro; `rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]`
0493. `rule` line 162; tags: concrete, equation-or-macro; `rule decStrToF(CS:IntSeq) => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS))) requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]`
0494. `syntax` line 165; tags: function; `syntax Int ::= headIS(IntSeq) [function]`
0495. `rule` line 166; tags: equation-or-macro; `rule headIS(iCons(C:Int, _:IntSeq)) => C`
0496. `syntax` line 167; tags: function, total; `syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]`
0497. `rule` line 168; tags: equation-or-macro; `rule intPart(CS:IntSeq) => intPartAcc(CS, 0)`
0498. `rule` line 169; tags: equation-or-macro; `rule intPartAcc(.IntSeq, A:Int) => A`
0499. `rule` line 170; tags: equation-or-macro; `rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A`
0500. `rule` line 171; tags: equation-or-macro; `rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48)) requires C =/=Int 46`
0501. `syntax` line 173; tags: function, total; `syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]`
0502. `rule` line 174; tags: equation-or-macro; `rule fracPart(.IntSeq) => 0`
0503. `rule` line 175; tags: equation-or-macro; `rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)`
0504. `rule` line 176; tags: equation-or-macro; `rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46`
0505. `rule` line 177; tags: equation-or-macro; `rule fracAcc(.IntSeq, A:Int) => A`
0506. `rule` line 178; tags: equation-or-macro; `rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))`
0507. `syntax` line 179; tags: function, total; `syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]`
0508. `rule` line 180; tags: equation-or-macro; `rule fracScale(.IntSeq) => 1`
0509. `rule` line 181; tags: equation-or-macro; `rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)`
0510. `rule` line 182; tags: equation-or-macro; `rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46`
0511. `rule` line 183; tags: equation-or-macro; `rule fscAcc(.IntSeq, A:Int) => A`
0512. `rule` line 184; tags: equation-or-macro; `rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)`
0513. `rule` line 185; tags: equation-or-macro; `rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)`
0514. `rule` line 186; tags: equation-or-macro; `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`
0515. `rule` line 187; tags: equation-or-macro; `rule applyBuiltin("float", F:Float, .Vals) => F`
0516. `syntax` line 190; tags: function, total, symbol, no-evaluators; `syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]`
0517. `rule` line 191; tags: concrete, equation-or-macro; `rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]`
0518. `rule` line 192; tags: equation-or-macro; `rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)`
0519. `syntax` line 195; tags: function, total, symbol, no-evaluators; `syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]`
0520. `rule` line 196; tags: concrete, equation-or-macro; `rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]`
0521. `rule` line 197; tags: equation-or-macro; `rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)`
0522. `rule` line 198; tags: equation-or-macro; `rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))`
0523. `rule` line 199; tags: equation-or-macro; `rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)`
0524. `rule` line 200; tags: equation-or-macro; `rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))`
0525. `rule` line 201; tags: equation-or-macro; `rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)`
0526. `rule` line 202; tags: equation-or-macro; `rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))`
0527. `rule` line 203; tags: equation-or-macro; `rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)`
0528. `rule` line 204; tags: equation-or-macro; `rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))`
0529. `rule` line 205; tags: equation-or-macro; `rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)`
0530. `rule` line 206; tags: equation-or-macro; `rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))`
0531. `syntax` line 209; tags: function, total, symbol, no-evaluators; `syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]`
0532. `rule` line 210; tags: concrete, equation-or-macro; `rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]`
0533. `rule` line 211; tags: equation-or-macro; `rule applyBuiltin("int", F:Float, .Vals) => truncF(F)`
0534. `rule` line 213; tags: equation-or-macro; `rule applyBuiltin("float", I:Int, .Vals) => intToF(I)`
0535. `rule` line 214; tags: equation-or-macro; `rule applyBuiltin("float", F:Float, .Vals) => F`
0536. `syntax` line 217; tags: function, total, symbol, no-evaluators; `syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]`
0537. `rule` line 218; tags: concrete, equation-or-macro; `rule roundF(F:Float) => #if (F -Float floorFloat(F)) ==Float 0.5 #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi) #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]`
0538. `syntax` line 223; tags: function, total, symbol, no-evaluators; `syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]`
0539. `rule` line 224; tags: concrete, equation-or-macro; `rule roundFN(F:Float, N:Int) => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11) /Float Int2Float(10 ^Int N, 53, 11) [concrete]`
0540. `rule` line 227; tags: equation-or-macro; `rule applyBuiltin("round", F:Float, .Vals) => roundF(F)`
0541. `rule` line 228; tags: equation-or-macro; `rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)`
0542. `syntax` line 230; tags: function, total, symbol, no-evaluators; `syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]`
0543. `rule` line 231; tags: concrete, equation-or-macro; `rule sqrtF(F:Float) => sqrtFloat(F) [concrete]`
0544. `syntax` line 232; tags: none; `syntax KItem ::= "#mathSqrt"`
0545. `rule` line 233; tags: priority, operational; `rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]`
0546. `rule` line 234; tags: operational; `rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>`
0547. `rule` line 235; tags: operational; `rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>`
0548. `syntax` line 243; tags: none; `syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)`
0549. `rule` line 244; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
0550. `rule` line 245; tags: operational; `rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>`
0551. `rule` line 246; tags: operational; `rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>`
0552. `rule` line 247; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`
0553. `syntax` line 250; tags: none; `syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)`
0554. `rule` line 251; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)`
0555. `rule` line 252; tags: operational; `rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>`
0556. `rule` line 253; tags: operational; `rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>`
0557. `rule` line 254; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k> requires isFloat(V)`
0558. `syntax` line 261; tags: none; `syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)`
0559. `rule` line 262; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int) => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k> requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))`
0560. `rule` line 265; tags: operational; `rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>`
0561. `rule` line 266; tags: operational; `rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>`
0562. `rule` line 267; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k> requires isFloat(V)`
0563. `rule` line 270; tags: operational; `rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float) => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k> requires isInt(V) orBool isBool(V)`
## reference-semantics/semantics/functions.k

0564. `syntax` line 8; tags: none; `syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int) | #bindP(ParamNames, Vals) | "#pop" | "#endcall"`
0565. `rule` line 14; tags: operational; `rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>`
0566. `syntax` line 18; tags: none; `syntax Expr ::= closureExpr(ParamNames, Stmts)`
0567. `rule` line 19; tags: operational; `rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k> <env> L:Int </env>`
0568. `syntax` line 27; tags: none; `syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)`
0569. `syntax` line 31; tags: none; `syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map) | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)`
0570. `rule` line 33; tags: operational; `rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), BODY:Stmts) => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>`
0571. `rule` line 36; tags: operational; `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
0572. `rule` line 42; tags: operational; `rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>`
0573. `rule` line 47; tags: operational; `rule <k> Lambda(Params(PNS:ParamNames), E:Expr) => closureVal(PNS, Return(E) .Stmts, L) ... </k> <env> L:Int </env>`
0574. `rule` line 50; tags: operational; `rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames), FreeVars(FVS:ParamNames), E:Expr) => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>`
0575. `rule` line 53; tags: operational; `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map) => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires FV in_keys(M)`
0576. `rule` line 59; tags: operational; `rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map) => closureValC(PNS, CVS, BODY, CM) ... </k>`
0577. `rule` line 63; tags: operational; `rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>`
0578. `rule` line 64; tags: operational; `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>`
0579. `rule` line 68; tags: priority, operational; `rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(P, cellsOf({M["$cells"]}:>Val)) andBool P in_keys(M) andBool isCellRef({M[P]}:>Val) [priority(40)]`
0580. `rule` line 78; tags: operational; `rule <k> Return(V:Val) ~> _ => #pop </k> <ret> noRet => retV(V) </ret>`
0581. `rule` line 80; tags: operational; `rule <k> #endcall => #pop ... </k> <ret> noRet => retV(noneV) </ret>`
0582. `rule` line 85; tags: operational; `rule <k> #pop => V ~> CONT </k> <ret> retV(V) => noRet </ret> <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack> <env> L:Int => CALLERL </env> <scopes> SC:Map => SC [ L <- undef ] </scopes> <scopeLoc> _ => SAVEDL </scopeLoc>`
## reference-semantics/semantics/int.k

0583. `rule` line 7; tags: equation-or-macro; `rule applyUn("-", I:Int) => 0 -Int I`
0584. `rule` line 9; tags: equation-or-macro; `rule applyBin("+", I1:Int, I2:Int) => I1 +Int I2`
0585. `rule` line 11; tags: equation-or-macro; `rule applyBin("+", I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi`
0586. `rule` line 12; tags: equation-or-macro; `rule applyBin("+", B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I`
0587. `rule` line 13; tags: equation-or-macro; `rule applyBin("-", I1:Int, I2:Int) => I1 -Int I2`
0588. `rule` line 14; tags: equation-or-macro; `rule applyBin("*", I1:Int, I2:Int) => I1 *Int I2`
0589. `rule` line 15; tags: equation-or-macro; `rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)`
0590. `rule` line 16; tags: equation-or-macro; `rule applyBin("`
0591. `rule` line 17; tags: equation-or-macro; `rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0`
0592. `syntax` line 19; tags: function; `syntax Int ::= pyMod(Int, Int) [function]`
0593. `rule` line 20; tags: equation-or-macro; `rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2`
0594. `rule` line 22; tags: equation-or-macro; `rule applyCmp("<", I1:Int, I2:Int) => I1 <Int I2`
0595. `rule` line 23; tags: equation-or-macro; `rule applyCmp("<=", I1:Int, I2:Int) => I1 <=Int I2`
0596. `rule` line 24; tags: equation-or-macro; `rule applyCmp(">", I1:Int, I2:Int) => I1 >Int I2`
0597. `rule` line 25; tags: equation-or-macro; `rule applyCmp(">=", I1:Int, I2:Int) => I1 >=Int I2`
0598. `rule` line 26; tags: equation-or-macro; `rule applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`
0599. `rule` line 27; tags: equation-or-macro; `rule applyCmp("!=", I1:Int, I2:Int) => I1 =/=Int I2`
## reference-semantics/semantics/iter.k

0600. `syntax` line 8; tags: none; `syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)`
## reference-semantics/semantics/list.k

0601. `rule` line 9; tags: operational; `rule <k> #iterNext(list(.ValSeq)) => #iterDone ... </k>`
0602. `rule` line 10; tags: operational; `rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>`
0603. `syntax` line 13; tags: none; `syntax ApplyK ::= "toList"`
0604. `rule` line 14; tags: operational; `rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>`
0605. `rule` line 15; tags: operational; `rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>`
0606. `syntax` line 18; tags: function, total; `syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]`
0607. `rule` line 19; tags: equation-or-macro; `rule valSeqConcat(.ValSeq, T:ValSeq) => T`
0608. `rule` line 20; tags: equation-or-macro; `rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))`
0609. `rule` line 24; tags: priority, operational; `rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k> [priority(45)]`
0610. `rule` line 27; tags: equation-or-macro; `rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B`
0611. `rule` line 28; tags: equation-or-macro; `rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)`
0612. `syntax` line 33; tags: function, total; `syntax Bool ::= hasRefVS(ValSeq) [function, total]`
0613. `rule` line 34; tags: equation-or-macro; `rule hasRefVS(.ValSeq) => false`
0614. `rule` line 35; tags: equation-or-macro; `rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)`
0615. `syntax` line 37; tags: function; `syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function] | deepEqV(Val, Val, Map) [function]`
0616. `rule` line 39; tags: equation-or-macro; `rule deepEqVS(.ValSeq, .ValSeq, _:Map) => true`
0617. `rule` line 40; tags: equation-or-macro; `rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map) => false`
0618. `rule` line 41; tags: equation-or-macro; `rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map) => false`
0619. `rule` line 42; tags: equation-or-macro; `rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map) => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)`
0620. `rule` line 45; tags: equation-or-macro; `rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP) requires H in_keys(HP)`
0621. `rule` line 47; tags: equation-or-macro; `rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP) requires notBool isRefV(A) andBool H in_keys(HP)`
0622. `rule` line 49; tags: equation-or-macro; `rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)`
0623. `rule` line 50; tags: owise, equation-or-macro; `rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]`
0624. `rule` line 53; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap> [priority(40)]`
0625. `syntax` line 58; tags: none; `syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"`
0626. `rule` line 59; tags: operational; `rule <k> Compare(LV:Val, CmpOp("in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>`
0627. `rule` line 60; tags: operational; `rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>`
0628. `rule` line 61; tags: operational; `rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>`
0629. `rule` line 62; tags: operational; `rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>`
0630. `rule` line 63; tags: operational; `rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k> requires E ==K V`
0631. `rule` line 65; tags: operational; `rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k> requires notBool (E ==K V)`
0632. `rule` line 67; tags: operational; `rule <k> B:Bool ~> #notB => notBool B ... </k>`
## reference-semantics/semantics/methods.k

0633. `syntax` line 10; tags: function; `syntax Val ::= applyMethod(Val, String, Vals) [function]`
0634. `rule` line 13; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)`
0635. `rule` line 14; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)`
0636. `rule` line 15; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)`
0637. `rule` line 16; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)`
0638. `rule` line 19; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "lower", .Vals) => str(mapLower(CS))`
0639. `rule` line 20; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "upper", .Vals) => str(mapUpper(CS))`
0640. `rule` line 21; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))`
0641. `rule` line 26; tags: equation-or-macro; `rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))`
0642. `syntax` line 27; tags: function, total; `syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]`
0643. `rule` line 28; tags: equation-or-macro; `rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq`
0644. `rule` line 29; tags: equation-or-macro; `rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS`
0645. `rule` line 30; tags: equation-or-macro; `rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq))) => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))`
0646. `rule` line 34; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)`
0647. `syntax` line 35; tags: function; `syntax Int ::= cntSub(IntSeq, IntSeq) [function]`
0648. `rule` line 36; tags: equation-or-macro; `rule cntSub(.IntSeq, _:IntSeq) => 0`
0649. `rule` line 37; tags: equation-or-macro; `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC) requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0`
0650. `rule` line 39; tags: equation-or-macro; `rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC) requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0`
0651. `syntax` line 41; tags: function, total; `syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]`
0652. `rule` line 42; tags: equation-or-macro; `rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0`
0653. `rule` line 43; tags: owise, equation-or-macro; `rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]`
0654. `rule` line 44; tags: equation-or-macro; `rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0`
0655. `rule` line 47; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))`
0656. `syntax` line 48; tags: function, total; `syntax IntSeq ::= trimWS(IntSeq) [function, total]`
0657. `rule` line 49; tags: equation-or-macro; `rule trimWS(.IntSeq) => .IntSeq`
0658. `rule` line 50; tags: equation-or-macro; `rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)`
0659. `rule` line 51; tags: equation-or-macro; `rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)`
0660. `syntax` line 52; tags: function, total; `syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]`
0661. `rule` line 53; tags: equation-or-macro; `rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)`
0662. `rule` line 54; tags: equation-or-macro; `rule revISAcc(.IntSeq, A:IntSeq) => A`
0663. `rule` line 55; tags: equation-or-macro; `rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))`
0664. `rule` line 58; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)`
0665. `rule` line 61; tags: equation-or-macro; `rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)`
0666. `rule` line 64; tags: equation-or-macro; `rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)`
0667. `syntax` line 65; tags: function, total; `syntax Int ::= cntOccVS(ValSeq, Val) [function, total]`
0668. `rule` line 66; tags: equation-or-macro; `rule cntOccVS(.ValSeq, _:Val) => 0`
0669. `rule` line 67; tags: equation-or-macro; `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V`
0670. `rule` line 68; tags: equation-or-macro; `rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V) requires notBool (A ==K V)`
0671. `rule` line 72; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals) => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k> [priority(40)]`
0672. `syntax` line 75; tags: function; `syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]`
0673. `rule` line 76; tags: equation-or-macro; `rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)`
0674. `rule` line 77; tags: equation-or-macro; `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR)) requires isWSC(C)`
0675. `rule` line 79; tags: equation-or-macro; `rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC) requires notBool isWSC(C)`
0676. `syntax` line 82; tags: function; `syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]`
0677. `rule` line 83; tags: equation-or-macro; `rule flushTok(ACC:ValSeq, .IntSeq) => ACC`
0678. `rule` line 84; tags: equation-or-macro; `rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))`
0679. `syntax` line 85; tags: function, total; `syntax Bool ::= isWSC(Int) [function, total]`
0680. `rule` line 86; tags: equation-or-macro; `rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13`
0681. `rule` line 89; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals)) => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k> [priority(39)]`
0682. `rule` line 94; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals)) => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k> [priority(40)]`
0683. `syntax` line 97; tags: function; `syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]`
0684. `rule` line 98; tags: equation-or-macro; `rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq) => vCons(str(CUR), .ValSeq)`
0685. `rule` line 99; tags: equation-or-macro; `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq)) requires C ==Int SEP`
0686. `rule` line 101; tags: equation-or-macro; `rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq))) requires notBool (C ==Int SEP)`
0687. `rule` line 104; tags: equation-or-macro; `rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals) => str(replaceC(CS, A, B))`
0688. `syntax` line 106; tags: function, total; `syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]`
0689. `rule` line 107; tags: equation-or-macro; `rule replaceC(.IntSeq, _:Int, _:Int) => .IntSeq`
0690. `rule` line 108; tags: equation-or-macro; `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A`
0691. `rule` line 109; tags: equation-or-macro; `rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)`
0692. `syntax` line 112; tags: function, total; `syntax Bool ::= isUpperC(Int) [function, total]`
0693. `rule` line 113; tags: equation-or-macro; `rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90`
0694. `syntax` line 115; tags: function, total; `syntax Bool ::= isLowerC(Int) [function, total]`
0695. `rule` line 116; tags: equation-or-macro; `rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122`
0696. `syntax` line 118; tags: function, total; `syntax Bool ::= isAlphaC(Int) [function, total]`
0697. `rule` line 119; tags: equation-or-macro; `rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)`
0698. `syntax` line 121; tags: function, total; `syntax Bool ::= isDigitC(Int) [function, total]`
0699. `rule` line 122; tags: equation-or-macro; `rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57`
0700. `syntax` line 124; tags: function, total; `syntax Bool ::= hasUpper(IntSeq) [function, total]`
0701. `rule` line 125; tags: equation-or-macro; `rule hasUpper(.IntSeq) => false`
0702. `rule` line 126; tags: equation-or-macro; `rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)`
0703. `syntax` line 128; tags: function, total; `syntax Bool ::= hasLower(IntSeq) [function, total]`
0704. `rule` line 129; tags: equation-or-macro; `rule hasLower(.IntSeq) => false`
0705. `rule` line 130; tags: equation-or-macro; `rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)`
0706. `syntax` line 132; tags: function, total; `syntax Bool ::= allAlpha(IntSeq) [function, total]`
0707. `rule` line 133; tags: equation-or-macro; `rule allAlpha(.IntSeq) => true`
0708. `rule` line 134; tags: equation-or-macro; `rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)`
0709. `syntax` line 136; tags: function, total; `syntax Bool ::= allDigit(IntSeq) [function, total]`
0710. `rule` line 137; tags: equation-or-macro; `rule allDigit(.IntSeq) => true`
0711. `rule` line 138; tags: equation-or-macro; `rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)`
0712. `syntax` line 140; tags: function, total; `syntax Int ::= lowerC(Int) [function, total]`
0713. `rule` line 142; tags: equation-or-macro; `rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)`
0714. `rule` line 143; tags: owise, equation-or-macro; `rule lowerC(C:Int) => C [owise]`
0715. `syntax` line 145; tags: function, total; `syntax Int ::= upperC(Int) [function, total]`
0716. `rule` line 146; tags: equation-or-macro; `rule upperC(C:Int) => C -Int 32 requires isLowerC(C)`
0717. `rule` line 147; tags: owise, equation-or-macro; `rule upperC(C:Int) => C [owise]`
0718. `syntax` line 149; tags: function, total; `syntax Int ::= swapC(Int) [function, total]`
0719. `rule` line 150; tags: equation-or-macro; `rule swapC(C:Int) => C +Int 32 requires isUpperC(C)`
0720. `rule` line 151; tags: equation-or-macro; `rule swapC(C:Int) => C -Int 32 requires isLowerC(C)`
0721. `rule` line 152; tags: owise, equation-or-macro; `rule swapC(C:Int) => C [owise]`
0722. `syntax` line 154; tags: function, total; `syntax IntSeq ::= mapLower(IntSeq) [function, total]`
0723. `rule` line 155; tags: equation-or-macro; `rule mapLower(.IntSeq) => .IntSeq`
0724. `rule` line 156; tags: equation-or-macro; `rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))`
0725. `syntax` line 158; tags: function, total; `syntax IntSeq ::= mapUpper(IntSeq) [function, total]`
0726. `rule` line 159; tags: equation-or-macro; `rule mapUpper(.IntSeq) => .IntSeq`
0727. `rule` line 160; tags: equation-or-macro; `rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))`
0728. `syntax` line 162; tags: function, total; `syntax IntSeq ::= mapSwap(IntSeq) [function, total]`
0729. `rule` line 163; tags: equation-or-macro; `rule mapSwap(.IntSeq) => .IntSeq`
0730. `rule` line 164; tags: equation-or-macro; `rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))`
0731. `syntax` line 166; tags: function, total; `syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]`
0732. `rule` line 167; tags: equation-or-macro; `rule startsWith(.IntSeq, _:IntSeq) => true`
0733. `rule` line 168; tags: equation-or-macro; `rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false`
0734. `rule` line 169; tags: equation-or-macro; `rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)`
## reference-semantics/semantics/operators.k

0735. `rule` line 10; tags: operational; `rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>`
0736. `rule` line 12; tags: operational; `rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>`
0737. `context` line 15; tags: none; `context Compare(HOLE, _)`
0738. `context` line 16; tags: none; `context Compare(_:Val, CmpOp(_, HOLE))`
0739. `rule` line 17; tags: owise, operational; `rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]`
0740. `rule` line 19; tags: equation-or-macro; `rule applyCmp("is", V:Val, noneV) => V ==K noneV`
0741. `rule` line 20; tags: equation-or-macro; `rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)`
0742. `rule` line 25; tags: priority, operational; `rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0743. `rule` line 28; tags: priority, operational; `rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) [priority(40)]`
0744. `rule` line 34; tags: priority, operational; `rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k> <heap> ... H |-> V:Val ... </heap> requires OP =/=String "in" andBool OP =/=String "not in" [priority(40)]`
0745. `rule` line 38; tags: priority, operational; `rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k> <heap> ... H |-> V:Val ... </heap> requires notBool isRefV(L) orBool OP ==String "in" orBool OP ==String "not in" [priority(40)]`
0746. `rule` line 44; tags: priority, operational; `rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
## reference-semantics/semantics/range.k

0747. `syntax` line 9; tags: function, total; `syntax Bool ::= inRange(Int, Int, Int) [function, total]`
0748. `rule` line 10; tags: equation-or-macro; `rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)`
0749. `syntax` line 12; tags: function; `syntax Int ::= rangeLen(Int, Int, Int) [function]`
0750. `rule` line 13; tags: equation-or-macro; `rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST requires ST >Int 0 andBool HI >Int LO`
0751. `rule` line 15; tags: equation-or-macro; `rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST) requires ST <Int 0 andBool HI <Int LO`
0752. `rule` line 17; tags: equation-or-macro; `rule rangeLen(LO:Int, HI:Int, ST:Int) => 0 requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)`
0753. `rule` line 20; tags: operational; `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k> requires inRange(I, HI, ST)`
0754. `rule` line 23; tags: operational; `rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k> requires notBool inRange(I, HI, ST)`
## reference-semantics/semantics/set.k

0755. `syntax` line 8; tags: none; `syntax Val ::= setV(IntSeq)`
0756. `syntax` line 11; tags: function, total; `syntax Bool ::= codeIn(Int, IntSeq) [function, total]`
0757. `rule` line 12; tags: equation-or-macro; `rule codeIn(_:Int, .IntSeq) => false`
0758. `rule` line 13; tags: equation-or-macro; `rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)`
0759. `syntax` line 16; tags: function, total; `syntax IntSeq ::= dedupCodes(IntSeq) [function, total] | dedupFrom(IntSeq, IntSeq) [function, total]`
0760. `rule` line 18; tags: equation-or-macro; `rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)`
0761. `rule` line 19; tags: equation-or-macro; `rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC`
0762. `rule` line 20; tags: equation-or-macro; `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC) requires codeIn(C, ACC)`
0763. `rule` line 22; tags: equation-or-macro; `rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C)) requires notBool codeIn(C, ACC)`
0764. `syntax` line 25; tags: function, total; `syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]`
0765. `rule` line 26; tags: equation-or-macro; `rule snocCode(.IntSeq, C:Int) => iCons(C, .IntSeq)`
0766. `rule` line 27; tags: equation-or-macro; `rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))`
0767. `syntax` line 31; tags: function, total; `syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]`
0768. `rule` line 32; tags: equation-or-macro; `rule subsetCodes(.IntSeq, _:IntSeq) => true`
0769. `rule` line 33; tags: equation-or-macro; `rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)`
0770. `syntax` line 35; tags: function, total; `syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]`
0771. `rule` line 36; tags: equation-or-macro; `rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)`
0772. `rule` line 39; tags: equation-or-macro; `rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)`
## reference-semantics/semantics/sort.k

0773. `syntax` line 18; tags: function, total, symbol, no-evaluators; `syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]`
0774. `syntax` line 19; tags: function; `syntax ValSeq ::= insVS(Int, ValSeq) [function]`
0775. `rule` line 20; tags: concrete, equation-or-macro; `rule sortVS(.ValSeq) => .ValSeq [concrete]`
0776. `rule` line 21; tags: concrete, equation-or-macro; `rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]`
0777. `rule` line 22; tags: concrete, equation-or-macro; `rule insVS(X:Int, .ValSeq) => vCons(X, .ValSeq) [concrete]`
0778. `rule` line 23; tags: concrete, equation-or-macro; `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]`
0779. `rule` line 24; tags: concrete, equation-or-macro; `rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X >Int Y [concrete]`
0780. `syntax` line 26; tags: function; `syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]`
0781. `rule` line 27; tags: concrete, equation-or-macro; `rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]`
0782. `rule` line 28; tags: concrete, equation-or-macro; `rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]`
0783. `rule` line 29; tags: concrete, equation-or-macro; `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R)) requires strLt(A, B) orBool A ==K B [concrete]`
0784. `rule` line 31; tags: concrete, equation-or-macro; `rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R)) requires notBool (strLt(A, B) orBool A ==K B) [concrete]`
0785. `rule` line 36; tags: operational; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals)) => #alloc(list(sortVS(VS))) ... </k>`
0786. `rule` line 40; tags: priority, operational; `rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k> <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap> [priority(40)]`
0787. `syntax` line 49; tags: function, total, symbol, no-evaluators; `syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]`
0788. `syntax` line 51; tags: function, total; `syntax ValSeq ::= revVS(ValSeq) [function, total] | revVSAcc(ValSeq, ValSeq) [function, total]`
0789. `rule` line 53; tags: equation-or-macro; `rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)`
0790. `rule` line 54; tags: equation-or-macro; `rule revVSAcc(.ValSeq, A:ValSeq) => A`
0791. `rule` line 55; tags: equation-or-macro; `rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))`
0792. `syntax` line 57; tags: function, total; `syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]`
0793. `rule` line 58; tags: equation-or-macro; `rule condRev(S:ValSeq, false) => S`
0794. `rule` line 59; tags: equation-or-macro; `rule condRev(S:ValSeq, true) => revVS(S)`
0795. `rule` line 61; tags: operational; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals)) => #alloc(list(sortKeyVS(VS, KV))) ... </k>`
0796. `rule` line 63; tags: operational; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>`
0797. `rule` line 65; tags: operational; `rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals)) => #alloc(list(condRev(sortVS(VS), RB))) ... </k>`
## reference-semantics/semantics/str.k

0798. `rule` line 8; tags: operational; `rule <k> #iterNext(str(.IntSeq)) => #iterDone ... </k>`
0799. `rule` line 9; tags: operational; `rule <k> #iterNext(str(iCons(C:Int, R:IntSeq))) => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>`
0800. `syntax` line 13; tags: function; `syntax IntSeq ::= strToCodes(String) [function]`
0801. `rule` line 14; tags: operational; `rule <k> Str(S:String) => str(strToCodes(S)) ... </k>`
0802. `rule` line 15; tags: equation-or-macro; `rule strToCodes("") => .IntSeq`
0803. `rule` line 16; tags: equation-or-macro; `rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S)))) requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128`
0804. `syntax` line 20; tags: function, total; `syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]`
0805. `rule` line 21; tags: equation-or-macro; `rule seqConcat(.IntSeq, T:IntSeq) => T`
0806. `rule` line 22; tags: equation-or-macro; `rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))`
0807. `rule` line 24; tags: equation-or-macro; `rule applyBin("+", str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))`
0808. `rule` line 25; tags: equation-or-macro; `rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B`
0809. `rule` line 26; tags: equation-or-macro; `rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)`
0810. `rule` line 29; tags: equation-or-macro; `rule applyCmp("in", str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)`
0811. `rule` line 30; tags: equation-or-macro; `rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)`
0812. `syntax` line 32; tags: function, total; `syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]`
0813. `rule` line 33; tags: equation-or-macro; `rule strPrefix(.IntSeq, _:IntSeq) => true`
0814. `rule` line 34; tags: equation-or-macro; `rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false`
0815. `rule` line 35; tags: equation-or-macro; `rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)`
0816. `syntax` line 37; tags: function, total; `syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]`
0817. `rule` line 38; tags: equation-or-macro; `rule strContains(P:IntSeq, X:IntSeq) => true requires strPrefix(P, X)`
0818. `rule` line 39; tags: equation-or-macro; `rule strContains(P:IntSeq, .IntSeq) => false requires notBool strPrefix(P, .IntSeq)`
0819. `rule` line 40; tags: equation-or-macro; `rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs) requires notBool strPrefix(P, iCons(C, Xs))`
0820. `syntax` line 48; tags: function, total; `syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]`
0821. `rule` line 49; tags: equation-or-macro; `rule strLt(.IntSeq, .IntSeq) => false`
0822. `rule` line 50; tags: equation-or-macro; `rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true`
0823. `rule` line 51; tags: equation-or-macro; `rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false`
0824. `rule` line 52; tags: equation-or-macro; `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true requires A <Int B`
0825. `rule` line 53; tags: equation-or-macro; `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false requires A >Int B`
0826. `rule` line 54; tags: equation-or-macro; `rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B`
0827. `rule` line 56; tags: equation-or-macro; `rule applyCmp("<", str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)`
0828. `rule` line 57; tags: equation-or-macro; `rule applyCmp(">", str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)`
0829. `rule` line 58; tags: equation-or-macro; `rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)`
0830. `rule` line 59; tags: equation-or-macro; `rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)`
## reference-semantics/semantics/subscript.k

0831. `syntax` line 11; tags: function, total; `syntax Val ::= valSeqAt(ValSeq, Int) [function, total]`
0832. `rule` line 12; tags: equation-or-macro; `rule valSeqAt(vCons(V:Val, _:ValSeq), 0) => V`
0833. `rule` line 13; tags: equation-or-macro; `rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1) requires I >Int 0`
0834. `syntax` line 16; tags: function; `syntax Int ::= intSeqAt(IntSeq, Int) [function]`
0835. `rule` line 17; tags: equation-or-macro; `rule intSeqAt(iCons(C:Int, _:IntSeq), 0) => C`
0836. `rule` line 18; tags: equation-or-macro; `rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1) requires I >Int 0`
0837. `syntax` line 21; tags: function, total; `syntax Int ::= normIdx(Int, Int) [function, total]`
0838. `rule` line 22; tags: equation-or-macro; `rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I <Int 0`
0839. `rule` line 23; tags: equation-or-macro; `rule normIdx(I:Int, _:Int) => I requires I >=Int 0`
0840. `context` line 27; tags: none; `context Subscript(HOLE, _)`
0841. `context` line 28; tags: none; `context Subscript(_:Val, HOLE:Expr)`
0842. `rule` line 31; tags: priority, operational; `rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0843. `rule` line 35; tags: operational; `rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>`
0844. `syntax` line 37; tags: function; `syntax Val ::= applyIndex(Val, Int) [function]`
0845. `rule` line 38; tags: equation-or-macro; `rule applyIndex(list(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
0846. `rule` line 39; tags: equation-or-macro; `rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))`
0847. `rule` line 40; tags: equation-or-macro; `rule applyIndex(str(IS:IntSeq), I:Int) => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))`
0848. `syntax` line 44; tags: none; `syntax KItem ::= #evalB(Bound) | "#toSome" | #slLo(Val, Bound, Bound) | #slHi(Val, OptInt, Bound) | #slStep(Val, OptInt, OptInt)`
0849. `syntax` line 49; tags: none; `syntax OptInt ::= "noB" | someB(Int)`
0850. `rule` line 50; tags: operational; `rule <k> #evalB(NoBound) => noB ... </k>`
0851. `rule` line 51; tags: operational; `rule <k> #evalB(E:Expr) => E ~> #toSome ... </k>`
0852. `rule` line 52; tags: operational; `rule <k> I:Int ~> #toSome => someB(I) ... </k>`
0853. `rule` line 54; tags: operational; `rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>`
0854. `rule` line 55; tags: operational; `rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound) => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>`
0855. `rule` line 56; tags: operational; `rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound) => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>`
0856. `rule` line 58; tags: priority, operational; `rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt) => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k> [priority(45)]`
0857. `rule` line 61; tags: operational; `rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>`
0858. `syntax` line 63; tags: function; `syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]`
0859. `rule` line 64; tags: equation-or-macro; `rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
0860. `rule` line 66; tags: equation-or-macro; `rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt) => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))`
0861. `rule` line 68; tags: equation-or-macro; `rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt) => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))`
0862. `syntax` line 72; tags: function, total; `syntax Int ::= slStep(OptInt) [function, total]`
0863. `rule` line 73; tags: equation-or-macro; `rule slStep(noB) => 1`
0864. `rule` line 74; tags: equation-or-macro; `rule slStep(someB(S:Int)) => S`
0865. `syntax` line 76; tags: function; `syntax Int ::= slStart(OptInt, OptInt, Int) [function]`
0866. `rule` line 77; tags: equation-or-macro; `rule slStart(noB, ST:OptInt, _LEN:Int) => 0 requires slStep(ST) >Int 0`
0867. `rule` line 79; tags: equation-or-macro; `rule slStart(noB, ST:OptInt, LEN:Int) => LEN -Int 1 requires slStep(ST) <Int 0`
0868. `rule` line 81; tags: equation-or-macro; `rule slStart(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`
0869. `syntax` line 83; tags: function; `syntax Int ::= slStop(OptInt, OptInt, Int) [function]`
0870. `rule` line 84; tags: equation-or-macro; `rule slStop(noB, ST:OptInt, LEN:Int) => LEN requires slStep(ST) >Int 0`
0871. `rule` line 86; tags: equation-or-macro; `rule slStop(noB, ST:OptInt, _LEN:Int) => -1 requires slStep(ST) <Int 0`
0872. `rule` line 88; tags: equation-or-macro; `rule slStop(someB(I:Int), ST:OptInt, LEN:Int) => slAdjust(I, LEN, slStep(ST))`
0873. `syntax` line 90; tags: function, total; `syntax Int ::= slAdjust(Int, Int, Int) [function, total]`
0874. `rule` line 91; tags: equation-or-macro; `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP) requires I <Int 0`
0875. `rule` line 93; tags: equation-or-macro; `rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP) requires I >=Int 0`
0876. `syntax` line 96; tags: function, total; `syntax Int ::= clampLo(Int, Int) [function, total]`
0877. `rule` line 97; tags: equation-or-macro; `rule clampLo(J:Int, _STEP:Int) => J requires J >=Int 0`
0878. `rule` line 99; tags: equation-or-macro; `rule clampLo(J:Int, STEP:Int) => #if STEP <Int 0 #then -1 #else 0 #fi requires J <Int 0`
0879. `syntax` line 102; tags: function, total; `syntax Int ::= clampHi(Int, Int, Int) [function, total]`
0880. `rule` line 103; tags: equation-or-macro; `rule clampHi(I:Int, LEN:Int, _STEP:Int) => I requires I <Int LEN`
0881. `rule` line 105; tags: equation-or-macro; `rule clampHi(I:Int, LEN:Int, STEP:Int) => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi requires I >=Int LEN`
0882. `syntax` line 109; tags: function; `syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]`
0883. `rule` line 110; tags: equation-or-macro; `rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int) => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
0884. `rule` line 113; tags: equation-or-macro; `rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
0885. `syntax` line 116; tags: function; `syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]`
0886. `rule` line 117; tags: equation-or-macro; `rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int) => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP)) requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)`
0887. `rule` line 120; tags: equation-or-macro; `rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))`
## reference-semantics/semantics/syntax.k

0888. `syntax` line 9; tags: macro, strict, seqstrict; `syntax Expr ::= "Int" "(" Int ")" | "Float" "(" Float ")" | "Bool" "(" Bool ")" | "Name" "(" String ")" | "Str" "(" String ")" | "UnaryOp" "(" String "," Expr ")" [strict(2)] | "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2, 3)] | "BoolOp" "(" String "," Exprs ")" | "ListExpr" "(" Exprs ")" | "DictExpr" "(" Entries ")" | "ListComp" "(" Expr "," CompFors ")" [macro] | "GenExp" "(" Expr "," CompFors ")" [macro] | "TupleExpr" "(" Exprs ")" | "Subscript" "(" Expr "," Index ")" | "IfExp" "(" Expr "," Expr "," Expr ")" [strict(1)] | "Lambda" "(" Params "," Expr ")" | "KwArg" "(" String "," Expr ")" | "Lambda" "(" Params "," CellVars "," FreeVars "," Expr ")" | "NoneVal" | "Call" "(" Expr "," Exprs ")" | "Attribute" "(" Expr "," String ")" [strict(1)] | "Compare" "(" Expr "," CmpOp ")"`
0889. `syntax` line 32; tags: none; `syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"`
0890. `syntax` line 33; tags: none; `syntax Entry ::= "Entry" "(" Expr "," Expr ")"`
0891. `syntax` line 34; tags: none; `syntax Entries ::= List{Entry, ","}`
0892. `syntax` line 35; tags: none; `syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"`
0893. `syntax` line 36; tags: none; `syntax CompFors ::= List{CompFor, ""}`
0894. `syntax` line 37; tags: none; `syntax Exprs ::= List{Expr, ","}`
0895. `syntax` line 38; tags: none; `syntax Index ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"`
0896. `syntax` line 39; tags: none; `syntax Bound ::= Expr | "NoBound"`
0897. `syntax` line 41; tags: strict; `syntax Stmt ::= "Assign" "(" Expr "," Expr ")" [strict(2)] | "Import" "(" String ")" | "ImportFrom" "(" String "," ParamNames ")" | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)] | "For" "(" Expr "," Expr "," Stmts ")" [strict(2)] | "While" "(" Expr "," Stmts ")" | "Break" | "Continue" | "If" "(" Expr "," Stmts "," Stmts ")" [strict(1)] | "Return" "(" Expr ")" [strict] | "Assert" "(" Expr ")" [strict] | "Expr" "(" Expr ")" [strict] | "FuncDef" "(" String "," Params "," Stmts ")" | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"`
0898. `syntax` line 56; tags: none; `syntax Stmts ::= List{Stmt, ""}`
0899. `syntax` line 57; tags: none; `syntax Params ::= "Params" "(" ParamNames ")"`
0900. `syntax` line 58; tags: none; `syntax CellVars ::= "CellVars" "(" ParamNames ")"`
0901. `syntax` line 59; tags: none; `syntax FreeVars ::= "FreeVars" "(" ParamNames ")"`
0902. `syntax` line 60; tags: none; `syntax ParamNames ::= List{String, ","}`
0903. `syntax` line 61; tags: none; `syntax Module ::= "Module" "(" Stmts ")"`
## reference-semantics/semantics/tuple.k

0904. `rule` line 10; tags: operational; `rule <k> #iterNext(tuple(.ValSeq)) => #iterDone ... </k>`
0905. `rule` line 11; tags: operational; `rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>`
0906. `syntax` line 14; tags: none; `syntax ApplyK ::= "toTuple"`
0907. `rule` line 15; tags: operational; `rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>`
0908. `rule` line 16; tags: operational; `rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>`
0909. `rule` line 18; tags: equation-or-macro; `rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B`
0910. `rule` line 20; tags: operational; `rule <k> Compare(LV:Val, CmpOp("in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>`
0911. `rule` line 21; tags: operational; `rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>`
0912. `rule` line 23; tags: equation-or-macro; `rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)`
0913. `syntax` line 24; tags: function; `syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]`
0914. `rule` line 25; tags: equation-or-macro; `rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V`
0915. `rule` line 26; tags: equation-or-macro; `rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1) requires notBool (A ==K V)`
0916. `rule` line 28; tags: equation-or-macro; `rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)`
0917. `syntax` line 31; tags: none; `syntax KItem ::= #bindTgt(Expr, Val)`
0918. `rule` line 32; tags: operational; `rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>`
0919. `rule` line 35; tags: priority, operational; `rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k> <env> L:Int </env> <scopes> ... L |-> scope(M:Map, _) ... </scopes> requires "$cells" in_keys(M) andBool pnMember(X, cellsOf({M["$cells"]}:>Val)) andBool X in_keys(M) andBool isCellRef({M[X]}:>Val) [priority(40)]`
0920. `rule` line 42; tags: operational; `rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
0921. `rule` line 43; tags: operational; `rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
0922. `rule` line 44; tags: priority, operational; `rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0923. `syntax` line 49; tags: none; `syntax KItem ::= #unpackSeq(Exprs, ValSeq)`
0924. `rule` line 50; tags: operational; `rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
0925. `rule` line 51; tags: operational; `rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>`
0926. `rule` line 52; tags: priority, operational; `rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k> <heap> ... H |-> V:Val ... </heap> [priority(40)]`
0927. `rule` line 55; tags: operational; `rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq)) => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>`
0928. `rule` line 57; tags: operational; `rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>`
## verification.k

0929. `syntax` line 8; tags: macro; `syntax Module ::= "solutionProgram" [macro]`
0930. `rule` line 9; tags: equation-or-macro; `rule solutionProgram => Module( FuncDef("truncate_number", Params("number"), Return(BinOp("%", Name("number"), Float(1.0)))))`
## spec.k

0931. `claim` line 10; tags: none; `claim <k> #loadAll(solutionProgram) ~> Call(Name("truncate_number"), (Float(N:Float), .Exprs)) => floatMod(N, 1.0) </k> <env> 0 </env> <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope => 0 |-> scope( "truncate_number" |-> closureVal( ("number", .ParamNames), Return(BinOp("%", Name("number"), Float(1.0))) .Stmts, 0), parent(-1)) -1 |-> builtinsScope </scopes> <scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc> <stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>`
