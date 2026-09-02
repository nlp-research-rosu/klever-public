requires "verification.k"

module SPEC-VACUITY
  imports VALID-DATE-VERIFICATION

  // Fresh adversarial mutation: reverse the exact result required by the
  // length-ten entry claim.  Witness 03-11-2000 makes validDate10 true and
  // the real program returns true, while this destination requires false.
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
      notBool validDate10(
        M0, M1, SEP1, D0, D1, SEP2, Y0, Y1, Y2, Y3
      )
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
