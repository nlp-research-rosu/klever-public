requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Exact constructor terms emitted in solution.mpy.
  syntax Stmts ::= nearBody() [function, total]
  rule nearBody() =>
    If(Compare(Call(Name("abs"),
                    BinOp("-", Name("number"), Name("other"))),
               CmpOp("<", Name("threshold"))),
       Assign(Name("found"), Bool(true))
       Break
       .Stmts,
       .Stmts)
    .Stmts

  syntax Stmts ::= helperLoopBody() [function, total]
  rule helperLoopBody() =>
    If(Compare(Name("index"), CmpOp(">=", Name("start"))),
       nearBody(),
       .Stmts)
    AugAssign(Name("index"), "+", Int(1))
    .Stmts

  syntax Stmts ::= helperBody() [function, total]
  rule helperBody() =>
    Assign(Name("found"), Bool(false))
    Assign(Name("index"), Int(0))
    Assign(Name("other"), Name("number"))
    For(Name("other"), Name("numbers"), helperLoopBody())
    Assign(Name("index"), Int(0))
    Assign(Name("other"), Name("number"))
    Return(Name("found"))
    .Stmts

  syntax Stmts ::= outerLoopBody() [function, total]
  rule outerLoopBody() =>
    If(Call(Name("is_close_to_any"),
            Name("number"), Name("numbers"), Name("threshold"),
            Name("start"), .Exprs),
       Assign(Name("found"), Bool(true))
       Break
       .Stmts,
       .Stmts)
    AugAssign(Name("start"), "+", Int(1))
    .Stmts

  syntax Stmts ::= entryBody() [function, total]
  rule entryBody() =>
    Assign(Name("found"), Bool(false))
    Assign(Name("start"), Int(1))
    Assign(Name("number"), Name("threshold"))
    For(Name("number"), Name("numbers"), outerLoopBody())
    Assign(Name("start"), Int(1))
    Assign(Name("number"), Name("threshold"))
    Return(Name("found"))
    .Stmts

  syntax Val ::= helperClosure() [function, total]
               | entryClosure()  [function, total]
  rule helperClosure() =>
    closureVal(("number", "numbers", "threshold", "start"), helperBody(), 0)
  rule entryClosure() =>
    closureVal(("numbers", "threshold"), entryBody(), 0)

  syntax Module ::= solutionModule() [function, total]
  rule solutionModule() =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("is_close_to_any",
              Params("number", "numbers", "threshold", "start"),
              helperBody())
      FuncDef("has_close_elements",
              Params("numbers", "threshold"),
              entryBody())
      .Stmts)

  syntax Scope ::= solutionScope() [function, total]
  rule solutionScope() =>
    scope(.Map
          [ "is_close_to_any" <- helperClosure() ]
          [ "has_close_elements" <- entryClosure() ],
          parent(-1))

  // A typed proof-only ValSeq representation. The two iterator equations below
  // are the representation relation to MPY lists and make every yielded
  // element statically Float to the prover.
  syntax ValSeq ::= FloatSeq
  syntax FloatSeq ::= ".FloatSeq" | fCons(Float, FloatSeq)
  rule <k> #iterNext(list(.FloatSeq)) => #iterDone ... </k>
    [priority(40)]
  rule <k> #iterNext(list(fCons(F:Float, R:FloatSeq)))
        => #iterYield(F, list(R)) ... </k>
    [priority(40)]

  syntax Bool ::= near(Float, Float, Float) [function, total]
  rule near(A:Float, B:Float, T:Float) => floatLt(absF(subF(A, B)), T)

  // Search CUR, whose first element has absolute index I, ignoring elements
  // before START. This is exactly the helper's loop invariant.
  syntax Bool ::= closeSkip(Float, FloatSeq, Float, Int, Int) [function, total]
  rule closeSkip(_:Float, .FloatSeq, _:Float, _:Int, _:Int) => false
  rule closeSkip(A:Float, fCons(_:Float, R:FloatSeq), T:Float,
                 I:Int, START:Int)
    => closeSkip(A, R, T, I +Int 1, START)
    requires I <Int START
  rule closeSkip(A:Float, fCons(B:Float, R:FloatSeq), T:Float,
                 I:Int, START:Int)
    => near(A, B, T) orBool closeSkip(A, R, T, I +Int 1, START)
    requires I >=Int START

  // For each head of CUR, compare it with the portion of ALL beginning at
  // START, then advance both CUR and START. Initially CUR=ALL and START=1,
  // so this denotes exactly all pairs of distinct positions i < j.
  syntax Bool ::= hasPairs(FloatSeq, FloatSeq, Float, Int) [function, total]
  rule hasPairs(_:FloatSeq, .FloatSeq, _:Float, _:Int) => false
  rule hasPairs(ALL:FloatSeq, fCons(A:Float, R:FloatSeq), T:Float, START:Int)
    => closeSkip(A, ALL, T, 0, START)
       orBool hasPairs(ALL, R, T, START +Int 1)

  syntax KItem ::= "#proofDone"
