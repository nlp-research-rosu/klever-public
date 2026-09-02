requires "/tmp/audit-work/27-flip-case/candidate/verification.k"

module ADEQUACY-WITNESS
  imports VERIFICATION

  // S = the code sequence for "Hello"; the RHS is the literal code sequence
  // for "hELLO", not mapSwap(S).
  claim
    <k>
      #runFlipCase(
        iCons(72,
          iCons(101,
            iCons(108,
              iCons(108,
                iCons(111, .IntSeq))))))
      =>
      str(
        iCons(104,
          iCons(69,
            iCons(76,
              iCons(76,
                iCons(79, .IntSeq))))))
    </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0  |-> scope(
                 "flip_case" |->
                   closureVal(
                     ("string", .ParamNames),
                     flipCaseBody,
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
