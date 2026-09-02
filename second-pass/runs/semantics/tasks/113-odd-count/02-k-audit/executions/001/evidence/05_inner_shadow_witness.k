requires "verification.k"

module ODD-COUNT-INNER-SHADOW-WITNESS
  imports ODD-COUNT-VERIFICATION

  claim
    <k>
      For(
        Name("digit"),
        str(iCons(49, .IntSeq)),
        ODD-INNER-BODY)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
              "int" |-> closureVal(
                         "x",
                         Return(Int(0)) .Stmts,
                         0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(.ValSeq))
              ("result" |-> ref(0))
              ("digits" |-> str(iCons(49, .IntSeq)))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "int" |-> closureVal(
                         "x",
                         Return(Int(0)) .Stmts,
                         0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(.ValSeq))
              ("result" |-> ref(0))
              ("digits" |-> str(iCons(49, .IntSeq)))
              ("count" |-> 1)
              ("digit" |-> str(iCons(49, .IntSeq)))
              ("text" |-> str(.IntSeq)),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(inner-bridge-shadow)]
endmodule
