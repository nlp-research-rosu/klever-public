requires "/tmp/audit-work/verification.k"

module REVIEWER-EMPTY-LIST-BASE-SPEC
  imports PAIRS-VERIFICATION

  claim [fixed-semantics-result]:
    <k>
      Call(
        closureVal(
          .ParamNames,
          If(ListExpr(.Exprs), Return(Bool(true)), .Stmts)
          Return(Bool(false))
          .Stmts,
          0),
        .Exprs)
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module REVIEWER-EMPTY-LIST-LEMMA-SPEC
  imports PAIRS-VERIFICATION-LEMMAS

  // This conclusion is false in Python and under the supplied base semantics,
  // but becomes provable solely because the priority-40 toList bridge changes
  // the empty list's representation and hence its truthiness.
  claim [false-bridge-enabled-result]:
    <k>
      Call(
        closureVal(
          .ParamNames,
          If(ListExpr(.Exprs), Return(Bool(true)), .Stmts)
          Return(Bool(false))
          .Stmts,
          0),
        .Exprs)
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(intValues(.IntSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
