requires "verification.k"

module SUM-SQUARES-SPEC
  imports SUM-SQUARES-VERIFICATION

  // Inductive loop invariant after at least one element has been bound.  The
  // local map is exact, which also records that this is a plain (non-cell)
  // function frame.  The claim is proved first, then admitted as a proved
  // lemma while proving the end-to-end function claim.
  claim [loop]:
    <k>
      #loop(list(intVals(IS:Ints)), Name("value"), sumSquaresLoopBody)
      ~> (Return(Name("total")) .Stmts)
      ~> #endcall
      ~> KONT:K
    =>
      (Return(Name("total")) .Stmts)
      ~> #endcall
      ~> KONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      (L |-> scope(
        "lst"   |-> list(intVals(ORIG:Ints))
        "value" |-> OLD:Int
        "total" |-> ACC:Int
        "index" |-> I:Int,
        P:Parent))
    =>
      SC
      (L |-> scope(
        "lst"   |-> list(intVals(ORIG))
        "value" |-> endValue(IS, OLD)
        "total" |-> sumSquares(IS, I, ACC)
        "index" |-> endIndex(IS, I),
        P))
    </scopes>

  // Function-body summary from the initialized local frame through return.
  // This isolates frame cleanup from the loop induction.
  claim [body]:
    <k>
      #loop(list(intVals(IS:Ints)), Name("value"), sumSquaresLoopBody)
      ~> (Return(Name("total")) .Stmts)
      ~> #endcall
    =>
      sumSquares(IS, 0, 0)
      ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "sum_squares" |->
          closureVal(
            ("lst", .ParamNames),
            sumSquaresFunctionBody,
            0),
        parent(-1))
      1  |-> scope(
        "lst"   |-> list(intVals(IS))
        "total" |-> 0
        "index" |-> 0,
        parent(0))
    =>
      -1 |-> builtinsScope
      0  |-> scope(
        "sum_squares" |->
          closureVal(
            ("lst", .ParamNames),
            sumSquaresFunctionBody,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(CONT, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // End-to-end correctness for every finite list of mathematical integers.
  claim [main]:
    <k>
      Call(
        Name("sum_squares"),
        (list(intVals(IS:Ints)), .Exprs))
    =>
      sumSquares(IS, 0, 0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "sum_squares" |->
          closureVal(
            ("lst", .ParamNames),
            sumSquaresFunctionBody,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
