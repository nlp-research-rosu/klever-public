requires "verification.k"

module ODD-COUNT-OUTER-SHADOW-WITNESS
  imports ODD-COUNT-VERIFICATION

  claim
    <k>
      #loop(
        list(
          vCons(
            str(iCons(49, .IntSeq)),
            .ValSeq)),
        Name("digits"),
        ODD-OUTER-BODY)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
              "str" |-> closureVal(
                         "x",
                         Return(Str("")) .Stmts,
                         0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(
                          vCons(
                            str(iCons(49, .IntSeq)),
                            .ValSeq)))
              ("result" |-> ref(0))
              ("digits" |-> str(.IntSeq))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "str" |-> closureVal(
                         "x",
                         Return(Str("")) .Stmts,
                         0),
              parent(-1))
      1  |-> scope(
              ("lst" |-> list(
                          vCons(
                            str(iCons(49, .IntSeq)),
                            .ValSeq)))
              ("result" |-> ref(0))
              ("digits" |-> str(.IntSeq))
              ("count" |-> 0)
              ("digit" |-> str(.IntSeq))
              ("text" |-> str(.IntSeq)),
              parent(0))
    </scopes>
    <heap>
      0 |-> list(.ValSeq)
      =>
      0 |-> list(
             oddCountFrom(
               .ValSeq,
               vCons(
                 str(iCons(49, .IntSeq)),
                 .ValSeq)))
    </heap>
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(bridge-shadow)]
endmodule
