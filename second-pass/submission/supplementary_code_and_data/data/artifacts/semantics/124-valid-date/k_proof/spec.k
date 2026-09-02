requires "verification.k"

module VALID-DATE-SPEC
  imports VALID-DATE-VERIFICATION

  // Every string whose length is not ten is rejected. Together with the next
  // claim, this covers every string in the semantics' IntSeq representation.
  claim
    <k>
      #loadAll(validDateModule)
      ~> Call(Name("valid_date"), str(CS:IntSeq))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope("valid_date" |-> validDateClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(CS) =/=Int 10

  // A ten-character string is accepted exactly when it has mm-dd-yyyy digit
  // and separator syntax and its month/day obey the prompt's bounds.
  claim
    <k>
      #loadAll(validDateModule)
      ~>
      Call(
        Name("valid_date"),
        str(iCons(
          M0:Int,
          iCons(
            M1:Int,
            iCons(
              SEP1:Int,
              iCons(
                D0:Int,
                iCons(
                  D1:Int,
                  iCons(
                    SEP2:Int,
                    iCons(
                      Y0:Int,
                      iCons(
                        Y1:Int,
                        iCons(
                          Y2:Int,
                          iCons(Y3:Int, .IntSeq)))))))))))
      )
      =>
      validDate10(M0, M1, SEP1, D0, D1, SEP2, Y0, Y1, Y2, Y3)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope("valid_date" |-> validDateClosure, parent(-1))
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
