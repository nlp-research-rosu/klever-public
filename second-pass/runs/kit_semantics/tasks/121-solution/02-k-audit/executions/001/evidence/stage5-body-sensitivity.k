requires "verification-base.k"

module STAGE5-BODY-SENSITIVITY
  imports VERIFICATION-BASE

  // Fresh false mutation: advance the real loop body's position by 2, but
  // demand the original program result/state for [1, 3].
  claim [position-step-two]:
    <k>
      #loop(
        list(vCons(1, vCons(3, .ValSeq))),
        Name("value"),
        If(
          Compare(
            BinOp("%", Name("position"), Int(2)),
            CmpOp("==", Int(0))
          ),
          If(
            Compare(
              BinOp("%", Name("value"), Int(2)),
              CmpOp("!=", Int(0))
            ),
            AugAssign(Name("result"), "+", Name("value")) .Stmts,
            .Stmts
          ) .Stmts,
          .Stmts
        )
        AugAssign(Name("position"), "+", Int(2)) .Stmts
      )
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
        1 |-> scope(
          "lst"      |-> list(vCons(1, vCons(3, .ValSeq)))
          "position" |-> 0
          "result"   |-> 0
          "value"    |-> 0,
          parent(0)
        )
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
        1 |-> scope(
          "lst"      |-> list(vCons(1, vCons(3, .ValSeq)))
          "position" |-> 2
          "result"   |-> 1
          "value"    |-> 3,
          parent(0)
        )
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
