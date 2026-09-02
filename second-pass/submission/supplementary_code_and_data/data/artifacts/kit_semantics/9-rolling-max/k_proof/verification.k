requires "reference-semantics/semantics.k"

module VERIFICATION-SUMMARIES
  imports MPY
  imports INT

  // The complete formal domain: every element of the MPY payload is an Int.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, R:ValSeq))
    => isInt(V) andBool allInts(R)

  rule { true #Equals isInt(V:Val) }
    => #Exists I:Int . { V #Equals I }
    [simplification]

  syntax Int ::= stepMax(Int, Int) [function, total]
  rule stepMax(M:Int, I:Int) => I requires I >Int M
  rule stepMax(M:Int, I:Int) => M requires I <=Int M

  // Execute the mathematical rolling-maximum fold while accumulating the
  // already-produced prefix exactly as list.append does.
  syntax ValSeq ::= rollAcc(ValSeq, Int, ValSeq) [function, total]
  rule rollAcc(A:ValSeq, _:Int, .ValSeq) => A
  rule rollAcc(A:ValSeq, M:Int, vCons(I:Int, R:ValSeq))
    => rollAcc(
         valSeqConcat(A, vCons(stepMax(M, I), .ValSeq)),
         stepMax(M, I),
         R)
  rule rollAcc(A:ValSeq, _:Int, vCons(_:Val, _:ValSeq)) => A [owise]

  syntax ValSeq ::= rollingMax(ValSeq) [function, total]
  rule rollingMax(.ValSeq) => .ValSeq
  rule rollingMax(vCons(H:Int, T:ValSeq))
    => rollAcc(.ValSeq, H, vCons(H, T))
  rule rollingMax(vCons(_:Val, _:ValSeq)) => .ValSeq [owise]

  // Final scalar locals of the source for-loop.
  syntax Int ::= foldMax(Int, ValSeq) [function, total]
  rule foldMax(M:Int, .ValSeq) => M
  rule foldMax(M:Int, vCons(I:Int, R:ValSeq))
    => foldMax(stepMax(M, I), R)
  rule foldMax(M:Int, vCons(_:Val, _:ValSeq)) => M [owise]

  syntax Int ::= lastOr(Int, ValSeq) [function, total]
  rule lastOr(D:Int, .ValSeq) => D
  rule lastOr(_:Int, vCons(I:Int, R:ValSeq)) => lastOr(I, R)
  rule lastOr(D:Int, vCons(_:Val, _:ValSeq)) => D [owise]
endmodule

module VERIFICATION-CORE
  imports VERIFICATION-SUMMARIES

  // Exact specialization of MPY-TUPLE's plain-frame target-binding rule.
  // bind-spec.k proves this transition without importing VERIFICATION.
  rule <k> #bindTgt(Name(X:String), I:Int) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(M:Map => M [ X <- I ], P:Parent) ...
       </scopes>
       requires notBool ("$cells" in_keys(M))
       [priority(40)]
endmodule

module VERIFICATION
  imports VERIFICATION-CORE

  // Exact loop summary. loop-spec.k proves this complete transition against
  // VERIFICATION-CORE (fixed MPY execution plus the separately connected
  // binding specialization) before this rule is used by the entry proof.
  rule
    <k>
      #loop(
        list(IS:ValSeq),
        Name("number"),
        If(
          Compare(Name("number"), CmpOp(">", Name("current"))),
          Assign(Name("current"), Name("number")) .Stmts,
          .Stmts)
        Expr(Call(
          Attribute(Name("result"), "append"),
          (Name("current"), .Exprs))) .Stmts)
      ~> .Stmts
      ~> Return(Name("result")) .Stmts
      ~> #endcall
      =>
      .Stmts
      ~> Return(Name("result")) .Stmts
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(MODULE:Map, parent(-1))
      1 |-> scope(
        "current" |-> (M:Int => foldMax(M, IS))
        "number"  |-> (D:Int => lastOr(D, IS))
        "numbers" |-> list(ORIGINAL:ValSeq)
        "result"  |-> ref(0),
        parent(0))
      -1 |-> BUILTINS:Scope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(A:ValSeq => rollAcc(A, M, IS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(IS)
    [priority(40)]
endmodule