endmodule

// Staged proved lemmas; prove.sh compiles each only after proving the identical
// claim against the preceding module.
module VERIFICATION-WITH-INNER
  imports VERIFICATION-BASE

  rule <k> For(Name("other"), list(ALL:FloatSeq), _B:Stmts)
        => .K ... </k>
       <env> 2 </env>
       <scopes> ... 2 |-> scope(M:Map => M
                                  [ "found" <- closeSkip(A, ALL, T, 0, START) ]
                                  [ "index" <- 0 ]
                                  [ "other" <- A ],
                                parent(0)) ... </scopes>
       <ret> noRet </ret>
    requires {M["number"]}:>Val ==K A
     andBool {M["numbers"]}:>Val ==K list(ALL)
     andBool {M["threshold"]}:>Val ==K T
     andBool {M["start"]}:>Val ==K START
     andBool {M["found"]}:>Val ==K false
     andBool {M["index"]}:>Val ==K 0
    [priority(45)]
endmodule

module VERIFICATION-WITH-HELPER
  imports VERIFICATION-WITH-INNER

  rule <k> Call(Name("is_close_to_any"),
                Name("number"), Name("numbers"), Name("threshold"),
                Name("start"), .Exprs)
        => closeSkip(A, ALL, T, 0, START) ... </k>
       <env> 1 </env>
       <scopes> ... 1 |-> scope(M:Map, parent(0)) ... </scopes>
    requires {M["number"]}:>Val ==K A:Float
     andBool {M["numbers"]}:>Val ==K list(ALL:FloatSeq)
     andBool {M["threshold"]}:>Val ==K T:Float
     andBool {M["start"]}:>Val ==K START:Int
    [priority(40)]

  rule <k> #applyK(toCall(closureVal(
                     ("number", "numbers", "threshold", "start"),
                     _BODY:Stmts, 0)),
                   (A:Float, list(ALL:FloatSeq),
                    T:Float, START:Int, .Vals)) ~> K:K
        => closeSkip(A, ALL, T, 0, START) ~> K ... </k>
       <env> 1 </env>
       <scopeLoc> 2 </scopeLoc>
       <ret> noRet </ret>
    [priority(40)]
endmodule

module VERIFICATION-WITH-OUTER
  imports VERIFICATION-WITH-HELPER

  rule <k> For(Name("number"), list(ALL:FloatSeq), _B:Stmts)
        => .K ... </k>
       <env> 1 </env>
       <scopes> ... 1 |-> scope(M:Map => M
                                  [ "found" <- hasPairs(ALL, ALL, T, 1) ]
                                  [ "start" <- 1 ]
                                  [ "number" <- T ],
                                parent(0)) ... </scopes>
       <ret> noRet </ret>
    requires {M["numbers"]}:>Val ==K list(ALL)
     andBool {M["threshold"]}:>Val ==K T:Float
     andBool {M["found"]}:>Val ==K false
     andBool {M["start"]}:>Val ==K 1
    [priority(45)]
endmodule

module VERIFICATION-WITH-ENTRY
  imports VERIFICATION-WITH-OUTER

  rule <k> Call(Name("has_close_elements"),
                list(ALL:FloatSeq), T:Float, .Exprs)
        => hasPairs(ALL, ALL, T, 1) ... </k>
       <env> 0 </env>
       <scopeLoc> 1 </scopeLoc>
       <ret> noRet </ret>
    [priority(40)]
endmodule

module VERIFICATION
  imports VERIFICATION-WITH-ENTRY
endmodule
