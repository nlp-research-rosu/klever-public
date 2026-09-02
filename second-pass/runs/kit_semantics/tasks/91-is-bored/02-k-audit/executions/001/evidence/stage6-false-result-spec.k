requires "verification.k"

module STAGE6-FALSE-RESULT-SPEC
  imports VERIFICATION

  // Deliberately false for the realizable input "I work": the submitted
  // program and the proved summary both return 1, not 2.
  claim [i-work-wrong-result]:
    <k>
      Call(
        Name("is_bored"),
        ( str(
            iCons(73,
              iCons(32,
                iCons(119,
                  iCons(111,
                    iCons(114,
                      iCons(107, .IntSeq))))))
          ),
          .Exprs )
      )
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          BORED-FUNCTION-BODY,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
