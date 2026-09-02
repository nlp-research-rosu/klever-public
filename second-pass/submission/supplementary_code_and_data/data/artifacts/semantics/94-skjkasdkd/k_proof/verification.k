requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Explicit form of Map deletion used by function-frame teardown.
  rule (((X:KItem |-> _:KItem) M:Map) [ X <- undef ]) => M
       requires notBool (X in_keys(M))
       [simplification]
  rule (M:Map [ X:KItem <- V:KItem ]) => (X |-> V) M
       requires notBool (X in_keys(M))
       [simplification]

  // Proof-normalization lemmas for ordinary (non-closure-cell) frames.  These
  // are guarded specializations of MPY's existing rules; the priority prevents
  // the symbolic prover from exploring impossible cellRef branches after the
  // guard has established that "$cells" is absent.
  rule <k> Name(X:String) => {M[X]}:>Val ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M) andBool notBool ("$cells" in_keys(M))
       [priority(39)]

  rule <k> Name(X:String) => V:Val ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _:Parent) ... </scopes>
       requires notBool ("$cells" in_keys(M))
       [priority(39)]

  // Direct literal cooling, equivalent to Int(I) => I followed by Assign's
  // strictness context.  Keeping it explicit avoids a symbolic freezer branch
  // at loop-summary boundaries.
  rule <k> Assign(Name(X:String), Int(I:Int)) => Assign(Name(X), I) ... </k>
       [priority(39)]

  rule <k> Assign(Name(X:String), Bool(B:Bool)) => Assign(Name(X), B) ... </k>
       [priority(39)]

  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         ((X |-> _:Val) M:Map => (X |-> V) M),
         _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ],
         _:Parent) ... </scopes>
       requires X in_keys(M)
         andBool notBool ("$cells" in_keys(M))
         andBool notBool isRefV({M[X]}:>Val)
       [priority(39)]

  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         ((X |-> A:Val) M:Map => (X |-> applyBin(OP, A, V)) M),
         _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> A) M))
         andBool notBool isRefV(A)
       [priority(38)]

  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _:Parent) ... </scopes>
       requires notBool ("$cells" in_keys(M))
       [priority(39)]

  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         ((X |-> _:Val) M:Map => (X |-> V) M),
         _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  // Strictness-normalized forms used by the outer list loop.
  rule <k> Compare(Name(X:String), CmpOp(OP:String, Name(Y:String)))
        => applyCmp(OP, A, B) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(
         (X |-> A:Val) (Y |-> B:Val) M:Map,
         _:Parent) ... </scopes>
       requires X =/=String Y
         andBool notBool (X in_keys(M))
         andBool notBool (Y in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> A) (Y |-> B) M))
       [priority(38)]

  rule <k> Compare(Name(X:String), CmpOp(OP:String, Int(I:Int)))
        => applyCmp(OP, A, I) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> A:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> A) M))
       [priority(38)]

  rule <k> If(Name(X:String), T:Stmts, E:Stmts)
        => #branch(truthy(V), T, E) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  rule <k> Assign(Name(X:String), Name(Y:String))
        => Assign(Name(X), V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((Y |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (Y in_keys(M))
         andBool notBool ("$cells" in_keys((Y |-> V) M))
       [priority(38)]

  rule <k> Return(Name(X:String)) => Return(V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  rule <k> For(T:Expr, Name(X:String), B:Stmts)
        => #loop(V, T, B) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope((X |-> V:Val) M:Map, _:Parent) ... </scopes>
       requires notBool (X in_keys(M))
         andBool notBool ("$cells" in_keys((X |-> V) M))
       [priority(38)]

  rule <k>
         Call(
           Name("skjkasdkd"),
           (list(asVals(IS:IntList)), .Exprs))
        => #applyK(
             toCall(closureVal(
               ("lst", .ParamNames),
               #functionBody,
               0)),
             (list(asVals(IS)), .Vals)) ...
       </k>
       <env> 0 </env>
       <scopes>
         ... 0 |-> scope(
           ("skjkasdkd" |-> closureVal(
             ("lst", .ParamNames),
             #functionBody,
             0))
           M:Map,
           parent(-1)) ...
       </scopes>
       requires notBool ("skjkasdkd" in_keys(M))
       [priority(38)]

  rule <k>
         Assign(
           Name("prime"),
           Compare(Name("number"), CmpOp(">=", Int(2))))
        => Assign(Name("prime"), N >=Int 2) ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(("number" |-> N:Int) M:Map, _:Parent) ... </scopes>
       requires notBool ("number" in_keys(M))
         andBool notBool ("$cells" in_keys(("number" |-> N) M))
       [priority(38)]

  // Integer-only input lists.  This sort makes the task's stated input
  // precondition structural, so symbolic execution never admits a non-int
  // element.
  syntax IntList ::= ".IntList" | intCons(Int, IntList)

  syntax ValSeq ::= asVals(IntList)

  // Structural iterator cases expose IntList's constructors to narrowing.
  rule <k> #iterNext(list(asVals(.IntList))) => #iterDone ... </k>
       [priority(39)]
  rule <k> #iterNext(list(asVals(intCons(I:Int, IS:IntList))))
        => #iterYield(I, list(asVals(IS))) ... </k>
       [priority(39)]

  // The mathematical primality oracle follows the implementation's trial
  // division exactly.  false means that an earlier divisor was already found.
  syntax Bool ::= trialPrime(Int, Int, Bool) [function, total]
  rule trialPrime(_:Int, _:Int, false) => false
  rule trialPrime(N:Int, D:Int, true) => true
    requires D *Int D >Int N
  rule trialPrime(N:Int, D:Int, true) => false
    requires D *Int D <=Int N andBool pyMod(N, D) ==Int 0
    [simplification]
  rule trialPrime(N:Int, D:Int, true) => trialPrime(N, D +Int 1, true)
    requires D *Int D <=Int N
      andBool notBool (pyMod(N, D) ==Int 0)
    [simplification]

  // The final divisor value is specified too, allowing the loop invariant to
  // describe the whole local store rather than hiding a side effect.
  syntax Int ::= trialDivisor(Int, Int, Bool) [function, total]
  rule trialDivisor(_:Int, D:Int, false) => D
  rule trialDivisor(N:Int, D:Int, true) => D
    requires D *Int D >Int N
  rule trialDivisor(N:Int, D:Int, true) => D +Int 1
    requires D *Int D <=Int N andBool pyMod(N, D) ==Int 0
    [simplification]
  rule trialDivisor(N:Int, D:Int, true)
    => trialDivisor(N, D +Int 1, true)
    requires D *Int D <=Int N
      andBool notBool (pyMod(N, D) ==Int 0)
    [simplification]

  syntax Bool ::= isPrime(Int) [function, total]
  rule isPrime(N:Int) => trialPrime(N, 2, N >=Int 2)

  syntax Int ::= largestPrime(IntList, Int) [function, total]
  rule largestPrime(.IntList, CUR:Int) => CUR
  rule largestPrime(intCons(N:Int, IS:IntList), CUR:Int)
    => largestPrime(IS, N)
    requires N >Int CUR andBool isPrime(N)
    [simplification]
  rule largestPrime(intCons(N:Int, IS:IntList), CUR:Int)
    => largestPrime(IS, CUR)
    requires N <=Int CUR
      orBool (N >Int CUR andBool notBool isPrime(N))
    [simplification]

  syntax Int ::= digitAcc(Int, Int) [function, total]
  rule digitAcc(N:Int, A:Int) => A
    requires N <=Int 0
    [simplification]
  rule digitAcc(N:Int, A:Int)
    => digitAcc(
         (N -Int pyMod(N, 10)) /Int 10,
         A +Int pyMod(N, 10))
    requires N >Int 0
    [simplification]

  syntax Int ::= digitSum(Int) [function, total]
  rule digitSum(N:Int) => digitAcc(N, 0)

  // Exact AST fragments emitted by py2mpy.py for solution.py.
  syntax Expr ::= "#primeCond" [macro]
  rule #primeCond => BoolOp(
    "and",
    Name("prime"),
    Compare(
      BinOp("*", Name("divisor"), Name("divisor")),
      CmpOp("<=", Name("number"))))

  syntax Stmts ::= "#primeBody" [macro]
  rule #primeBody =>
    If(Compare(
      BinOp("%", Name("number"), Name("divisor")),
      CmpOp("==", Int(0))),
      Assign(Name("prime"), Bool(false)),
      .Stmts)
    AugAssign(Name("divisor"), "+", Int(1))

  syntax Stmts ::= "#scanBody" [macro]
  rule #scanBody =>
    If(Compare(Name("number"), CmpOp(">", Name("largest"))),
      Assign(Name("divisor"), Int(2))
      Assign(
        Name("prime"),
        Compare(Name("number"), CmpOp(">=", Int(2))))
      While(#primeCond, #primeBody)
      If(Name("prime"),
        Assign(Name("largest"), Name("number")),
        .Stmts),
      .Stmts)

  syntax Expr ::= "#digitCond" [macro]
  rule #digitCond =>
    Compare(Name("largest"), CmpOp(">", Int(0)))

  syntax Stmts ::= "#digitBody" [macro]
  rule #digitBody =>
    AugAssign(
      Name("digit_total"),
      "+",
      BinOp("%", Name("largest"), Int(10)))
    AugAssign(Name("largest"), "//", Int(10))

  syntax Stmts ::= "#functionBody" [macro]
  rule #functionBody =>
    Assign(Name("largest"), Int(0))
    Assign(Name("number"), Int(0))
    Assign(Name("divisor"), Int(2))
    Assign(Name("prime"), Bool(false))
    Assign(Name("digit_total"), Int(0))
    For(Name("number"), Name("lst"), #scanBody)
    While(#digitCond, #digitBody)
    Return(Name("digit_total"))

  // Bounded entry-prefix summary.  It is the direct composition of MPY-CALL's
  // frame allocation, #bindP, the five literal assignments, and For's
  // one-time iterable evaluation.  No loop iteration is summarized here.
  rule <k>
         #applyK(
           toCall(closureVal(
             ("lst", .ParamNames),
             #functionBody,
             0)),
           (list(asVals(IS:IntList)), .Vals))
        =>
         #loop(list(asVals(IS)), Name("number"), #scanBody)
         ~> While(#digitCond, #digitBody)
         ~> Return(Name("digit_total"))
         ~> #endcall
       </k>
       <env> 0 => 1 </env>
       <scopes>
         MOD:Map
         =>
         MOD
         1 |-> scope(
           ("lst" |-> list(asVals(IS)))
           ("largest" |-> 0)
           ("number" |-> 0)
           ("divisor" |-> 2)
           ("prime" |-> false)
           ("digit_total" |-> 0),
           parent(0))
       </scopes>
       <scopeLoc> 1 => 2 </scopeLoc>
       <stack>
         .List => ListItem(frame(.K, 0, 1))
       </stack>
       requires notBool (1 in_keys(MOD))
       [priority(37)]

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule =>
    Module(FuncDef("skjkasdkd", Params("lst"), #functionBody))
endmodule
